"""Data models for portfolio positions and snapshots."""

from dataclasses import dataclass, field


@dataclass
class Position:
    ticker: str
    description: str
    units: float
    price: float
    average_cost: float
    unrealized_pnl: float
    currency: str = "CAD"
    exchange: str = ""
    security_type: str = ""  # crypto, equity, etf
    cash_equivalent: bool = False

    @property
    def market_value(self) -> float:
        return self.units * self.price

    @property
    def cost_basis(self) -> float:
        return self.units * self.average_cost

    @property
    def return_pct(self) -> float:
        if self.average_cost == 0:
            return 0.0
        return ((self.price - self.average_cost) / self.average_cost) * 100


@dataclass
class PortfolioSnapshot:
    date: str
    positions: list[Position] = field(default_factory=list)
    cash: float = 0.0

    @property
    def total_value(self) -> float:
        return sum(p.market_value for p in self.positions) + self.cash

    @property
    def total_cost_basis(self) -> float:
        return sum(p.cost_basis for p in self.positions)

    @property
    def total_unrealized_pnl(self) -> float:
        return sum(p.unrealized_pnl for p in self.positions)

    @property
    def position_count(self) -> int:
        return len([p for p in self.positions if not p.cash_equivalent])

    def top_holdings(self, n: int = 10) -> list[Position]:
        return sorted(self.positions, key=lambda p: p.market_value, reverse=True)[:n]

    TYPE_LABELS = {"cs": "Equity", "et": "ETF", "crypto": "Crypto", "ad": "ADRs/Other"}

    def allocation_by_type(self) -> dict[str, float]:
        total = self.total_value or 1
        result: dict[str, float] = {}
        for p in self.positions:
            key = self.TYPE_LABELS.get(p.security_type, p.security_type or "Other")
            result[key] = result.get(key, 0) + p.market_value
        return {k: round(v / total * 100, 1) for k, v in result.items()}

    def allocation_by_geography(self) -> dict[str, float]:
        total = self.total_value or 1
        result: dict[str, float] = {}
        for p in self.positions:
            if ".TO" in p.ticker or ".VN" in p.ticker or ".NE" in p.ticker:
                key = "Canada"
            elif p.security_type == "crypto":
                key = "Crypto"
            else:
                key = "US"
            result[key] = result.get(key, 0) + p.market_value
        return {k: round(v / total * 100, 1) for k, v in result.items()}
