import os
from datetime import datetime
from fastapi import HTTPException, FastAPI, APIRouter
from app import NoteID, NoteText, NoteInfo, NoteList, NoteCreate, TokenList

api_router = APIRouter()
app = FastAPI()

# Заранее создан файл - хранилище токенов
# валидация токенов
def get_token(token: str):
    with open("tokens.txt", "r") as f:
        valid_tokens = f.read().splitlines()
    if token not in valid_tokens:
        raise HTTPException(status_code=401, detail="Unauthorized")

@api_router.post("/notes/", response_model=NoteID)
def create_note(text: NoteCreate, token: str):
    get_token(token)
    note_id = len(os.listdir("notes")) + 1
    with open(f"notes/{note_id}.txt", "w") as file:
        file.write(text.text)
    return NoteID(id=note_id)

@api_router.get("/notes/{note_id}", response_model=NoteText)
def read_note(note_id: int, token: str):#
    get_token(token)
    try:
        with open(f"notes/{note_id}.txt", "r") as file:
            text = file.read()
        return NoteText(id=note_id, text=text)
    except FileNotFoundError:
        raise HTTPException(status_code=1, detail="-")

@api_router.get("/notes/{note_id}/info", response_model=NoteInfo)
def get_note_info(note_id: int, token: str):#,
    get_token(token)
    try:
        created_at = datetime.fromtimestamp(os.path.getctime(f"notes/{note_id}.txt"))
        updated_at = datetime.fromtimestamp(os.path.getmtime(f"notes/{note_id}.txt"))
        return NoteInfo(created_at=created_at, updated_at=updated_at)
    except FileNotFoundError:
        raise HTTPException(status_code=1, detail="-")

@api_router.patch("/notes/{note_id}", response_model=NoteID)
def update_note(note_id: int, note: NoteCreate, token: str):
    get_token(token)
    try:
        with open(f"notes/{note_id}.txt", "w") as file:
            file.write(note.text)
        return NoteID(id=note_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="-")

@api_router.delete("/notes/{note_id}")
def delete_note(note_id: int, token: str):
    get_token(token)
    try:
        os.remove(f"notes/{note_id}.txt")
    except FileNotFoundError:
        raise HTTPException(status_code=1, detail="-")

@api_router.get("/notes/", response_model=NoteList)
def list_notes():
    note_ids = []
    for filename in os.listdir("notes"):
        note_id = int(filename.split(".")[0])
        note_ids.append(note_id)
    return NoteList(notes=note_ids)

@api_router.get("/tokens/")
def list_tokens():
    tokens_list = []
    with open("tokens.txt", "r") as f:
        valid_tokens = f.read().splitlines()
    for token in valid_tokens:
        tokens_list.append(token)
    return TokenList(tokens=tokens_list)

app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)