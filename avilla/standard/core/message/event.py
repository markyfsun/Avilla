from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from avilla.core._vendor.graia.amnesia.message import MessageChain
from avilla.core.event import AvillaEvent

if TYPE_CHECKING:
    from graia.broadcast.interfaces.dispatcher import DispatcherInterface

    from avilla.core.account import BaseAccount
    from avilla.core.message import Message
    from avilla.core.selector import Selector


@dataclass
class MessageReceived(AvillaEvent):
    message: Message

    class Dispatcher(AvillaEvent.Dispatcher):
        @classmethod
        async def catch(cls, interface: DispatcherInterface[MessageReceived]):
            if interface.annotation is interface.event.message.__class__:
                return interface.event.message
            elif interface.annotation is MessageChain:
                return interface.event.message.content
            return await super().catch(interface)


@dataclass
class MessageSent(AvillaEvent):
    message: Message
    account: BaseAccount

    class Dispatcher(AvillaEvent.Dispatcher):
        @classmethod
        async def catch(cls, interface: DispatcherInterface[MessageReceived]):
            if interface.annotation is interface.event.message.__class__:
                return interface.event.message
            elif interface.annotation is MessageChain:
                return interface.event.message.content
            return await super().catch(interface)


@dataclass
class MessageEdited(AvillaEvent):
    message: Message
    operator: Selector
    past: MessageChain
    current: MessageChain

    class Dispatcher(AvillaEvent.Dispatcher):
        @classmethod
        async def catch(cls, interface: DispatcherInterface[MessageEdited]):
            if interface.annotation is Message:
                return interface.event.message
            elif interface.annotation is MessageChain:
                return interface.event.current
            return await super().catch(interface)


@dataclass
class MessageRevoked(AvillaEvent):
    message: Selector
    operator: Selector
    sender: Selector | None = None

    class Dispatcher(AvillaEvent.Dispatcher):
        @classmethod
        async def catch(cls, interface: DispatcherInterface[MessageRevoked]):
            return await super().catch(interface)
