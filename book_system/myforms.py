from django import forms
  
  
class UserForm(forms.Form):
    username = forms.CharField(label="学号/工号", max_length=20,
widget=forms.TextInput(attrs={'class': 'form-control'}))
 
    password = forms.CharField(label="密码", max_length=256,
widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
class RegisterForm(forms.Form):
    username = forms.CharField(label="学号", max_length=20,
widget=forms.TextInput(attrs={'class': 'form-control'}))
 
    password1 = forms.CharField(label="密码", max_length=256,
widget=forms.PasswordInput(attrs={'class': 'form-control'}))
 
    password2 = forms.CharField(label="确认密码", max_length=256,
widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
class ManagerRegisterForm(forms.Form):
    username = forms.CharField(label="工号", max_length=20,
widget=forms.TextInput(attrs={'class': 'form-control'}))
 
    password1 = forms.CharField(label="密码", max_length=256,
widget=forms.PasswordInput(attrs={'class': 'form-control'}))
 
    password2 = forms.CharField(label="确认密码", max_length=256,
widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class StuInfoForm(forms.Form):
    stu_name = forms.CharField(label="学生姓名",max_length=20, 
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    gender = forms.CharField(label='性别',max_length=10, 
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_num = forms.CharField(label="电话号码",max_length=20, 
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(label="电子邮箱地址",max_length=64, 
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    grade = forms.CharField(label="年级",max_length=16, 
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    major = forms.CharField(label="专业",max_length=30, 
                            widget=forms.TextInput(attrs={'class': 'form-control'}))

class MaInfoForm(forms.Form):
    name = forms.CharField(label="管理员姓名",max_length=20, 
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    gender = forms.CharField(label='性别',max_length=10, 
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_num = forms.CharField(label="电话号码",max_length=20, 
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(label="电子邮箱地址",max_length=64, 
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    
class MaInfoForm_id(forms.Form):
    id = forms.CharField(label="工号", max_length=20,
                           widget=forms.HiddenInput())
    name = forms.CharField(label="管理员姓名",max_length=20, 
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    gender = forms.CharField(label='性别',max_length=10, 
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_num = forms.CharField(label="电话号码",max_length=20, 
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(label="电子邮箱地址",max_length=64, 
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    
class StuInfoForm_id(forms.Form):
    id = forms.CharField(label="学号", max_length=20,
                           widget=forms.HiddenInput())
    stu_name = forms.CharField(label="学生姓名",max_length=20, 
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    gender = forms.CharField(label='性别',max_length=10, 
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_num = forms.CharField(label="电话号码",max_length=20, 
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(label="电子邮箱地址",max_length=64, 
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    grade = forms.CharField(label="年级",max_length=16, 
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    major = forms.CharField(label="专业",max_length=30, 
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    
class Search_Form(forms.Form):
    message = forms.CharField(label="搜索", max_length=200,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    
class Book_Form(forms.Form):
    bid = forms.CharField(label="bid", max_length=20,
                          widget=forms.TextInput(attrs={'class': 'form-control'}))
    isbn = forms.CharField(label='ISBN', max_length=20, 
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    bname = forms.CharField(label='书名',max_length=100, 
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    author = forms.CharField(label='作者',max_length=100, 
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    publisher = forms.CharField(label='出版社',max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    publish_date = forms.DateField(label='出版日期', widget=forms.DateInput(attrs={'type':'date'}))
    btype = forms.CharField(label='类型',max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    inventory = forms.IntegerField(label='库存')
    store_loc = forms.CharField(label='存放位置',max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    book_pic = forms.ImageField(label='图片',required=False) #mysql数据库中存储图片的路径

class Book_Form_edit(forms.Form):
    bid = forms.CharField(label="bid", max_length=20,
                          widget=forms.HiddenInput())
    isbn = forms.CharField(label='ISBN', max_length=20, 
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    bname = forms.CharField(label='书名',max_length=100, 
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    author = forms.CharField(label='作者',max_length=100, 
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    publisher = forms.CharField(label='出版社',max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    publish_date = forms.DateField(label='出版日期', widget=forms.DateInput(attrs={'type':'date'}))
    btype = forms.CharField(label='类型',max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    inventory = forms.IntegerField(label='库存')
    store_loc = forms.CharField(label='存放位置',max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    book_pic = forms.ImageField(label='图片',required=False) #mysql数据库中存储图片的路径