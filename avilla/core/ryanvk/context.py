from __future__ import annotations

from contextvars import ContextVar
from typing import TYPE_CHECKING

from .common.isolate import Isolate

if TYPE_CHECKING:
    from ..protocol import BaseProtocol

processing_protocol: ContextVar[type[BaseProtocol]] = ContextVar("processing_protocol")
processing_isolate: ContextVar[Isolate] = ContextVar("processing_isolate")