from django.db import models
from django.contrib.auth.models import Permission

class Role(models.Model):
    name = models.CharField(max_length=100)
    alias = models.CharField(max_length=100, default=name)    

    permissions = models.ManyToManyField(Permission,db_table='auth_role_permissions_map')
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "auth_role"