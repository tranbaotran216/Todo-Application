from tortoise import models
from tortoise.fields import IntField, BooleanField, CharField

class Todo(models.Model):
    id = IntField(pk=True)
    task=CharField(max_length=100, null=False)
    done = BooleanField(default=False)

    class Meta:
        table = "todos"