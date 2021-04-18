from pydantic import BaseModel
from pydantic import Field
from typing import List
from typing import Optional
from typing import Type

def update_forward_refs(cls: Type[BaseModel]) -> Type[BaseModel]:
    cls.update_forward_refs()

    return cls


class SendMessage(BaseModel):
    chat_id: int = Field(...)
    text: str = Field(...)

class Chat(BaseModel):
    id: int  # noqa: A003
    type: str  # noqa: A003


class User(BaseModel):
    id: int  # noqa: A003
    is_bot: bool
    first_name: str
    last_name: Optional[str] = Field(None)
    username: Optional[str] = Field(None)

class File(BaseModel):
    file_id: str
    file_unique_id: str
    file_size: Optional[int] = Field(None)
    file_path: Optional[int] = Field(None)

class PhotoSize(File):
    file_id: str
    file_unique_id: str
    width: int
    height: str
    file_size: Optional[int] = Field(None)

@update_forward_refs
class Message(BaseModel):
    message_id: int
    chat: Chat
    date: int
    text: Optional[str] = Field(None, min_length=0, max_length=2 ** 12)
    from_: Optional[User] = Field(None)
    reply_to_message: Optional["Message"] = Field(None)
    photo: List[PhotoSize] = Field(default_factory=list)

    class Config:
        fields = {
            "from_": "from",
        }


class Update(BaseModel):
    update_id: int
    message: Message

class setWebHook(BaseModel):
    url: str
    url_telega: str

class Baseuser(BaseModel):
    id: int
    user_id: int
    blog_user_id: Optional[int] = Field(None)
    blog_user_name: Optional[str] = Field(None)
    user_status: Optional[int] = Field(None)

