from pydantic import BaseModel


class ExchangeDTO(BaseModel):
    id: str
    name: str


class SymbolDTO(BaseModel):
    id: str
    market: str
    base: str
    quote: str
    settle: str | None = None


class OrderbookDTO(BaseModel):
    symbol: SymbolDTO
    exchange: ExchangeDTO
    timestamp: float | int
    asks: list[list[float | int]]
    bids: list[list[float | int]]
