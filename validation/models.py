from django.db import models

# Create your models here.
class ProductLineInfo(models.Model):
    name = models.CharField(db_column='name', max_length=10, blank=True, null=True)
    version = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField()
    number = models.IntegerField(blank=True, null=True)
    updated_by = models.CharField(db_column='updated_by', max_length=100, blank=True, null=True)  # Field name made lowercase.
    updated_date = models.DateField()

    class Meta:
        managed = False
        db_table = 's100_productspecification'

class RoleInfo(models.Model):
    role_name = models.CharField(db_column='role_name', max_length=100, blank=True, null=True)
    restricted = models.CharField(db_column='restricted', max_length=50, blank=True, null=True)
    active = models.BooleanField(db_column='active', blank=True, null=True) 
    description = models.CharField(max_length=500, blank=True, null=True)
 
    class Meta:
        managed = False
        db_table = 's100_role'

class AgencyInfo(models.Model):
    agency_name = models.CharField(db_column='agency_name', max_length=100, blank=True, null=True)
    address = models.CharField(db_column='address', max_length=500, blank=True, null=True)
    phoneno = models.IntegerField()
    contact_person = models.CharField(db_column='contact_person', max_length=100, blank=True, null=True)
    email = models.CharField(db_column='email', max_length=100, blank=True, null=True)
    description = models.CharField(db_column='description', max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 's100_agencyinfo'