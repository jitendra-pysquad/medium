from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pic = models.ImageField(upload_to='users/pics', null=True, blank=True)

    def __str__(self):
        return self.email if self.email else self.username

    def is_admin(self):
        return self.is_staff or self.is_superuser

