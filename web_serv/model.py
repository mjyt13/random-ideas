from typing import Dict

from pydantic import BaseModel
from datetime import datetime


# Класс, который описывает структуру ответа сервера для метода,
# который подсчитывает символы в строке.
# Данный класс обязательно должен быть наследован от pydantic.BaseModel!
class CountLettersResponse(BaseModel):
    counted_at: datetime
    counters: Dict[str, int]
