from functools import wraps

def Guard(dep):
    def decorator(route):
        @wraps(route)
        async def wrapper(*args, **kwargs):
            return await route(*args, **kwargs)
        wrapper.__dependencies__ = [Depends(dep)]
        return wrapper
    return decorator

@app.get("/decorated")
@Guard(get_current_user)
async def decorated_route():
    return {"message": "Guarded with decorator"}