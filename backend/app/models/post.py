# from datetime import datetime

# from tortoise import fields, models

# class Post(models.Model):
#     post_id = fields.IntField(primary_key=True)

#     user_id = fields.ForeignKey("models.User", related_name="posts")
    
#     content = fields.TextField()

#     created_at = fields.DatetimeField(null=True)
#     updated_at = fields.DatetimeField(null=True)