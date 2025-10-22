# backend/app/routers/protected.py
from fastapi import APIRouter, Depends
from backend.dependencies import get_admin

router = APIRouter(tags=["protected"])

# Route that tests expect:
admin_router = APIRouter(prefix="/api/admin")

@admin_router.get("/stats")
async def admin_stats(_user = Depends(get_admin)):
    # If not admin, get_admin will raise 403; otherwise return something simple.
    return {"ok": True}


# (Optional) keep your previous protected route, if you like:
protected_router = APIRouter(prefix="/api/protected")

@protected_router.get("/admin")
async def admin_only(_user = Depends(get_admin)):
    return {"ok": True}
