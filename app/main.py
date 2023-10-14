import uuid
from datetime import datetime
from typing import List

from dotenv import dotenv_values
from fastapi import FastAPI, HTTPException
import uvicorn
from fastapi.params import Body, Depends
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from starlette import status
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session

from app.api_schemas import UserSchema

config = dotenv_values(".env")

app = FastAPI(
    title="HomeJar - API Service",
    description="API specifications for HomeJar project",
    version="0.0.1",
    docs_url="/homejar/ui/",
    openapi_url="/homejar/openapi.json"
)
DATABASE_URL = "postgresql://andrerebo98:94xRYvIVbpGE@ep-rough-sound-662965.eu-central-1.aws.neon.tech/HomeJar"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class BaseModel(Base):
    __abstract__ = True
    id = Column(UUID, primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(UUID)
    modified_at = Column(DateTime, default=datetime.utcnow)
    modified_by = Column(UUID)

class UserModel(BaseModel):
    __tablename__ = "users"

    name = Column(String)
    phone = Column(String, unique=True, index=True)
    email = Column(String)
    password = Column(String)
    super_admin = Column(Boolean, default=False)
    is_child = Column(Boolean, default=False)
    account_user = Column(UUID, nullable=True)
    settings = Column(JSON, nullable=True)

def create_tables():
    Base.metadata.create_all(bind=engine)

def get_users(db: Session = Depends(get_db)):
    users = db.query(UserModel).all()
    return users

@app.get("/homejar/users", response_description="List all users", response_model=List[UserSchema])
async def list_users(limit: int = 15):
    return get_users()


@app.post("/homejar/users", response_description="Add new user", response_model=UserSchema)
async def create_user(body: UserSchema = Body(...), db: Session = Depends(get_db)):
    user_id = uuid.uuid4()
    body.id = str(user_id)
    body.modified_by = str(user_id)
    body.created_by = str(user_id)
    db_user = UserModel(**body.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content="ok")


if __name__ == "__main__":
    create_tables()
    uvicorn.run(app, host="0.0.0.0", port=8000)