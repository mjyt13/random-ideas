from pydantic import BaseModel
from datetime import datetime
from typing import List
""" Модели со структурой ответов сервера"""


# ответ на запрос на создание заметки
class NoteCreate(BaseModel):
    text: str

# ответ как ID созданной заметки
class NoteID(BaseModel):
    id: int

# ответ на запрос о получении информации
# время создания и последнего изменения
class NoteInfo(BaseModel):
    created_at: datetime
    updated_at: datetime

# ответ на запрос прочтения заметки
class NoteText(BaseModel):
    id: int
    text: str

# ответ на запрос получения ID всех заметок
class NoteList(BaseModel):
    notes: List[int]

class TokenList(BaseModel):
    tokens: List[str]
