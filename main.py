from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Release Management Service",
    description="Микросервис для управления релизами ПО (Лабораторная работа №6)",
    version="1.0.0",
)


class Release(BaseModel):
    id: int
    version: str
    status: str  # success, failed, pending
    description: Optional[str] = None
    created_at: datetime = datetime.now()


releases_db = [
    Release(
        id=1,
        version="v1.0.0",
        status="success",
        description="Первый стабильный релиз",
    ),
    Release(
        id=2,
        version="v1.1.0",
        status="pending",
        description="Сборка с автотестами",
    ),
]


@app.get("/api/v1/releases/", response_model=List[Release])
def get_releases():
    """Получение списка всех релизов"""
    return releases_db


@app.get("/api/v1/releases/{release_id}", response_model=Release)
def get_release(release_id: int):
    """Получение информации о релизе по ID"""
    for release in releases_db:
        if release.id == release_id:
            return release
    raise HTTPException(status_code=404, detail="Релиз не найден")


@app.post("/api/v1/releases/", response_model=Release, status_code=201)
def create_release(release: Release):
    """Создание нового релиза"""
    for existing in releases_db:
        if existing.id == release.id:
            raise HTTPException(
                status_code=400, detail="Релиз с таким ID уже существует"
            )
    releases_db.append(release)
    return release


@app.delete("/api/v1/releases/{release_id}", status_code=200)
def delete_release(release_id: int):
    """Удаление релиза по ID"""
    for index, release in enumerate(releases_db):
        if release.id == release_id:
            releases_db.pop(index)
            return {"detail": "Релиз успешно удален"}
    raise HTTPException(status_code=404, detail="Релиз не найден")
# проверка pull request