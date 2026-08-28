"""CISA Known Exploited Vulnerabilities feed — cache & parsing logic."""

import logging
from datetime import datetime, timezone

import requests
from fastapi import HTTPException, status

logger = logging.getLogger("uvicorn.error")

_CISA_URL = (
    "https://www.cisa.gov/sites/default/files/feeds/"
    "known_exploited_vulnerabilities.json"
)
_CACHE_TTL = 120  # seconds


def _parse_cisa_feed(data: dict, url: str, now: float) -> dict:
    vulnerabilities = (
        data.get("vulnerabilities", []) if isinstance(data, dict) else []
    )
    vulnerabilities = sorted(
        [v for v in vulnerabilities if isinstance(v, dict)],
        key=lambda v: (v.get("dateAdded") or "", v.get("cveID") or ""),
        reverse=True,
    )
    items = [
        {
            "cveID": vuln.get("cveID", ""),
            "vendorProject": vuln.get("vendorProject", ""),
            "product": vuln.get("product", ""),
            "vulnerabilityName": vuln.get("vulnerabilityName", ""),
            "dateAdded": vuln.get("dateAdded", ""),
            "shortDescription": vuln.get("shortDescription", ""),
            "requiredAction": vuln.get("requiredAction", ""),
            "dueDate": vuln.get("dueDate", ""),
        }
        for vuln in vulnerabilities[:12]
    ]
    return {
        "catalogVersion": data.get("catalogVersion", ""),
        "dateReleased": data.get("dateReleased", ""),
        "count": data.get("count", len(vulnerabilities)),
        "sourceUrl": url,
        "items": items,
        "updatedAt": now,
        "stale": False,
    }


def get_veille_payload(app_state: object, limit: int = 8) -> dict:
    """Return CISA KEV feed, using in-memory cache when fresh."""
    limit = max(1, min(limit, 12))
    now = datetime.now(timezone.utc).timestamp()

    cached = getattr(app_state, "veille_cache", None)
    if cached and now < cached.get("expires_at", 0):
        result = dict(cached["payload"])
        result["items"] = result.get("items", [])[:limit]
        return result

    try:
        response = requests.get(
            _CISA_URL,
            timeout=20,
            headers={"Accept": "application/json"},
        )
        response.raise_for_status()
        payload = _parse_cisa_feed(response.json(), _CISA_URL, now)
        app_state.veille_cache = {
            "payload": payload,
            "expires_at": now + _CACHE_TTL,
        }
        result = dict(payload)
        result["items"] = payload["items"][:limit]
        return result
    except Exception as exc:
        logger.exception("Échec de récupération de la veille CISA: %s", exc)
        cached = getattr(app_state, "veille_cache", None)
        if cached:
            stale = dict(cached["payload"])
            stale["items"] = stale.get("items", [])[:limit]
            stale["stale"] = True
            return stale
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=(
                "Impossible de récupérer la veille automatique pour le moment."
            ),
        ) from exc
