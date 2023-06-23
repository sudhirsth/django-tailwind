from django.db import models


class Group(models.Model):
    name=models.CharField(max_length=128)
    class Meta:
        db_table = 'access_group'

class AccessModule(models.Model):
    name = models.CharField(max_length=128)
    slug = models.CharField(max_length=128, unique=True)

    class Meta:
        db_table = 'access_module'


class AccessPermission(models.Model):
    module = models.ForeignKey(AccessModule, on_delete=models.PROTECT)
    name = models.CharField(max_length=128)
    slug = models.CharField(max_length=128, unique=True)
    groups = models.ManyToManyField(Group)

    class Meta:
        db_table = 'access_permission'
        unique_together = (('module', 'slug'))
