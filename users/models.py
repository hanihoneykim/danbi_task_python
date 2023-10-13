from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(
        max_length=100,
        default="",
        help_text="사용하실 이름 혹은 별명을 입력해주세요",
        verbose_name="username",
    )
    username = models.CharField(
        max_length=15,
        unique=True,
        verbose_name="ID",
        help_text="15자 이내로 만들어주세요. 영어 소문자, 특수문자 (_) 사용 가능.",
        default="",
    )
