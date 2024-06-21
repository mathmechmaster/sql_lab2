# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class BookInfo(models.Model):
    bid = models.CharField(primary_key=True, max_length=20)
    isbn = models.CharField(db_column='ISBN', max_length=20, blank=True, null=True)  # Field name made lowercase.
    bname = models.CharField(max_length=100, blank=True, null=True)
    author = models.CharField(max_length=100, blank=True, null=True)
    publisher = models.CharField(max_length=100, blank=True, null=True)
    publish_date = models.DateField(blank=True, null=True)
    btype = models.CharField(max_length=20, blank=True, null=True)
    inventory = models.IntegerField(blank=True, null=True)
    store_loc = models.CharField(max_length=200, blank=True, null=True)
    book_pic = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'book_info'


class BookManager(models.Model):
    manager_id = models.CharField(primary_key=True, max_length=20)
    manager_name = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    phone_num = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'book_manager'


class Borrow(models.Model):
    stu = models.OneToOneField('Student', models.DO_NOTHING, primary_key=True)  # The composite primary key (stu_id, bid, borrow_date) found, that is not supported. The first column is selected.
    bid = models.ForeignKey(BookInfo, models.DO_NOTHING, db_column='bid')
    borrow_date = models.DateField()
    due_date = models.DateField(blank=True, null=True)
    return_date = models.DateField(db_column='return_Date', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'borrow'
        unique_together = (('stu', 'bid', 'borrow_date'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
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


class HighManager(models.Model):
    manager = models.OneToOneField(BookManager, models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = 'high_manager'


class Reserve(models.Model):
    stu_id = models.CharField(primary_key=True, max_length=20)  # The composite primary key (stu_id, bid, reserve_Date) found, that is not supported. The first column is selected.
    bid = models.CharField(max_length=20)
    reserve_date = models.DateField(db_column='reserve_Date')  # Field name made lowercase.
    reserve_status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reserve'
        unique_together = (('stu_id', 'bid', 'reserve_date'),)


class Student(models.Model):
    stu_id = models.CharField(primary_key=True, max_length=20)
    stu_name = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    grade = models.CharField(max_length=16, blank=True, null=True)
    major = models.CharField(max_length=30, blank=True, null=True)
    phone_num = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'student'


class User(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    is_manager = models.IntegerField(blank=True, null=True)
    password = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'


class Violation(models.Model):
    stu_id = models.CharField(primary_key=True, max_length=20)  # The composite primary key (stu_id, bid, borrow_date) found, that is not supported. The first column is selected.
    bid = models.CharField(max_length=20)
    borrow_date = models.DateField()
    vio_day = models.IntegerField(blank=True, null=True)
    fine = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'violation'
        unique_together = (('stu_id', 'bid', 'borrow_date'),)
