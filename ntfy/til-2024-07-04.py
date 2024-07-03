from enum import Enum
from typing import Optional, List


class Attachment:
    name: str
    type: str
    size: int
    expires: int
    url: str

    def __init__(self, name: str, type: str, size: int, expires: int, url: str) -> None:
        self.name = name
        self.type = type
        self.size = size
        self.expires = expires
        self.url = url


class Event(Enum):
    MESSAGE = "message"


class Topic(Enum):
    KICK = "kick"


class NtfyMessageElement:
    id: str
    time: int
    expires: int
    event: Event
    topic: Topic
    title: Optional[str]
    message: str
    click: Optional[str]
    priority: Optional[int]
    content_type: Optional[str]
    tags: Optional[List[str]]
    attachment: Optional[Attachment]

    def __init__(self, id: str, time: int, expires: int, event: Event, topic: Topic, title: Optional[str], message: str, click: Optional[str], priority: Optional[int], content_type: Optional[str], tags: Optional[List[str]], attachment: Optional[Attachment]) -> None:
        self.id = id
        self.time = time
        self.expires = expires
        self.event = event
        self.topic = topic
        self.title = title
        self.message = message
        self.click = click
        self.priority = priority
        self.content_type = content_type
        self.tags = tags
        self.attachment = attachment
