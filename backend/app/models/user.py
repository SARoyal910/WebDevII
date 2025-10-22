from datetime import datetime
from enum import Enum
from passlib.hash import bcrypt
from tortoise import fields, models
import uuid

class Role(str, Enum):
    user = "user"
    admin = "admin"

class User(models.Model):
    """User model with password hashing using passlib (bcrypt)."""

    user_id = fields.UUIDField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    email = fields.CharField(max_length=255, unique=True)
    email_normalized = fields.CharField(max_length=255, null=True)
    
    fname = fields.CharField(max_length=50, null=True, default="")
    lname = fields.CharField(max_length=50, null=True, default="")
    
    hashed_password = fields.CharField(max_length=128)
    is_active = fields.BooleanField(default=True)
    role = fields.CharEnumField(Role, default=Role.user)
    
    activated_at = fields.DatetimeField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "users"

    def set_password(self, raw_password: str):
        # bcrypt truncates at 72 bytes; enforce and fail loudly
        if len(raw_password.encode("utf-8")) > 72:
            raise ValueError("Password exceeds bcrypt 72-byte limit.")
        self.hashed_password = bcrypt.hash(raw_password)

    def verify_password(self, raw_password: str) -> bool:
        
        return bcrypt.verify(raw_password, self.hashed_password)