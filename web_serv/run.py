from app import NoteID, NoteText, NoteInfo, NoteList
from datetime import datetime

import requests

API_URL = "http://localhost:8000"

def create_note():
    token = get_token()
    text = input("Введите текст заметки\n")
    response = requests.post(
        f"{API_URL}/notes/",
         json={"text": text},
         params={"token": token}
        )
    if response.status_code == 200:
        print(f"Заметка создана с ID: {response.json()['id']}")
    else:
        print(f"Ошибка: {response.json()['detail']}")

def get_note():
    token = get_token()
    note_id = input("Введите ID заметки: ")
    response = requests.get(
        f"{API_URL}/notes/{note_id}",
            params={"token": token}
            )
    if response.status_code == 200:
        print(f"Заметка {note_id}: {response.json()['text']}")
    else:
        print(f"Ошибка: {response.json()['detail']}")

def get_note_info():
    token = get_token()
    note_id = input("Введите ID заметки для получения информации: ")
    response = requests.get(
        f"{API_URL}/notes/{note_id}/info",
        params={"token": token}
    )
    if response.status_code == 200:
        info = response.json()
        print(f"Информация о заметке {note_id}:")
        print(f"Создана: {info['created_at']}")
        print(f"Обновлена: {info['updated_at']}")
    else:
        print(f"Ошибка: {response.json()['detail']}")

def update_note():
    token = get_token()
    note_id = input("Введите ID заметки для обновления: ")
    new_text = input("Введите новый текст заметки: ")
    response = requests.patch(
        f"{API_URL}/notes/{note_id}",
        json={"text": new_text},
        params={"token": token}
    )
    if response.status_code == 200:
        print(f"Заметка {note_id} обновлена.")
    else:
        print(f"Ошибка: {response.json()['detail']}")

def delete_note():
    token = get_token()
    note_id = input("Введите ID заметки для удаления: ")
    response = requests.delete(
        f"{API_URL}/notes/{note_id}",
        params={"token": token}
    )
    if response.status_code == 200:
        print(f"Заметка {note_id} удалена.")
    else:
        print(f"Ошибка: {response.json()['detail']}")

def list_notes():
    token = get_token()
    response = requests.get(
        f"{API_URL}/notes/",
        params={"token": token}
    )
    if response.status_code == 200:
        notes = response.json()['notes']
        if notes:
            print("Список заметок:")
            for note_id in notes:
                print(f"Заметка ID: {note_id}")
        else:
            print("Заметки отсутствуют.")
    else:
        print(f"Ошибка: {response.json()['detail']}")

def get_token():
    return input("токен: ")

def main():
    while True:

        print("\n1. Создать заметку\n2. Прочитать заметку по id"
              "\n3. Получить информацию о времени создания и обновления"
              "\n4. Обновить текст заметки\n5. Удалить заметку"
              "\n6. Вывести список id заметок")

        choice = input("->: ")

        if choice == "1":
            create_note()
        elif choice == "2":
            get_note()
        elif choice == "3":
            get_note_info()
        elif choice == "4":
            update_note()
        elif choice == "5":
            delete_note()
        elif choice == "6":
            list_notes()

        input("Продолжить")

if __name__ == "__main__":
    main()
