from abc import ABCMeta, abstractmethod, abstractproperty
from contextlib import AsyncExitStack
from typing import TYPE_CHECKING, Any, Generic

from avilla.core.builtins.profile import SelfProfile
from avilla.core.contactable import Contactable, ref
from avilla.core.launch import LaunchComponent
from avilla.core.message.chain import MessageChain
from avilla.core.platform import Platform
from avilla.core.relationship import Relationship
from avilla.core.typing import T_Config, T_ExecMW, T_Profile

from .execution import Execution

if TYPE_CHECKING:
    from . import Avilla


class BaseProtocol(Generic[T_Config], metaclass=ABCMeta):
    avilla: "Avilla"
    config: T_Config

    platform: Platform = Platform(
        name="Avilla Universal Protocol Implementation",
        protocol_provider_name="Avilla Protocol",
        implementation="avilla-core",
        supported_impl_version="$any",
        generation="1",
    )

    def __init__(self, avilla: "Avilla", config: T_Config) -> None:
        self.avilla = avilla
        self.config = config
        self.using_networks, self.using_exec_method = self.ensure_networks()
        self.__post_init__()

    @abstractmethod
    def ensure_networks(self):
        raise NotImplementedError

    def __post_init__(self) -> None:
        pass

    def ensure_execution(self, execution: "Execution") -> Any:
        raise NotImplementedError

    @abstractmethod
    def get_self(self) -> "Contactable[SelfProfile]":
        raise NotImplementedError

    @abstractmethod
    async def parse_message(self, data: Any) -> "MessageChain":
        raise NotImplementedError

    @abstractmethod
    async def serialize_message(self, message: "MessageChain") -> Any:
        raise NotImplementedError

    @abstractmethod
    async def get_relationship(self, entity: "Contactable[T_Profile]") -> "Relationship[T_Profile]":
        return Relationship(entity, self, middlewares=self.avilla.middlewares)

    @abstractmethod
    async def launch_mainline(self):
        """LaunchComponent.task"""

    async def launch_prepare(self):
        """LaunchComponent.prepare"""

    async def launch_cleanup(self):
        """LaunchComponent.cleanup"""

    @abstractproperty
    def launch_component(self) -> LaunchComponent:
        ...

    def has_ability(self, ability: str) -> bool:
        raise NotImplementedError

    async def exec_directly(self, execution: Execution, *middlewares: T_ExecMW) -> Any:
        async with AsyncExitStack() as exit_stack:
            for middleware in middlewares:
                await exit_stack.enter_async_context(middleware(self, execution))  # type: ignore
            return await self.ensure_execution(execution)

    def check_refpath(self, refpath: ref) -> None:
        pass