from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    """ Custom User Model"""

    avatar = models.ImageField(null=True, blank=True, upload_to="avatars")