from dataclasses import asdict
from dataclasses import dataclass


@dataclass(slots=True)
class BaseModel:
    """
    Base class for all PylonInsight domain objects.
    """

    def to_dict(self) -> dict:
        return asdict(self)