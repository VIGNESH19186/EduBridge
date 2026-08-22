from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from backend.database.database import get_db
from backend.models.user import User, RoleEnum
from backend.models.student import Student
from backend.models.teacher import Teacher
from backend.schemas.auth import RegisterRequest, LoginRequest, TokenResponse, UserOut
from backend.utils.security import hash_password, verify_password, create_access_token, decode_access_token

router = APIRouter(prefix="/api/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not token:
        raise credentials_exception
    payload = decode_access_token(token)
    if not payload or "user_id" not in payload:
        raise credentials_exception
    user = db.query(User).filter(User.id == payload["user_id"]).first()
    if not user:
        raise credentials_exception
    return user


def require_role(*allowed_roles: str):
    def dependency(user: User = Depends(get_current_user)) -> User:
        if user.role.value not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"This action requires one of the following roles: {allowed_roles}",
            )
        return user
    return dependency


@router.post("/register", response_model=TokenResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="An account with this email already exists.")

    user = User(
        name=payload.name,
        email=payload.email,
        hashed_password=hash_password(payload.password),
        role=RoleEnum(payload.role),
        preferred_language=payload.preferred_language or "English",
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    if user.role == RoleEnum.student:
        db.add(Student(user_id=user.id))
    elif user.role == RoleEnum.teacher:
        db.add(Teacher(user_id=user.id))
    db.commit()

    token = create_access_token({"user_id": user.id, "role": user.role.value})
    return TokenResponse(access_token=token, user_id=user.id, name=user.name, role=user.role.value)


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    token = create_access_token({"user_id": user.id, "role": user.role.value})
    return TokenResponse(access_token=token, user_id=user.id, name=user.name, role=user.role.value)


@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
    return current_user
