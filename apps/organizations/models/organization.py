from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Organization(MPTTModel):
    name = models.CharField(max_length=250, unique=True)
    desc = models.CharField(max_length=250)
    code = models.CharField(max_length=25, default='')
    subpath = models.CharField(max_length=25, default='')

    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']
