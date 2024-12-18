import datetime
import fastapi

from model import CountLettersResponse

api_router = fastapi.APIRouter()


# Обрати внимание на @api_router.get <- get - тип HTTP метода!
# Для того, чтобы создать put метод, необходимо написать @api_router.put
# /sum - url относительно сервера, по которму будет доступен метод.
# Обрати внимание на response_model <- описывает схему ответа сервера.
# В данном случае ответ сервера = число
@api_router.get("/sum", response_model=float)
def sum_(a: float, b: float):
    """
    Метод выполняет сложение 2х чисел (integer или float) и возвращает результат
    """
    return a + b


# Обрати внимание на response_model <- описывает схему ответа сервера
@api_router.get("/count_letters", response_model=CountLettersResponse)
def count_letters(text: str):
    """
    Метод выполняет выполняет подсчет количества букв в тексте и
    возвращает результат в виде словаря, состоящего из пар: буква и кол-во.
    Также этот метод возвращает дату и время по местному часовому поясу,
    когда был произведен подсчет.
    """
    letters_count = {}
    for letter in text:
        if letter in letters_count:
            letters_count[letter] += 1
        else:
            letters_count[letter] = 1
    return CountLettersResponse(
        counted_at=datetime.datetime.now(),
        counters=letters_count
    )
