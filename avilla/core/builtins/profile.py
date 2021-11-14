from typing import Optional

from pydantic import BaseModel

from avilla.core.contactable import Contactable
from avilla.core.role import Role

from ..profile import BaseProfile


class SelfProfile(BaseModel, BaseProfile):
    "self 只需要有 id(entity) 就可以了, 其他的请自行 fetchdata."
    name: Optional[str] = None


class StrangerProfile(BaseModel, BaseProfile):
    name: str
    age: Optional[int] = None


class FriendProfile(BaseModel, BaseProfile):
    name: str
    remark: str


class GroupProfile(BaseModel, BaseProfile):
    name: Optional[str] = None
    counts: Optional[int] = None
    limit: Optional[int] = None


class MemberProfile(BaseModel, BaseProfile):
    name: Optional[str] = None
    group: Optional[Contactable[GroupProfile]] = None
    role: Optional[Role] = None
    nickname: Optional[str] = None
    title: Optional[str] = None