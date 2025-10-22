# backend/app/routers/auth.py
from typing import Optional
from fastapi import APIRouter, Form, Depends, HTTPException, status, Header
from tortoise.exceptions import IntegrityError
from passlib.hash import bcrypt
from backend.app.models.user import User
from backend.dependencies import get_session
from backend.session import Session

router = APIRouter(prefix="/api/auth", tags=["auth"])


def hash_password(password: str) -> str:
    return bcrypt.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.verify(plain, hashed)


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(
    email: str = Form(...),
    password: str = Form(...),
    password_confirmation: str = Form(...),
    session: Session = Depends(get_session),
):
    if password != password_confirmation:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    username = (email.split("@", 1)[0] or email)

    try:
        user = await User.create(
            email=email,
            username=username,
            hashed_password=hash_password(password),
        )
    except IntegrityError:
        # unique email/username
        raise HTTPException(status_code=400, detail="User already exists")

    await session.load()
    # store the primary key (works regardless of underlying pk field name)
    session.data.user_id = str(user.pk)
    csrf_token = await session.rotate_csrf_token()
    await session.commit()

    return {"id": str(user.pk), "email": user.email, "csrf": csrf_token}


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    email: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_session),
):
    user = await User.get_or_none(email=email)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    await session.load()
    session.data.user_id = str(user.pk)
    csrf_token = await session.rotate_csrf_token()
    await session.commit()
    return {"csrf": csrf_token}


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(session: Session = Depends(get_session)):
    await session.load()
    await session.clear()
    return {"ok": True}


@router.post("/change-password", status_code=status.HTTP_200_OK)
async def change_password(
    old_password: str = Form(...),
    new_password: str = Form(...),
    session: Session = Depends(get_session),
    csrf_token: Optional[str] = Header(None, alias="X-CSRF-Token"),
):
    await session.load()
    if not csrf_token or not session.verify_csrf_token(csrf_token):
        raise HTTPException(status_code=400, detail="CSRF token missing or invalid")

    user_pk = getattr(session.data, "user_id", None)
    if not user_pk:
        raise HTTPException(status_code=401, detail="Not authenticated")

    # Use pk lookup so it works whether the field is 'id' or 'user_id'
    user = await User.get_or_none(pk=user_pk)
    if not user or not verify_password(old_password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid password")

    user.hashed_password = hash_password(new_password)
    await user.save()
    await session.commit()
    return {"ok": True}


@router.get("/me", status_code=status.HTTP_200_OK)
async def me(session: Session = Depends(get_session)):
    await session.load()
    user_pk = getattr(session.data, "user_id", None)
    if not user_pk:
        raise HTTPException(status_code=401, detail="Not authenticated")

    user = await User.get_or_none(pk=user_pk)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    return {"id": str(user.pk), "email": user.email, "csrf": session.get_csrf_token()}





