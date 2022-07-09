from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

from avilla.core.platform import Land
from avilla.core.relationship import Relationship
from avilla.core.utilles.selector import Selector

if TYPE_CHECKING:
    from avilla.core.protocol import BaseProtocol


@dataclass
class AbstractAccount(ABC):
    id: str
    land: Land
    protocol: BaseProtocol

    @abstractmethod
    async def get_relationship(self, target: Selector) -> Relationship:
        ...

    def get_self_relationship(self):
        return Relationship(
            self.protocol, self.to_selector(), Selector().land(self.land.name), Selector().account(self.id)
        )

    @property
    def available(self) -> bool:
        return True

    def to_selector(self) -> Selector:
        return Selector().land(self.land.name).account(self.id)

    def is_anonymous(self) -> bool:
        return self.id == "anonymous"


AccountSelector = Selector[Literal["land.account"]]