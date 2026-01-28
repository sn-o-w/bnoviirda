import asyncio, re, signal, ssl, unicodedata, websockets
import variabile_globale as vg
from time import time
from typing import Optional
from jocuri.jocuri_ruleta import ruleta
from jocuri.jocuri_phf import phf, penalizare_phf
from jocuri.jocuri_loto import mods_loto, loto_castigat
from jocuri.jocuri_blackjack import blackjack, penalizare_blackjack
from jocuri.jocuri_activare import on, off, on_auto, off_auto
from comenzi_globale.love import love
from comenzi_globale.cuminte import cuminte
from comenzi_globale.grinch import grinch
from comenzi_globale.flower import flower, top_10_flower
from comenzi_globale.video_random import video_random
from comenzi_globale.comenzi_help import comenzi, ajutor, botplay, new_user
from comenzi_mods.coinflip import mods_coinflip
from comenzi_mods.categorie import mods_schimba_categoria
from comenzi_mods.intrebari import intrebari
from puncte import puncte_chat, puncte_user, mods_puncte, schimb_puncte, top_10_vons


class TwitchBot:
    WS_URI = "wss://irc-ws.chat.twitch.tv:443"

    CONNECT_TIMEOUT = 15.0
    READY_TIMEOUT = 10.0
    PING_TIMEOUT = 360.0
    PING_CHECK_INTERVAL = 60.0

    RL_WINDOW = 30.0
    RL_NORMAL = 20
    RL_MOD = 100

    SEND_QUEUE_SIZE = 1000
    MSG_QUEUE_SIZE = 2000

    WS_MAX_QUEUE = 64

    BJ_OFF_CATEGORIES = {
        "Marbles On Stream",
        "Just Chatting",
        "Food & Drink",
        "Travel & Outdoors",
    }

    @staticmethod
    def normalize(text: str) -> str:
        return (
            unicodedata.normalize("NFKD", text)
            .encode("ascii", "ignore")
            .decode("utf-8", "ignore")
        )

    @staticmethod
    def parse_tags(raw: str) -> dict:
        out = {}
        if not raw:
            return out
        for kv in raw.split(";"):
            if "=" in kv:
                k, v = kv.split("=", 1)
                v = (
                    v.replace("\\s", " ")
                    .replace("\\n", "\n")
                    .replace("\\r", "\r")
                    .replace("\\:", ";")
                    .replace("\\\\", "\\")
                )
                out[k] = v
            else:
                out[kv] = ""
        return out

    @staticmethod
    def parse_irc_line(line: str) -> dict:
        tags = {}
        prefix = None
        trailing = None
        params = []

        rest = line

        if rest.startswith("@"):
            sp = rest.find(" ")
            if sp != -1:
                tags = TwitchBot.parse_tags(rest[1:sp])
                rest = rest[sp + 1 :]

        if rest.startswith(":"):
            sp = rest.find(" ")
            if sp != -1:
                prefix = rest[1:sp]
                rest = rest[sp + 1 :]

        if " :" in rest:
            before, trailing = rest.split(" :", 1)
        else:
            before = rest

        parts = before.split()
        if not parts:
            return {"tags": tags, "prefix": prefix, "command": "", "params": [], "trailing": trailing}

        return {"tags": tags, "prefix": prefix, "command": parts[0], "params": parts[1:], "trailing": trailing}

    @staticmethod
    def nick_from_prefix(prefix: Optional[str]) -> Optional[str]:
        if not prefix:
            return None
        return prefix.split("!", 1)[0]

    def __init__(self, username: str, client_id: str, token: str, channel: str):
        self.client_id = client_id
        self.username = username.lower()
        self.token = token.replace("oauth:", "").strip()
        self.channel = "#" + channel.lower()
        self.channel_id = vg.owner_id
        self.connection = self
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._ws: Optional[websockets.WebSocketClientProtocol] = None
        self._shutdown = False
        self._send_lock = None
        self._sender_task: Optional[asyncio.Task] = None
        self._listener_task: Optional[asyncio.Task] = None
        self._worker_task: Optional[asyncio.Task] = None
        self._ping_watchdog_task: Optional[asyncio.Task] = None
        self._send_q = None
        self._msg_q = None
        self._joined = False
        self._caps_acked = {"membership": False, "tags": False, "commands": False}
        self._ev_joined = None
        self._ev_caps = None
        self._last_ping_time = 0.0
        self._is_mod_in_channel = False
        self._rl_max = self.RL_NORMAL
        self._rl_sent_ts: list[float] = []

    def privmsg(self, channel: str, text: str):
        if not channel.startswith("#"):
            channel = "#" + channel
        self._enqueue_send(f"PRIVMSG {channel} :{text}")

    def send_msg(self, text: str):
        self.privmsg(self.channel, text)

    def _enqueue_send(self, line: str):
        if self._loop is None:
            return

        line = line.rstrip("\r\n") + "\r\n"

        def _put():
            try:
                self._send_q.put_nowait(line)
            except asyncio.QueueFull:
                # drop (mai bine decât să consumi RAM / să blochezi)
                pass

        self._loop.call_soon_threadsafe(_put)

    async def _ws_send_now(self, line: str):
        if not self._ws:
            return
        async with self._send_lock:
            await self._ws.send(line.rstrip("\r\n") + "\r\n")

    def _update_rate_limit(self):
        self._rl_max = self.RL_MOD if self._is_mod_in_channel else self.RL_NORMAL

    async def _throttle_privmsg(self):
        now = time()
        window_start = now - self.RL_WINDOW
        self._rl_sent_ts = [t for t in self._rl_sent_ts if t >= window_start]

        if len(self._rl_sent_ts) < self._rl_max:
            return

        oldest = self._rl_sent_ts[0]
        sleep_for = (oldest + self.RL_WINDOW) - now
        if sleep_for > 0:
            await asyncio.sleep(sleep_for)

    async def _sender_loop(self):
        try:
            while not self._shutdown and self._ws:
                line = await self._send_q.get()
                if not self._ws:
                    continue

                # throttling doar pentru PRIVMSG (nu pentru PONG)
                if line.startswith("PRIVMSG "):
                    await self._throttle_privmsg()

                async with self._send_lock:
                    await self._ws.send(line)

                if line.startswith("PRIVMSG "):
                    self._rl_sent_ts.append(time())

        except asyncio.CancelledError:
            return

    async def _worker_loop(self):
        try:
            while not self._shutdown:
                tags, message = await self._msg_q.get()
                await asyncio.to_thread(self.handle_pubmsg, tags, message)
        except asyncio.CancelledError:
            return

    async def _ping_watchdog_loop(self):
        try:
            while not self._shutdown and self._ws:
                await asyncio.sleep(self.PING_CHECK_INTERVAL)
                if self._last_ping_time and (time() - self._last_ping_time) > self.PING_TIMEOUT:
                    # forțează reconectare
                    try:
                        await self._ws.close()
                    except Exception:
                        pass
                    return
        except asyncio.CancelledError:
            return

    async def _connect(self):
        ssl_ctx = ssl.create_default_context()

        self._ws = await asyncio.wait_for(
            websockets.connect(
                self.WS_URI,
                ssl=ssl_ctx,
                ping_interval=None,
                    ping_timeout=None,
                close_timeout=5,
                max_queue=self.WS_MAX_QUEUE,
            ),
            timeout=self.CONNECT_TIMEOUT,
        )

        self._joined = False
        self._caps_acked = {"membership": False, "tags": False, "commands": False}
        self._ev_joined.clear()
        self._ev_caps.clear()
        self._last_ping_time = time()
        self._rl_sent_ts.clear()
        self._is_mod_in_channel = False
        self._update_rate_limit()
        self._sent_init = False

        await self._ws_send_now("CAP REQ :twitch.tv/membership")
        await self._ws_send_now("CAP REQ :twitch.tv/tags")
        await self._ws_send_now("CAP REQ :twitch.tv/commands")
        await self._ws_send_now(f"PASS oauth:{self.token}")
        await self._ws_send_now(f"NICK {self.username}")

        if self._sender_task is None or self._sender_task.done():
            self._sender_task = asyncio.create_task(self._sender_loop())

        if self._ping_watchdog_task is None or self._ping_watchdog_task.done():
            self._ping_watchdog_task = asyncio.create_task(self._ping_watchdog_loop())

        if self._worker_task is None or self._worker_task.done():
            self._worker_task = asyncio.create_task(self._worker_loop())

        self._listener_task = asyncio.create_task(self._listen())

    async def _await_ready(self):
        await asyncio.wait_for(
            asyncio.gather(self._ev_caps.wait(), self._ev_joined.wait()),
            timeout=self.READY_TIMEOUT,
        )

    async def _cleanup_connection(self):
        # oprește listener
        if self._listener_task and not self._listener_task.done():
            self._listener_task.cancel()
            await asyncio.gather(self._listener_task, return_exceptions=True)
        self._listener_task = None

        # oprește sender
        if self._sender_task and not self._sender_task.done():
            self._sender_task.cancel()
            await asyncio.gather(self._sender_task, return_exceptions=True)
        self._sender_task = None

        # oprește watchdog
        if self._ping_watchdog_task and not self._ping_watchdog_task.done():
            self._ping_watchdog_task.cancel()
            await asyncio.gather(self._ping_watchdog_task, return_exceptions=True)
        self._ping_watchdog_task = None

        # închide ws
        if self._ws:
            try:
                await self._ws.close()
            except Exception:
                pass
        self._ws = None

        # golește cozi (nu vrem backlog după reconnect)
        if self._send_q is not None:
            try:
                while True:
                    self._send_q.get_nowait()
            except asyncio.QueueEmpty:
                pass

        if self._msg_q is not None:
            try:
                while True:
                    self._msg_q.get_nowait()
            except asyncio.QueueEmpty:
                pass

        self._rl_sent_ts.clear()
        self._joined = False

        if self._ev_joined is not None:
            self._ev_joined.clear()
        if self._ev_caps is not None:
            self._ev_caps.clear()

    async def _listen(self):
        buffer = ""
        async for payload in self._ws:
            buffer += payload

            while "\r\n" in buffer:
                raw, buffer = buffer.split("\r\n", 1)
                if not raw:
                    continue

                msg = self.parse_irc_line(raw)
                cmd = msg["command"]
                tags = msg["tags"]
                prefix = msg["prefix"]
                params = msg["params"]
                trailing = msg["trailing"]

                # PING -> PONG
                if cmd == "PING":
                    self._last_ping_time = time()
                    target = trailing or (params[0] if params else "tmi.twitch.tv")
                    await self._ws_send_now(f"PONG :{target}")
                    continue

                if cmd == "001":
                    if not self._sent_init:
                        self._sent_init = True
                        await self._ws_send_now(f"JOIN {self.channel}")
                    continue

                if cmd == "RECONNECT":
                    return

                if cmd == "CAP" and len(params) >= 2 and params[1] == "ACK":
                    acked = trailing or ""
                    if "twitch.tv/membership" in acked:
                        self._caps_acked["membership"] = True
                    if "twitch.tv/tags" in acked:
                        self._caps_acked["tags"] = True
                    if "twitch.tv/commands" in acked:
                        self._caps_acked["commands"] = True
                    if all(self._caps_acked.values()):
                        self._ev_caps.set()
                    continue

                if cmd == "JOIN":
                    who = (self.nick_from_prefix(prefix) or "").lower()
                    chan = (params[0] if params else "").lower()
                    if who == self.username and chan == self.channel:
                        self._joined = True
                        self._ev_joined.set()
                        print(f"✅ S-a dat join cu succes la {self.channel} POGGERS")
                    continue

                if cmd == "PART":
                    who = (self.nick_from_prefix(prefix) or "").lower()
                    if who == self.username:
                        self._joined = False
                        self._ev_joined.clear()
                        await asyncio.sleep(5)
                        await self._ws_send_now(f"JOIN {self.channel}")
                    continue

                if cmd == "NOTICE":
                    msg_id = tags.get("msg-id", "")
                    text = trailing or ""
                    if msg_id in {"login_authentication_failed", "improperly_formatted_auth"} or "Login authentication failed" in text:
                        # fără spam de loguri; doar oprim
                        self._shutdown = True
                        return
                    continue

                if cmd == "USERSTATE":
                    badges = tags.get("badges", "")
                    self._is_mod_in_channel = (tags.get("mod") == "1") or ("broadcaster/1" in badges)
                    self._update_rate_limit()
                    continue

                if cmd == "ROOMSTATE":
                    continue

                if cmd == "CLEARCHAT":
                    target = (trailing or "").lower()
                    if target == self.username:
                        self._shutdown = True
                        return
                    continue

                if cmd == "PRIVMSG":
                    message = trailing or ""

                    sender = self.nick_from_prefix(prefix) or ""
                    if "display-name" not in tags and sender:
                        tags["display-name"] = sender

                    try:
                        self._msg_q.put_nowait((tags, message))
                    except asyncio.QueueFull:
                        # drop
                        pass

    def start(self):
        asyncio.run(self._run())

    async def _run(self):
        self._loop = asyncio.get_running_loop()
        self._send_lock = asyncio.Lock()
        self._ev_joined = asyncio.Event()
        self._ev_caps = asyncio.Event()
        self._send_q = asyncio.Queue(maxsize=self.SEND_QUEUE_SIZE)
        self._msg_q = asyncio.Queue(maxsize=self.MSG_QUEUE_SIZE)

        for sig in (signal.SIGINT, signal.SIGTERM):
            try:
                self._loop.add_signal_handler(sig, self._handle_shutdown)
            except NotImplementedError:
                pass

        backoff = 1
        while not self._shutdown:
            try:
                await self._connect()
                await self._await_ready()
                await self._listener_task

                backoff = 1
            except (asyncio.TimeoutError, websockets.ConnectionClosed, ConnectionResetError, OSError):
                if self._shutdown:
                    break
            except Exception:
                if self._shutdown:
                    break
            finally:
                await self._cleanup_connection()

            if not self._shutdown:
                await asyncio.sleep(backoff)
                backoff = min(backoff * 2, 60)

        if self._worker_task and not self._worker_task.done():
            self._worker_task.cancel()
            await asyncio.gather(self._worker_task, return_exceptions=True)

    def _handle_shutdown(self):
        self._shutdown = True
        if self._ws:
            try:
                asyncio.create_task(self._ws.close())
            except Exception:
                pass

    # Logica botului
    def handle_pubmsg(self, tags: dict, message: str):
        nrmlzd_msg = self.normalize(message)
        parts = nrmlzd_msg.split()

        user = tags.get("display-name") or tags.get("login") or "unknown"
        is_sub = (tags.get("subscriber") == "1")
        is_mod = (tags.get("mod") == "1") or (user.lower() == vg.owner)

        # Număr la loto
        if len(parts) == 1 and vg.numar_loto is not None:
            try:
                incercare = int(parts[0])
                if incercare == vg.numar_loto:
                    loto_castigat(self, user)
            except Exception:
                pass

        # Adaugă chatter
        if user not in vg.chat and user not in vg.evit:
            vg.chat.append(user)
        if user not in vg.all and user not in vg.evit:
            vg.all.append(user)

        # Blackjack on/off automat
        if vg.bj_off_automat and vg.on_bj and vg.user_blackjack is None:
            off_auto(self)

        m_game = re.search(r"The stream game has been updated to:\s*(.+)$", nrmlzd_msg)
        if m_game:
            game = m_game.group(1).strip()
            if game in self.BJ_OFF_CATEGORIES:
                if vg.on_bj and vg.user_blackjack is None:
                    off_auto(self)
                elif vg.on_bj and vg.user_blackjack is not None:
                    vg.bj_off_automat = True
            else:
                if not vg.on_bj:
                    on_auto(self)

        # Timere
        if time() > vg.timp_ajutor:
            ajutor(self, None, "@chat")

        if time() > vg.timp_puncte:
            puncte_chat(self, vg.chat)

        if vg.user_phf is not None and time() > vg.pedeapsa_phf:
            penalizare_phf(self, vg.user_phf, vg.miza_phf)

        if vg.user_blackjack is not None and time() > vg.pedeapsa_blackjack:
            penalizare_blackjack(self, vg.user_blackjack, vg.miza_blackjack)

        # Mesaj pentru userii noi
        if tags.get("source-room-id") == tags.get("room-id") and tags.get("first-msg") == "1":
            new_user(self, user)

        # Sub / pleb lists
        if is_sub and user not in vg.all_subs and user not in vg.evit:
            if user in vg.all_plebs:
                vg.all_plebs.remove(user)
            vg.all_subs.append(user)
        elif (not is_sub) and user not in vg.all_plebs and user not in vg.evit:
            if user in vg.all_subs:
                vg.all_subs.remove(user)
            vg.all_plebs.append(user)

        # Comenzi globale
        if nrmlzd_msg.startswith("!"):
            cmd = parts[0][1:] if parts else ""

            # PHF în curs
            if vg.user_phf == user and cmd == "joc" and vg.on_phf:
                if len(parts) >= 2:
                    vg.alegere_phf = parts[1]
                phf(self, vg.alegere_phf, vg.user_phf, vg.miza_phf)

            # PHF start
            elif cmd == "joc" and vg.user_phf is None and vg.on_phf:
                vg.user_phf = user
                vg.alegere_phf = parts[1] if len(parts) >= 2 else None
                vg.miza_phf = parts[2] if len(parts) >= 3 else None
                phf(self, vg.alegere_phf, vg.user_phf, vg.miza_phf)

            # BJ în curs
            if vg.user_blackjack == user and cmd == "bj" and vg.on_bj:
                if len(parts) >= 2:
                    vg.alegere_blackjack = parts[1]
                blackjack(self, vg.alegere_blackjack, vg.user_blackjack, vg.miza_blackjack)

            # BJ start
            elif cmd == "bj" and vg.user_blackjack is None and vg.on_bj:
                vg.user_blackjack = user
                vg.alegere_blackjack = parts[1] if len(parts) >= 2 else None
                vg.miza_blackjack = parts[2] if len(parts) >= 3 else None
                blackjack(self, vg.alegere_blackjack, vg.user_blackjack, vg.miza_blackjack)

            # Ruletă
            elif cmd == "ruleta" and tags.get("mod") != "1" and vg.on_ruleta and user != "ㄴㅇㅇㅇㅇㅇㄴ":
                ruleta(self, user, 1 if is_sub else 0)

            # Grinch
            elif cmd == "grinch":
                grinch(self, user, 1 if is_sub else 0)

            # Înscrie botul la Marbles
            elif cmd == "botplay":
                botplay(self)

            # Love
            elif cmd == "love":
                pers2 = " ".join(parts[1:]) if len(parts) >= 2 else None
                love(self, user, pers2)

            # Cuminte
            elif cmd == "cuminte":
                cuminte(self, user)

            # Flower
            elif cmd == "flower":
                flower(self, user)

            # Top flower
            elif cmd in ("topflower", "topflowers", "topfloricele"):
                top_10_flower(self)

            # Video random
            elif cmd == "video":
                video_random(self, user)

            # Puncte user
            elif cmd == "vons":
                alt_user = parts[1] if len(parts) >= 2 else None
                puncte_user(self, user, alt_user)

            # Top Vons
            elif cmd in ("topvon", "topvons"):
                top_10_vons(self)

            # Schimb
            elif cmd == "schimb":
                puncte = parts[1] if len(parts) >= 2 else None
                schimb_puncte(self, user, puncte)

            # Ajutor
            elif cmd == "ajutor":
                alt_user = parts[1] if len(parts) >= 2 else None
                ajutor(self, user, alt_user)

            # Comenzi
            elif cmd == "comenzi":
                alt_user = parts[1] if len(parts) >= 2 else None
                comenzi(self, user, alt_user)

        # Comenzi MODS
        if nrmlzd_msg.startswith("!") and is_mod:
            cmd = parts[0][1:] if parts else ""
            mod = user

            if cmd == "coinflip":
                nume = parts[1] if len(parts) >= 2 else None
                mods_coinflip(self, nume, mod)

            elif cmd == "g":
                categorie = parts[1] if len(parts) >= 2 else None
                mods_schimba_categoria(self, categorie, mod)

            elif cmd == "loto":
                try:
                    _, nr_min, nr_max, premiu = parts[:4]
                    vg.premiu_loto = int(premiu)
                except Exception:
                    nr_min = nr_max = premiu = None
                mods_loto(self, nr_min, nr_max, premiu, mod)

            elif cmd == "puncte":
                try:
                    _, u, nr_puncte = parts[:3]
                    nr_puncte = int(nr_puncte)
                except Exception:
                    u = nr_puncte = None
                mods_puncte(self, mod, u, nr_puncte)

            elif cmd == "on":
                minigame = parts[1] if len(parts) >= 2 else None
                on(self, mod, minigame)

            elif cmd == "off" and vg.user_blackjack is None and vg.user_phf is None:
                minigame = parts[1] if len(parts) >= 2 else None
                off(self, mod, minigame)

            elif cmd in vg.intrebari:
                nume = parts[1] if len(parts) >= 2 else None
                intrebari(self, cmd, nume)

        # Întrebări automate
        low = nrmlzd_msg.lower()
        if ("la ce facultate esti" in low or "ce facultate faci" in low or "ce facultate ai facut" in low or "la ce facultate ai fost" in low):
            intrebari(self, "facultate", user)

        elif ("ce inaltime ai" in low or "care e inaltimea ta" in low or "cat esti de inalta" in low or "cat de inalta esti" in low):
            intrebari(self, "inaltime", user)

        elif ("ce varsta ai" in low or "cati ani ai" in low):
            intrebari(self, "ani", user)

        elif ("cand te-ai apucat de stream" in low or "de cand faci stream" in low or "cand ai inceput sa faci stream" in low or "de cat timp faci stream" in low):
            intrebari(self, "inceput", user)

        elif ("ce zodie esti" in low or "care e zodia ta" in low):
            intrebari(self, "zodie", user)

        elif (
            "ce job ai" in low or "care este jobul tau" in low or "care este job-ul tau" in low
            or "care e jobul tau" in low or "care e job-ul tau" in low
            or "cu ce te ocupi" in low or "ce muncesti" in low or "ce lucrezi" in low
            or "unde muncesti" in low or "unde lucrezi" in low
        ):
            intrebari(self, "job", user)

        return