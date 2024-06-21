from django.db import models

# Create your models here.
class User(models.Model):   #manager和student的id不重复
    id = models.CharField(primary_key=True, max_length=20)
    is_manager = models.IntegerField(blank=True, null=True)
    password = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'user'

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
    book_pic = models.ImageField(upload_to='images') #mysql数据库中存储图片的路径

    class Meta:
        managed = True
        db_table = 'book_info'


class BookManager(models.Model):
    manager_id = models.CharField(primary_key=True, max_length=20)
    manager_name = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    phone_num = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'book_manager'


class Borrow(models.Model):
    id = models.CharField(primary_key=True,max_length=45)
    stu_id = models.CharField(max_length=20)  # The composite primary key (stu_id, bid, borrow_date) found, that is not supported. The first column is selected.
    bid = models.CharField(max_length=20)
    borrow_date = models.DateField()
    due_date = models.DateField(blank=True, null=True)
    return_date = models.DateField(db_column='return_Date', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'borrow'
        unique_together = (('stu_id', 'bid', 'borrow_date'),)

class HighManager(models.Model):
    manager = models.OneToOneField(BookManager, models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = True
        db_table = 'high_manager'


class Reserve(models.Model):
    id = models.CharField(primary_key=True,max_length=45)
    stu_id = models.CharField(max_length=20)  # The composite primary key (stu_id, bid, reserve_Date) found, that is not supported. The first column is selected.
    bid = models.CharField(max_length=20)
    reserve_date = models.DateField(db_column='reserve_Date')  # Field name made lowercase.
    reserve_status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
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
        managed = True
        db_table = 'student'


class Violation(models.Model):
    id = models.CharField(primary_key=True,max_length=45)
    stu_id = models.CharField(max_length=20)  # The composite primary key (stu_id, bid, borrow_date) found, that is not supported. The first column is selected.
    bid = models.CharField(max_length=20)
    borrow_date = models.DateField()
    due_date = models.DateField()

    class Meta:
        managed = True
        db_table = 'violation'

