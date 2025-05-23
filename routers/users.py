from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.user import UserCreate, UserOut, UserToken, UserLogin, RefreshToken
from models.user import User
from security import hash_password, verify_password, create_access_token, get_current_user
from dependencies import get_db
from datetime import timedelta
from utils.routers import ProtectedRouter
from jose import jwt

SECRET_KEY = "pizzaria-backend-key"
ALGORITHM = "HS256"

protect_router = ProtectedRouter(prefix="/users", tags=["Users"])
public_router = APIRouter(prefix="/users", tags=["Users"])

@protect_router.get("/", response_model=list[UserOut])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@protect_router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return UserOut.from_orm(current_user)

@public_router.post("/login", response_model=UserToken)
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=login_data.email).first()

    if not user:
        raise HTTPException(status_code=400, detail="Usuário não existe.")
    
    password_matches = verify_password(login_data.password, user.hashed_password)

    if not password_matches:
        raise HTTPException(status_code=400, detail="Senha inválida. Tente novamente.")
    else:
        token = create_access_token({"sub": str(user.id), "role": user.role}, timedelta(minutes=1))
        refresh_token = create_access_token({"sub": str(user.id), "role": user.role}, timedelta(days=7))

        return {"access_token": token, "refresh_token": refresh_token, "token_type": "bearer"}
    
@public_router.post("/refresh", response_model=UserToken)
def login(refresh_data: RefreshToken, db: Session = Depends(get_db)):
    db = next(get_db())
    user = get_current_user(refresh_data.refresh_token, db)

    if user:
        token = create_access_token({"sub": str(user.id), "role": user.role}, timedelta(minutes=1))
        refresh_token = create_access_token({"sub": str(user.id), "role": user.role}, timedelta(days=7))

        return {"access_token": token, "refresh_token": refresh_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Refresh token inválido")
    
@public_router.post("/", response_model=UserOut)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    username_exists = db.query(User).filter_by(username=user_data.username).first()
    email_exists = db.query(User).filter_by(email=user_data.email).first()

    if username_exists:
        raise HTTPException(status_code=400, detail="Um usuário com esse nome já existe.")
    
    if email_exists:
        raise HTTPException(status_code=400, detail="Um usuário com esse email já existe")

    hashed = hash_password(user_data.password)

    new_user = User(
        username=user_data.username,
        contact=user_data.contact,
        email=user_data.email,
        hashed_password=hashed,
        is_active=True,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
