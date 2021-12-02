from django.db import models

# Create your models here.

class Fileinfo(models.Model):
    file_name = models.CharField(db_column='file_name', max_length=100, blank=True, null=True)  # Field name made lowercase.
    file_path = models.CharField(max_length=200, blank=True, null=True)
    file_size = models.CharField(max_length=100, blank=True, null=True)
    uploaded_by = models.CharField(db_column='uploaded_by', max_length=100, blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    agency_name = models.CharField(db_column='agency_name', max_length=200, blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    updated_by = models.CharField(db_column='updated_by', max_length=100, blank=True, null=True)  # Field name made lowercase.
    updated_date = models.DateTimeField(blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 's100_fileinfo'

class Headerinfo(models.Model): 
    product_line = models.CharField(db_column='product_line', max_length=100, blank=True, null=True)  # Field name made lowercase.
    header_name = models.CharField(max_length=100, blank=True, null=True)
    header_value = models.CharField(max_length=1000, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 's100_header_info' 

class Metadatainfo(models.Model): 
    product_line = models.CharField(db_column='product_line', max_length=100, blank=True, null=True)  # Field name made lowercase.
    created_by = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    deleted_by = models.CharField(max_length=100, blank=True, null=True)
    deleted_date = models.DateTimeField(blank=True, null=True)
    metadata = models.CharField(max_length=2000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 's100_file_metadata'

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


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)

class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)

class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)



class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'

class RoleInfo(models.Model):
    role_name = models.CharField(db_column='role_name', max_length=100, blank=True, null=True)
    restricted = models.CharField(db_column='restricted', max_length=50, blank=True, null=True)
    active = models.BooleanField(db_column='active', blank=True, null=True)
    description = models.CharField(db_column='description', max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 's100_role'
        
class UserInfo(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(db_column='user_name', max_length=200, blank=True, null=True)
    first_name = models.CharField(db_column='first_name', max_length=100, blank=True, null=True)
    last_name = models.CharField(db_column='last_name', max_length=100, blank=True, null=True)
    email = models.CharField(db_column='email', max_length=100, blank=True, null=True)
    phoneno = models.IntegerField()
    description = models.CharField(db_column='description', max_length=500, blank=True, null=True)
    role_id = models.ForeignKey(RoleInfo, models.DO_NOTHING, db_column='role_id', blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 's100_userinfo'

class AgencyInfo(models.Model):    
    agency_name = models.CharField(db_column='agency_name', max_length=100, blank=True, null=True)
    address = models.CharField(db_column='address', max_length=500, blank=True, null=True)
    phoneno = models.IntegerField()
    contact_person = models.CharField(db_column='contact_person', max_length=100, blank=True, null=True)
    email = models.CharField(db_column='email', max_length=100, blank=True, null=True)
    description = models.CharField(db_column='description', max_length=500, blank=True, null=True)
    agency_id = models.ForeignKey(UserInfo, models.DO_NOTHING, db_column='agency_id', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 's100_agencyinfo'

class PasswordInfo(models.Model):
    password_id = models.AutoField(primary_key=True)
    password = models.CharField(db_column='password', max_length=200, blank=True, null=True)
    password_expiry = models.DateField()
    password_alg = models.CharField(db_column='password_alg', max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 's100_password_info'

