from model import CountLettersResponse
from datetime import datetime

if __name__ == '__main__':
    # Данный код демонстрирует процесс создания экземпляра модели и
    # заполнения его данными, а также преобразование в json.
    # Будет полезен при разработке собственной модели ответа.
    response = CountLettersResponse(
        counted_at=datetime.now(),
        counters={
            "a": 1,
            "b": 2
        }
    )
    print(response.json())
