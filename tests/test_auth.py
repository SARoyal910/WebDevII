# tests/test_auth.py
import pytest
from httpx import AsyncClient, ASGITransport
from asgi_lifespan import LifespanManager
from fastapi import status
from backend.main import app   # important: import the routed app

@pytest.mark.asyncio
async def test_signup_and_me():
    async with LifespanManager(app):  # ensures startup/shutdown runs
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            r = await ac.post(
                "/api/auth/signup",
                data={"email": "a@b.com", "password": "pass123", "password_confirmation": "pass123"},
            )
            assert r.status_code == status.HTTP_201_CREATED
            assert "csrf" in r.json()
            assert any(c.startswith("sid=") for c in r.headers.get_list("set-cookie"))

            r2 = await ac.get("/api/auth/me")
            assert r2.status_code == 200
            assert r2.json()["email"] == "a@b.com"

@pytest.mark.asyncio
async def test_login_logout_flow():
    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        # create user
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            await ac.post(
                "/api/auth/signup",
                data={"email": "c@d.com", "password": "pass123", "password_confirmation": "pass123"},
            )

        # new client → login
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac2:
            r = await ac2.post("/api/auth/login", data={"email": "c@d.com", "password": "pass123"})
            assert r.status_code == 200
            csrf = r.json()["csrf"]

            r2 = await ac2.post(
                "/api/auth/change-password",
                data={"old_password": "pass123", "new_password": "newpass"},
                headers={"X-CSRF-Token": csrf},
            )
            assert r2.status_code == 200

            r3 = await ac2.post("/api/auth/logout")
            assert r3.status_code == 200

            r4 = await ac2.get("/api/auth/me")
            assert r4.status_code in (401, 303)

@pytest.mark.asyncio
async def test_admin_protected():
    async with LifespanManager(app):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            await ac.post(
                "/api/auth/signup",
                data={"email": "e@f.com", "password": "pass123", "password_confirmation": "pass123"},
            )
            r = await ac.get("/api/admin/stats")
            assert r.status_code in (401, 403)

@pytest.mark.asyncio
async def test_csrf_missing_is_rejected():
    async with LifespanManager(app):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            await ac.post(
                "/api/auth/signup",
                data={"email": "x@y.com", "password": "pass123", "password_confirmation": "pass123"},
            )
            r = await ac.post(
                "/api/auth/change-password",
                data={"old_password": "pass123", "new_password": "pass456"},
            )
            assert r.status_code == 400
            assert "csrf" in r.text.lower()



