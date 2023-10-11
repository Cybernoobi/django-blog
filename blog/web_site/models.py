from django.db import models

# Create your models here.

"""
create table if not exists category(
    name 
)
"""


class Category(models.Model):
    name = models.CharField(max_length=155, verbose_name="Название категории")
