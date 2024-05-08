# from typing import List
# import fastapi as _fastapi
# import fastapi.security as _security

# import sqlalchemy.orm as _orm

# from database import get_db
# import services as _services, schemas as _schemas
from typing import List
from fastapi import FastAPI, Depends, HTTPException
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


app = _fastapi.FastAPI()


@app.post("/api/users")
async def create_user(
    user: _schemas.UserCreate, db: _orm.Session = _fastapi.Depends(get_db)
):
    db_user = await _services.get_user_by_email(user.email, db)
    if db_user:
        raise _fastapi.HTTPException(status_code=400, detail="Email already in use")

    user = await _services.create_user(user, db)

    return await _services.create_token(user)


@app.post("/api/token")
async def generate_token(
    form_data: _security.OAuth2PasswordRequestForm = _fastapi.Depends(),
    db: _orm.Session = _fastapi.Depends(get_db),
):
    user = await _services.authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise _fastapi.HTTPException(status_code=401, detail="Invalid Credentials")

    return await _services.create_token(user)


@app.get("/api/users/me", response_model=_schemas.User)
async def get_user(user: _schemas.User = _fastapi.Depends(_services.get_current_user)):
    return user


@app.post("/api/leads", response_model=_schemas.Lead)
async def create_lead(
    lead: _schemas.LeadCreate,
    user: _schemas.User = _fastapi.Depends(_services.get_current_user),
    db: _orm.Session = _fastapi.Depends(get_db),
):
    return await _services.create_lead(user=user, db=db, lead=lead)


@app.get("/api/leads", response_model=List[_schemas.Lead])
async def get_leads(
    user: _schemas.User = _fastapi.Depends(_services.get_current_user),
    db: _orm.Session = _fastapi.Depends(get_db),
):
    return await _services.get_leads(user=user, db=db)


@app.get("/api/leads/{lead_id}", status_code=200)
async def get_lead(
    lead_id: int,
    user: _schemas.User = _fastapi.Depends(_services.get_current_user),
    db: _orm.Session = _fastapi.Depends(get_db),
):
    return await _services.get_lead(lead_id, user, db)


@app.delete("/api/leads/{lead_id}", status_code=204)
async def delete_lead(
    lead_id: int,
    user: _schemas.User = _fastapi.Depends(_services.get_current_user),
    db: _orm.Session = _fastapi.Depends(get_db),
):
    await _services.delete_lead(lead_id, user, db)
    return {"message", "Successfully Deleted"}


@app.put("/api/leads/{lead_id}", status_code=200)
async def update_lead(
    lead_id: int,
    lead: _schemas.LeadCreate,
    user: _schemas.User = _fastapi.Depends(_services.get_current_user),
    db: _orm.Session = _fastapi.Depends(get_db),
):
    await _services.update_lead(lead_id, lead, user, db)
    return {"message", "Successfully Updated"}


@app.get("/api")
async def root():
    return {"message": "Awesome Leads Manager"}








# from typing import List
# from fastapi import FastAPI, Depends, HTTPException
# from fastapi.security import OAuth2PasswordRequestForm
# from sqlalchemy.orm import Session
# import uvicorn
# import services
# import schemas
# import database

# app = FastAPI()

# @app.post("/api/users")
# async def create_user(
#     user: schemas.UserCreate, 
#     db: Session = Depends(database.get_db)
# ):
#     db_user = await services.get_user_by_email(user.email, db)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already in use")

#     user = await services.create_user(user, db)

#     return await services.create_token(user)

# @app.post("/api/token")
# async def generate_token(
#     form_data: OAuth2PasswordRequestForm = Depends(),
#     db: Session = Depends(database.get_db),
# ):
#     user = await services.authenticate_user(form_data.username, form_data.password, db)

#     if not user:
#         raise HTTPException(status_code=401, detail="Invalid Credentials")

#     return await services.create_token(user)

# @app.get("/api/users/me", response_model=schemas.User)
# async def get_user(user: schemas.User = Depends(services.get_current_user)):
#     return user

# @app.post("/api/leads", response_model=schemas.Lead)
# async def create_lead(
#     lead: schemas.LeadCreate,
#     user: schemas.User = Depends(services.get_current_user),
#     db: Session = Depends(database.get_db),
# ):
#     return await services.create_lead(user=user, db=db, lead=lead)

# @app.get("/api/leads", response_model=List[schemas.Lead])
# async def get_leads(
#     user: schemas.User = Depends(services.get_current_user),
#     db: Session = Depends(database.get_db),
# ):
#     return await services.get_leads(user=user, db=db)

# @app.get("/api/leads/{lead_id}", status_code=200)
# async def get_lead(
#     lead_id: int,
#     user: schemas.User = Depends(services.get_current_user),
#     db: Session = Depends(database.get_db),
# ):
#     return await services.get_lead(lead_id, user, db)

# @app.delete("/api/leads/{lead_id}", status_code=204)
# async def delete_lead(
#     lead_id: int,
#     user: schemas.User = Depends(services.get_current_user),
#     db: Session = Depends(database.get_db),
# ):
#     await services.delete_lead(lead_id, user, db)
#     return {"message": "Successfully Deleted"}

# @app.put("/api/leads/{lead_id}", status_code=200)
# async def update_lead(
#     lead_id: int,
#     lead: schemas.LeadCreate,
#     user: schemas.User = Depends(services.get_current_user),
#     db: Session = Depends(database.get_db),
# ):
#     await services.update_lead(lead_id, lead, user, db)
#     return {"message": "Successfully Updated"}

# @app.get("/api")
# async def root():
#     return {"message": "Awesome Leads Manager"}

# if __name__ == "__main__":
#     database.create_tables()
#     uvicorn.run(app, host="0.0.0.0", port=8000)




