from __future__ import annotations

from typing import Any

import requests


API_BASE_URL = "http://127.0.0.1:8000"
REQUEST_TIMEOUT_SECONDS = 10


class APIError(RuntimeError):
    """Raised when the FastAPI backend cannot return usable data."""


def fetch_json(endpoint: str) -> Any:
    """Fetch JSON data from the FastAPI backend."""
    url = f"{API_BASE_URL}{endpoint}"

    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT_SECONDS)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        raise APIError(
            "FastAPI backend is unavailable. Start it and refresh this page."
        ) from exc


def get_health() -> dict[str, str]:
    """Return API health status."""
    return fetch_json("/health")


def get_trips(limit: int = 20) -> list[dict[str, Any]]:
    """Return processed trips from the API."""
    return fetch_json(f"/trips?limit={limit}")


def get_trips_per_day() -> list[dict[str, Any]]:
    """Return daily trip counts."""
    return fetch_json("/analytics/trips-per-day")


def get_trips_by_vendor() -> list[dict[str, Any]]:
    """Return trip counts by vendor."""
    return fetch_json("/analytics/trips-by-vendor")


def get_trips_by_payment_type() -> list[dict[str, Any]]:
    """Return trip counts by payment type."""
    return fetch_json("/analytics/trips-by-payment-type")


def get_hourly_demand() -> list[dict[str, Any]]:
    """Return trip counts by pickup hour."""
    return fetch_json("/analytics/hourly-demand")


def get_top_pickup_locations() -> list[dict[str, Any]]:
    """Return top pickup locations."""
    return fetch_json("/analytics/top-pickup-locations")


def get_top_dropoff_locations() -> list[dict[str, Any]]:
    """Return top dropoff locations."""
    return fetch_json("/analytics/top-dropoff-locations")
