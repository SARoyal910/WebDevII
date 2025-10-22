# backend/dependencies.py
from fastapi import Depends, HTTPException, Request, Response, status
from backend.session import Session, InMemoryKV
from backend.app.models.user import User


async def get_session(request: Request, response: Response) -> Session:
    """
    Produce a Session object backed by an in-app InMemoryKV.
    """
    kv = getattr(request.app.state, "kv", None)
    if kv is None:
        kv = InMemoryKV()
        request.app.state.kv = kv
    return Session(request=request, response=response, storage=kv)


async def get_current_user(session: Session = Depends(get_session)) -> User:
    await session.load()
    user_id = getattr(session.data, "user_id", None)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return user


async def get_admin(session: Session = Depends(get_session)) -> User:
    """
    Minimal admin gate. Unless a flag is set on the session, deny access.
    Tests typically expect non-admins to be rejected with 403.
    """
    user = await get_current_user(session)
    is_admin = getattr(session.data, "is_admin", False)
    if not is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin only")
    return user



