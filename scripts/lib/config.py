"""Configuration for SnapTrade API access."""

from dataclasses import dataclass


@dataclass
class SnapTradeConfig:
    client_id: str
    consumer_key: str
    user_id: str
    user_secret: str
