from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar, Generic, TypeVar, cast

from typing_extensions import Unpack

from avilla.core.ryanvk.capability import CoreCapability

from .common.collect import BaseCollector
from .context import processing_isolate, processing_protocol

if TYPE_CHECKING:
    from ..account import AbstractAccount
    from ..context import Context
    from ..metadata import Metadata, MetadataRoute
    from ..protocol import BaseProtocol
    from ..selector import FollowsPredicater
    from .fn import PullFn


TProtocol = TypeVar("TProtocol", bound="BaseProtocol")
TAccount = TypeVar("TAccount", bound="AbstractAccount")

TProtocol1 = TypeVar("TProtocol1", bound="BaseProtocol")
TAccount1 = TypeVar("TAccount1", bound="AbstractAccount")

T = TypeVar("T")
T1 = TypeVar("T1")
M = TypeVar("M", bound="Metadata")


class AvillaPerformTemplate:
    __collector__: ClassVar[BaseCollector]

    context: Context
    protocol: BaseProtocol
    account: AbstractAccount

    def __init__(self, context: Context):
        self.context = context
        self.protocol = context.protocol
        self.account = context.account


class Collector(BaseCollector):
    post_applying: bool = False

    def __init__(self):
        super().__init__()
        self.artifacts["lookup"] = {}

    @property
    def _(self):
        class perform_template(AvillaPerformTemplate, self._base_ring3()):
            __native__ = True

        return perform_template

    def pull(
        self, target: str, route: type[M] | MetadataRoute[Unpack[tuple[Any, ...]], M], **patterns: FollowsPredicater
    ):
        return self.entity(cast("PullFn[M]", CoreCapability.pull), (target, patterns), route)

    def fetch(self, resource_type: type[T]):  # type: ignore[reportInvalidTypeVarUse]
        return self.entity(CoreCapability.fetch.into(resource_type), resource_type)

    def __post_collect__(self, cls: type[AvillaPerformTemplate]):
        super().__post_collect__(cls)
        if self.post_applying:
            if (isolate := processing_isolate.get(None)) is not None:
                isolate.apply(cls)


class ProtocolCollector(Generic[TProtocol, TAccount], Collector):
    def __init__(self):
        super().__init__()

    @property
    def _(self):
        class perform_template(super()._, Generic[TProtocol1, TAccount1]):
            __native__ = True

            context: Context
            protocol: TProtocol1
            account: TAccount1

        return perform_template[TProtocol, TAccount]

    def __post_collect__(self, cls: type[AvillaPerformTemplate]):
        super().__post_collect__(cls)
        if self.post_applying:
            if (protocol := processing_protocol.get(None)) is None:
                raise RuntimeError("expected processing protocol")
            protocol.isolate.apply(cls)