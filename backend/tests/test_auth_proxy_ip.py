from types import SimpleNamespace

from app.auth import get_client_ip


def test_get_client_ip_prefers_forwarded_for_header():
    request = SimpleNamespace(
        headers={"x-forwarded-for": "203.0.113.7, 10.0.0.4"},
        client=SimpleNamespace(host="192.168.1.5"),
    )

    assert get_client_ip(request) == "203.0.113.7"


def test_get_client_ip_falls_back_to_real_ip_header():
    request = SimpleNamespace(
        headers={"x-real-ip": "198.51.100.9"},
        client=SimpleNamespace(host="192.168.1.5"),
    )

    assert get_client_ip(request) == "198.51.100.9"
