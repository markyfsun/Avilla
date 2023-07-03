from __future__ import annotations

from typing import TYPE_CHECKING, Awaitable, Callable, TypeVar

from avilla.core._vendor.dataclasses import dataclass

if TYPE_CHECKING:
    from avilla.core.event import AvillaEvent
    from avilla.core.ryanvk.collector.account import (
        AccountBasedPerformTemplate,
        AccountCollector,
    )

PBPT = TypeVar("PBPT", bound="AccountBasedPerformTemplate", contravariant=True)


@dataclass(unsafe_hash=True)
class EventParserSign:
    event_type: str


class OneBot11EventParse:
    @classmethod
    def collect(cls, collector: AccountCollector, event_type: str):
        def receiver(entity: Callable[[PBPT, dict], Awaitable[AvillaEvent]]):
            collector.artifacts[EventParserSign(event_type)] = (collector, entity)
            return entity

        return receiver