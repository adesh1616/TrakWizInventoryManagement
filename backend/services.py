# import fastapi as _fastapi
# import fastapi.security as _security
# import jwt as _jwt
# import datetime as _dt
# import sqlalchemy.orm as _orm
# import hashlib as _hash

# import database as _database, models as _models, schemas as _schemas

# oauth2schema = _security.OAuth2PasswordBearer(tokenUrl="/api/token")

# JWT_SECRET = "myjwtsecret"


# def create_database():
#     return _database.Base.metadata.create_all(bind=_database.engine)


# def get_db():
#     db = _database.SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# async def get_user_by_email(email: str, db: _orm.Session):
#     return db.query(_models.User).filter(_models.User.email == email).first()


# async def create_user(user: _schemas.UserCreate, db: _orm.Session):
#     user_obj = _models.User(
#         email=user.email, hashed_password=_hash.bcrypt.hash(user.hashed_password)
#     )
#     db.add(user_obj)
#     db.commit()
#     db.refresh(user_obj)
#     return user_obj


# async def authenticate_user(email: str, password: str, db: _orm.Session):
#     user = await get_user_by_email(db=db, email=email)

#     if not user:
#         return False

#     if not user.verify_password(password):
#         return False

#     return user


# async def create_token(user: _models.User):
#     user_obj = _schemas.User.from_orm(user)

#     token = _jwt.encode(user_obj.dict(), JWT_SECRET)

#     return dict(access_token=token, token_type="bearer")


# async def get_current_user(
#     db: _orm.Session = _fastapi.Depends(get_db),
#     token: str = _fastapi.Depends(oauth2schema),
# ):
#     try:
#         payload = _jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
#         user = db.query(_models.User).get(payload["id"])
#     except:
#         raise _fastapi.HTTPException(
#             status_code=401, detail="Invalid Email or Password"
#         )

#     return _schemas.User.from_orm(user)


# async def create_lead(user: _schemas.User, db: _orm.Session, lead: _schemas.LeadCreate):
#     lead = _models.Lead(**lead.model_dump(), owner_id=user.id)
#     db.add(lead)
#     db.commit()
#     db.refresh(lead)
#     return _schemas.Lead.from_orm(lead)


# async def get_leads(user: _schemas.User, db: _orm.Session):
#     leads = db.query(_models.Lead).filter_by(owner_id=user.id)

#     return list(map(_schemas.Lead.from_orm, leads))


# async def _lead_selector(lead_id: int, user: _schemas.User, db: _orm.Session):
#     lead = (
#         db.query(_models.Lead)
#         .filter_by(owner_id=user.id)
#         .filter(_models.Lead.id == lead_id)
#         .first()
#     )

#     if lead is None:
#         raise _fastapi.HTTPException(status_code=404, detail="Lead does not exist")

#     return lead


# async def get_lead(lead_id: int, user: _schemas.User, db: _orm.Session):
#     lead = await _lead_selector(lead_id=lead_id, user=user, db=db)

#     return _schemas.Lead.from_orm(lead)


# async def delete_lead(lead_id: int, user: _schemas.User, db: _orm.Session):
#     lead = await _lead_selector(lead_id, user, db)

#     db.delete(lead)
#     db.commit()

# async def update_lead(lead_id: int, lead: _schemas.LeadCreate, user: _schemas.User, db: _orm.Session):
#     lead_db = await _lead_selector(lead_id, user, db)

#     lead_db.first_name = lead.first_name
#     lead_db.last_name = lead.last_name
#     lead_db.email = lead.email
#     lead_db.company = lead.company
#     lead_db.note = lead.note
#     lead_db.date_last_updated = _dt.datetime.utcnow()

#     db.commit()
#     db.refresh(lead_db)

#     return _schemas.Lead.from_orm(lead_db)

import fastapi
import fastapi.security
import jwt
import datetime
import sqlalchemy.orm
import bcrypt
import database, models, schemas

oauth2schema = fastapi.security.OAuth2PasswordBearer(tokenUrl="/api/token")

JWT_SECRET = "myjwtsecret"

async def get_user_by_email(email: str, db: sqlalchemy.orm.Session):
    try:
        return db.query(models.User).filter(models.User.email == email).first()
    except Exception as e:
        print(f"An error occurred while fetching user by email: {e}")

async def create_user(user: schemas.UserCreate, db: sqlalchemy.orm.Session):
    try:
        hashed_password = bcrypt.hashpw(user.hashed_password.encode(), bcrypt.gensalt())
        user_obj = models.User(
            email=user.email, hashed_password=hashed_password
        )
        db.add(user_obj)
        db.commit()
        db.refresh(user_obj)
        return user_obj
    except Exception as e:
        print(f"An error occurred while creating user: {e}")

async def authenticate_user(email: str, password: str, db: sqlalchemy.orm.Session):
    try:
        user = await get_user_by_email(db=db, email=email)
        if not user:
            return False
        if not bcrypt.checkpw(password.encode(), user.hashed_password):
            return False
        return user
    except Exception as e:
        print(f"An error occurred while authenticating user: {e}")

async def create_token(user: models.User):
    user_obj = schemas.User.from_orm(user)
    token = jwt.encode(user_obj.dict(), JWT_SECRET)
    return dict(access_token=token, token_type="bearer")

async def get_current_user(
    db: sqlalchemy.orm.Session = fastapi.Depends(database.get_db),
    token: str = fastapi.Depends(oauth2schema),
):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = db.query(models.User).get(payload["id"])
    except:
        raise fastapi.HTTPException(
            status_code=401, detail="Invalid Email or Password"
        )
    return schemas.User.from_orm(user)
