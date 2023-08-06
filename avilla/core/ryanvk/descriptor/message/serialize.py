from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Awaitable, Callable, Generic, TypeVar

if TYPE_CHECKING:
    from avilla.core._vendor.graia.amnesia.message.element import Element
    from avilla.core.ryanvk.collector.account import (
        AccountBasedPerformTemplate,
        AccountCollector,
    )

PBPT = TypeVar("PBPT", bound="AccountBasedPerformTemplate", contravariant=True)
E = TypeVar("E", bound="Element")
T = TypeVar("T")


@dataclass(unsafe_hash=True)
class MessageSerializeSign(Generic[E]):
    element_type: type[Element]


class MessageSerialize(Generic[T]):
    @classmethod
    def collect(cls: type[MessageSerialize[T]], collector: AccountCollector, element_type: type[E]):
        def receiver(entity: Callable[[PBPT, E], Awaitable[T]]) -> Callable[[PBPT, E], Awaitable[T]]:
            collector.artifacts[MessageSerializeSign(element_type)] = (collector, entity)
            return entity

        return receiver
