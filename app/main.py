from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from .database import engine, Base, get_db
from .models import Lab
from .crud import get_all_labs, get_lab_by_id
from .schemas import LabList, LabDetail

app = FastAPI(title="Labs Backend — grustniserver")

# Создаём таблицы и сеем данные при первом запуске
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    db: Session = next(get_db())
    if db.query(Lab).count() == 0:
        seed_data(db)
    db.close()

def seed_data(db: Session):
    labs = [
        {
            "name": "Broken Nginx",
            "difficulty": 2,
            "estimated_time": 25,
            "description": "Nginx не отвечает на 80 порту. Найдите проблему и почините сервис.",
            "docker_image": "ghcr.io/yourname/nginx-broken:latest"
        },
        {
            "name": "Postgres не стартует",
            "difficulty": 3,
            "estimated_time": 40,
            "description": "База данных не поднимается после перезагрузки. Почините конфиг и запустите сервис.",
            "docker_image": "ghcr.io/yourname/postgres-broken:latest"
        },
        {
            "name": "SSH без пароля",
            "difficulty": 1,
            "estimated_time": 15,
            "description": "Нужно зайти по SSH без пароля (ключ уже лежит в контейнере).",
            "docker_image": "ghcr.io/yourname/ssh-lab:latest"
        },
        {
            "name": "Apache + неправильные права",
            "difficulty": 4,
            "estimated_time": 35,
            "description": "Сайт не открывается из-за прав на файлы. Исправьте и перезапустите Apache.",
            "docker_image": "ghcr.io/yourname/apache-permissions:latest"
        },
    ]
    for data in labs:
        lab = Lab(**data)
        db.add(lab)
    db.commit()

@app.get("/labs")
def get_labs(
    id: int | None = Query(None, alias="id", description="ID лабы (если нужен один)"),
    db: Session = Depends(get_db)
):
    if id is not None:
        lab = get_lab_by_id(db, id)
        if not lab:
            raise HTTPException(status_code=404, detail="Лаба не найдена")

        # Пока статус мок. Позже заменим на реальный из таблицы сессий
        return LabDetail(
            id=lab.id,
            name=lab.name,
            difficulty=lab.difficulty,
            estimated_time=lab.estimated_time,
            description=lab.description,
            docker_image=lab.docker_image,
            status="not_launched"          # ← здесь будет "deploying", "running" и т.д.
        )

    # Список всех лаб
    labs = get_all_labs(db)
    return {
        "labs": [LabList.model_validate(l) for l in labs]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)