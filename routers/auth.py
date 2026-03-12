from datetime import timedelta, timezone, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm , OAuth2PasswordBearer
from jose import jwt, JWTError
from jose.constants import ALGORITHMS
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from starlette.status import HTTP_201_CREATED
from fastapi.templating import Jinja2Templates

from database import SessionLocal
from models import Users
from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated= 'auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')
router = APIRouter(
    prefix='/auth',
    tags=['authorization']
)

class CreateUserRequest(BaseModel):
       username: str
       first_name: str
       last_name : str
       password : str
       role : str
       email : str


class Token(BaseModel):
    access_token :str
    token_type : str




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

templates = Jinja2Templates(directory='templates')

@router.get("/login-page")
def render_login_page(request: Request):
    return templates.TemplateResponse("login.html",{"request": request})

@router.get("/register-page")
def render_register_page(request: Request):
    return templates.TemplateResponse("register.html",{"request": request})

@router.post("/" , status_code=HTTP_201_CREATED)
def create_user(db: db_dependency, create_user_request : CreateUserRequest
                ):
    create_user_modal = Users(
        email = create_user_request.email,
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        username = create_user_request.username,
        role = create_user_request.role,
        hashed_password= bcrypt_context.hash(create_user_request.password),
        is_active= True
    )
    # user = Users(**create_user_modal.model_Dump())
    db.add(create_user_modal)
    db.commit()
    return create_user_modal


def authenticate_user(form_data, db):
    username= form_data.username
    user= db.query(Users).filter(Users.username ==username).first()
    if not user :
        return False

    # if not bcrypt_context.verify(user.hashed_password, form_data.password):
    #     return False
    return user



@router.post("/token" , response_model=Token)
async def login_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                      db: db_dependency):
 user = authenticate_user(form_data,db)
 if not  user:
     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                         detail='Could not validate user.'
                         )

 tok = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))

 return {'access_token': tok , 'token_type':'bearer'}

SECRET_KEY = '93847893U489UT53984UFDJGNDJNFGJNDFJG'
ALGORITHM = 'HS256'

def create_access_token(username:str , user_id:int ,user_role:str,  expires_delta: timedelta):
    encode =  {'sub':username , 'id': user_id , 'role':user_role}
    expires = datetime.now(timezone.utc)+ expires_delta
    encode.update({'exp':expires})
    return jwt.encode(encode, SECRET_KEY,algorithm=ALGORITHM)



def get_current_user(token: Annotated[str,Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username : str = payload.get('sub')
        user_id : int = payload.get('id')
        user_role : str = payload.get('role')

        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail = 'Could not validate user.'
                                )
        return {'username': username , 'id': user_id , 'user_role':user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')





