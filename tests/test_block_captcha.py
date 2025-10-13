import sys
import types

import pytest
from fastapi.testclient import TestClient


class _FakeRedis:
    """Minimal async Redis replacement for counting attempts in tests."""

    def __init__(self):
        self._store: dict[str, int] = {}
        self.expirations: dict[str, int] = {}

    async def incr(self, key: str) -> int:
        self._store[key] = self._store.get(key, 0) + 1
        return self._store[key]

    async def expire(self, key: str, seconds: int):
        self.expirations[key] = seconds
        return True

    async def get(self, key: str):
        value = self._store.get(key)
        return None if value is None else str(value)

    async def delete(self, key: str):
        self._store.pop(key, None)
        return True

    async def close(self):
        return True


if "redis.asyncio" not in sys.modules:
    fake_asyncio_module = types.ModuleType("redis.asyncio")
    fake_asyncio_module.from_url = lambda *args, **kwargs: _FakeRedis()
    sys.modules["redis.asyncio"] = fake_asyncio_module

    fake_redis_root = types.ModuleType("redis")
    fake_redis_root.asyncio = fake_asyncio_module
    sys.modules.setdefault("redis", fake_redis_root)


from flaskr.tools.fast_api import block_captch_5_errors_in_minit as captcha_module


@pytest.fixture(autouse=True)
def fake_redis(monkeypatch):
    original = captcha_module.r
    fake = _FakeRedis()
    monkeypatch.setattr(captcha_module, "r", fake)
    try:
        yield fake
    finally:
        captcha_module.r = original


@pytest.fixture
def fastapi_client():
    return TestClient(captcha_module.app)


def test_five_failed_attempts_return_remaining_count(fastapi_client):
    for attempt in range(1, captcha_module.MAX_FAILED_ATTEMPTS + 1):
        response = fastapi_client.post(
            "/login",
            data={"username": "alice", "password": "wrong"},
        )
        assert response.status_code == 401
        body = response.json()
        expected_remaining = captcha_module.MAX_FAILED_ATTEMPTS - attempt
        assert body["remaining_attempts"] == expected_remaining
        assert body["blocked_after"] == captcha_module.BLOCK_WINDOW_SECONDS


def test_sixth_failed_attempt_is_blocked(fastapi_client):
    for _ in range(captcha_module.MAX_FAILED_ATTEMPTS):
        fastapi_client.post(
            "/login",
            data={"username": "alice", "password": "wrong"},
        )

    blocked_response = fastapi_client.post(
        "/login",
        data={"username": "alice", "password": "wrong"},
    )

    assert blocked_response.status_code == 429
    assert "Too many failed attempts" in blocked_response.json()["detail"]
