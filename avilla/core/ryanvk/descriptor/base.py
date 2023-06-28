from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Mapping, Protocol, TypeVar

from typing_extensions import Concatenate, ParamSpec

from ..common.fn import BaseFn, FnImplement

if TYPE_CHECKING:
    from ...context import Context
    from ..collector import AvillaPerformTemplate, Collector
    from ..common.capability import Capability


P = ParamSpec("P")
R = TypeVar("R", covariant=True)
R1 = TypeVar("R1", covariant=True)
C = TypeVar("C", bound="Capability")
H = TypeVar("H", bound="AvillaPerformTemplate")


class Fn(BaseFn["Collector", P, R]):
    def __init__(self, template: Callable[Concatenate[C, P], R]) -> None:
        self.template = template  # type: ignore

    def collect(self, collector: Collector):
        def receive(entity: Callable[Concatenate[H, P], R]):
            collector.artifacts[FnImplement(self.capability, self.name)] = (collector, entity)
            return entity

        return receive

    def get_collect_signature(self):
        return FnImplement(self.capability, self.name)

    def get_execute_signature(self, runner: Context, *args: P.args, **kwargs: P.kwargs) -> Any:
        return FnImplement(self.capability, self.name)

    class _InferProtocol(Protocol[R1]):
        def get_execute_signature(self, runner: Context, *args, **kwargs) -> R1:
            ...

    def get_execute_layout(
        self: _InferProtocol[R1], runner: Context, *args: P.args, **kwargs: P.kwargs
    ) -> Mapping[R1, tuple[Collector, Callable[Concatenate[AvillaPerformTemplate, P], R]]]:
        return runner.artifacts

    def execute(self, runner: Context, *args: P.args, **kwargs: P.kwargs) -> R:
        collector, entity = self.get_execute_layout(runner, *args, **kwargs)[
            self.get_execute_signature(runner, *args, **kwargs)
        ]
        instance = collector.cls(runner)
        return entity(instance, *args, **kwargs)
