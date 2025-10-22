# backend/session.py
import secrets
from types import SimpleNamespace
from typing import Optional, Dict, Any


class InMemoryKV:
    """
    Super-simple async key-value store used for sessions during tests/dev.
    Stores each session id ('sid') as a dict with keys like: 'data', 'csrf'.
    """
    def __init__(self) -> None:
        self._store: Dict[str, Dict[str, Any]] = {}

    async def get(self, key: str) -> Optional[Dict[str, Any]]:
        return self._store.get(key)

    async def set(self, key: str, value: Dict[str, Any]) -> None:
        self._store[key] = value

    async def delete(self, key: str) -> None:
        self._store.pop(key, None)


class Session:
    """
    Minimal session wrapper:
    - Cookie 'sid' identifies a record in KV storage.
    - `data` is a SimpleNamespace you can put fields on (e.g., user_id).
    - CSRF token is stored and verified per session.
    """
    COOKIE_NAME = "sid"

    def __init__(self, request, response, storage: InMemoryKV) -> None:
        self.request = request
        self.response = response
        self.storage = storage
        self.sid: Optional[str] = None
        self.data: SimpleNamespace = SimpleNamespace()
        self._csrf: Optional[str] = None
        self._loaded: bool = False
        self._new_sid: bool = False

    async def load(self) -> None:
        if self._loaded:
            return

        sid = self.request.cookies.get(self.COOKIE_NAME)
        if not sid:
            # create new session id, set cookie on response
            sid = secrets.token_urlsafe(32)
            self._new_sid = True
            # Set cookie; tests only check for presence of "sid=" in Set-Cookie
            self.response.set_cookie(
                key=self.COOKIE_NAME,
                value=sid,
                httponly=True,
                samesite="lax",
                secure=False,
                path="/",
            )

        self.sid = sid
        raw = await self.storage.get(sid) or {}
        self._csrf = raw.get("csrf")
        self.data = SimpleNamespace(**(raw.get("data") or {}))
        self._loaded = True

    async def commit(self) -> None:
        if not self.sid:
            # Shouldn't happen if load() was called
            return
        payload = {
            "data": self.data.__dict__,
            "csrf": self._csrf,
        }
        await self.storage.set(self.sid, payload)

    async def clear(self) -> None:
        if self.sid:
            await self.storage.delete(self.sid)
        # Overwrite cookie as expired (good hygiene, not strictly required by tests)
        self.response.delete_cookie(self.COOKIE_NAME)
        self.sid = None
        self.data = SimpleNamespace()
        self._csrf = None
        self._loaded = False
        self._new_sid = False

    async def rotate_csrf_token(self) -> str:
        self._csrf = secrets.token_urlsafe(32)
        return self._csrf

    def verify_csrf_token(self, token: Optional[str]) -> bool:
        return bool(token) and token == self._csrf

    def get_csrf_token(self) -> Optional[str]:
        return self._csrf

