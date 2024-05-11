from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
import fastapi
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import uvicorn
from pydantic import BaseModel
from datetime import datetime
import jwt
import bcrypt
import services as _services, schemas as _schemas
import sqlalchemy.orm as _orm

# Database
DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    Base.metadata.create_all(bind=engine)

# Models
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

Base.metadata.create_all(bind=engine)

# Schemas
class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserInDB(BaseModel):
    username: str
    hashed_password: str

# Password hashing
def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode(), hashed_password)

def get_password_hash(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# Services
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")
JWT_SECRET = "myjwtsecret"

async def get_user_by_username(username: str, db: Session):
    try:
        return db.query(User).filter(User.username == username).first()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while fetching user by username.")

async def create_user(user: UserCreate, db: Session):
    try:
        hashed_password = get_password_hash(user.password)
        user_obj = User(
            username=user.username, hashed_password=hashed_password
        )
        db.add(user_obj)
        db.commit()
        db.refresh(user_obj)
        return user_obj
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while creating user.")

async def authenticate_user(username: str, password: str, db: Session):
    try:
        user = await get_user_by_username(db=db, username=username)
        if not user:
            return False
        if not verify_password(password, user.hashed_password):
            return False
        return user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while authenticating user.")

async def create_token(user: User):
    try:
        user_obj = UserInDB(username=user.username, hashed_password=user.hashed_password)
        token = jwt.encode(user_obj.dict(), JWT_SECRET)
        return dict(access_token=token, token_type="bearer")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while creating token.")

# Main
app = FastAPI()

@app.post("/register/")
async def register_user(
    user: UserCreate, 
    db: Session = Depends(get_db)
):
    db_user = await get_user_by_username(user.username, db)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already in use")

    user = await create_user(user, db)

    return await create_token(user)

@app.post("/login/")
async def login_user(
    user: UserLogin, 
    db: Session = Depends(get_db)
):
    user = await authenticate_user(user.username, user.password, db)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid Credentials")

    return await create_token(user)

@app.get("/protected/")
def protected_route(token: str = Depends(oauth2_scheme)):
    return {"message": "Access granted"}

@app.get("/api/users/me", response_model=_schemas.User)
async def get_user(user: _schemas.User = fastapi.Depends(_services.get_current_user)):
    return user


@app.post("/api/leads", response_model=_schemas.Lead)
async def create_lead(
    lead: _schemas.LeadCreate,
    user: _schemas.User = fastapi.Depends(_services.get_current_user),
    db: _orm.Session = fastapi.Depends(get_db),
):
    return await _services.create_lead(user=user, db=db, lead=lead)


@app.get("/api/leads", response_model=List[_schemas.Lead])
async def get_leads(
    user: _schemas.User = fastapi.Depends(_services.get_current_user),
    db: _orm.Session = fastapi.Depends(get_db),
):
    return await _services.get_leads(user=user, db=db)


@app.get("/api/leads/{lead_id}", status_code=200)
async def get_lead(
    lead_id: int,
    user: _schemas.User = fastapi.Depends(_services.get_current_user),
    db: _orm.Session = fastapi.Depends(get_db),
):
    return await _services.get_lead(lead_id, user, db)


@app.delete("/api/leads/{lead_id}", status_code=204)
async def delete_lead(
    lead_id: int,
    user: _schemas.User = fastapi.Depends(_services.get_current_user),
    db: _orm.Session = fastapi.Depends(get_db),
):
    await _services.delete_lead(lead_id, user, db)
    return {"message", "Successfully Deleted"}


@app.put("/api/leads/{lead_id}", status_code=200)
async def update_lead(
    lead_id: int,
    lead: _schemas.LeadCreate,
    user: _schemas.User = fastapi.Depends(_services.get_current_user),
    db: _orm.Session = fastapi.Depends(get_db),
):
    await _services.update_lead(lead_id, lead, user, db)
    return {"message", "Successfully Updated"}


@app.get("/api")
async def root():
    return {"message": "TrakWiz Inventory Management"}

if __name__ == "__main__":
    create_tables()
    uvicorn.run(app, host="0.0.0.0", port=8000)
