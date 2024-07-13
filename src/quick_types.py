from typing import Optional, List, Any
from datetime import datetime
from uuid import UUID


class Update:
    type: str
    status: Optional[str]
    title: Optional[str]
    text: Optional[str]
    interrupted: Optional[bool]

    def __init__(self, type: str, status: Optional[str], title: Optional[str], text: Optional[str], interrupted: Optional[bool]) -> None:
        self.type = type
        self.status = status
        self.title = title
        self.text = text
        self.interrupted = interrupted


class Message:
    message_from: str
    content: str
    created_at: datetime
    updated_at: datetime
    ancestors: List[UUID]
    id: UUID
    children: List[UUID]
    updates: Optional[List[Update]]
    interrupted: Optional[bool]
    files: Optional[List[Any]]

    def __init__(self, message_from: str, content: str, created_at: datetime, updated_at: datetime, ancestors: List[UUID], id: UUID, children: List[UUID], updates: Optional[List[Update]], interrupted: Optional[bool], files: Optional[List[Any]]) -> None:
        self.message_from = message_from
        self.content = content
        self.created_at = created_at
        self.updated_at = updated_at
        self.ancestors = ancestors
        self.id = id
        self.children = children
        self.updates = updates
        self.interrupted = interrupted
        self.files = files


class Parameters:
    temperature: float
    truncate: int
    max_new_tokens: int
    stop: List[str]
    top_p: float
    stop_sequences: List[str]
    return_full_text: bool

    def __init__(self, temperature: float, truncate: int, max_new_tokens: int, stop: List[str], top_p: float, stop_sequences: List[str], return_full_text: bool) -> None:
        self.temperature = temperature
        self.truncate = truncate
        self.max_new_tokens = max_new_tokens
        self.stop = stop
        self.top_p = top_p
        self.stop_sequences = stop_sequences
        self.return_full_text = return_full_text


class Escalate2X:
    note: str
    prompt: str
    model: str
    parameters: Parameters
    user_message: Message
    assistant_message: Message

    def __init__(self, note: str, prompt: str, model: str, parameters: Parameters, user_message: Message, assistant_message: Message) -> None:
        self.note = note
        self.prompt = prompt
        self.model = model
        self.parameters = parameters
        self.user_message = user_message
        self.assistant_message = assistant_message
