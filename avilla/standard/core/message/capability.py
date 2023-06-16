from __future__ import annotations

from graia.amnesia.message import MessageChain

from avilla.core.ryanvk import Capability, Fn, TargetFn
from avilla.core.selector import Selector

# MessageFetch => rs.pull(Message, target=...)


class MessageSend(Capability):
    @TargetFn
    async def send(self, message: MessageChain, *, reply: Selector | None = None) -> Selector:
        ...


class MessageRevoke(Capability):
    @TargetFn
    async def revoke(self) -> None:
        ...


class MessageEdit(Capability):
    @Fn
    async def edit(self, content: MessageChain) -> None:
        ...