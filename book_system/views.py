from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from book_system import models
from .myforms import UserForm, RegisterForm, StuInfoForm, MaInfoForm, ManagerRegisterForm, MaInfoForm_id, StuInfoForm_id, Search_Form, Book_Form, Book_Form_edit
import hashlib
from django.utils.encoding import smart_str
from django.forms import formset_factory
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from django.db import transaction  # 事务处理
from datetime import date,datetime,timedelta

def hash_code(s, salt='sql_lab2'):# 加盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()

# Create your views here.
def index(request):
    if not request.session.get('is_login',None):
        return render(request,'user/index.html')
    request.session['is_high_manager'] = 0
    if request.session.get('is_manager',None):
        try:
            high_manager = models.HighManager.manager.objects.get(manager_id=request.session.get('user_id',None))
            request.session['is_high_manager'] = 1
        except:
            request.session['is_high_manager'] = 0
            #message = "没有访问权限"
    return render(request,'user/index.html')

def login(request):
    if request.session.get('is_login',None):
        return redirect('/user/index')

    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(id=username)
                # 哈希值和数据库内的值进行比对
                if smart_str(user.password) == hash_code(password):
                #if user.password == hash_code(password):
                #if user.password == password:
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['is_manager'] = user.is_manager
                   
                    #request.session['user_name'] = user.name
                    return redirect('/user/index/')
                else:
                    message = "密码不正确_" + smart_str(password)
            except:
                message = "用户不存在！"                 
        return render(request, 'user/login.html', locals())
  
    login_form = UserForm()
    return render(request, 'user/login.html', locals())
  
def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。
        return redirect("/user/index/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'user/register.html', locals())
            else:
                same_id_user = models.User.objects.filter(id=username)
                print(username)

                if same_id_user:  # id唯一
                    message = '此id已注册！'
                    return render(request, 'user/register.html', locals())
  
                # 当一切都OK的情况下，创建新用户  
                new_user = models.User(id = username,is_manager = 0,password = hash_code(password1))
                #new_user.id = username
                #new_user.is_manager = 0
                # 使用加密密码
                #new_user.password = hash_code(password1)
                # new_user.password = password1
                new_user.save()
                new_stu = models.Student(stu_id = username)
                #new_stu.stu_id = username
                new_stu.save()
                return redirect('/user/login/')  # 自动跳转到登录页面
    register_form = RegisterForm()
    return render(request, 'user/register.html', locals())
  
def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/user/login")
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/user/login")

def userinfo(request):
    if request.method == 'GET':
        # 获取用户数据到user_info(管理员/学生)
        if not request.session.get('is_login', None):
            return redirect("/user/login")
        user_id = request.session.get('user_id', None)
        user = models.User.objects.get(id=user_id)
        request.session['is_manager'] = user.is_manager
        if user.is_manager:
            user_info = models.BookManager.objects.get(manager_id=user_id)
            request.session['manager_name'] = user_info.manager_name
            request.session['gender'] = user_info.gender
            request.session['phone_num'] = user_info.phone_num
            request.session['email'] = user_info.email
            forms = MaInfoForm(initial={
            'name': user_info.manager_name,
            'gender': user_info.gender,
            'phone_num': user_info.phone_num,
            'email': user_info.email,
        })
        else:
            user_info = models.Student.objects.get(stu_id=user_id)
            request.session['stu_name'] = user_info.stu_name
            request.session['gender'] = user_info.gender
            request.session['phone_num'] = user_info.phone_num
            request.session['email'] = user_info.email
            request.session['grade'] = user_info.grade
            request.session['major'] = user_info.major
            forms = StuInfoForm(initial={
            'stu_name': user_info.stu_name,
            'gender': user_info.gender,
            'phone_num': user_info.phone_num,
            'email': user_info.email,
            'grade': user_info.grade,
            'major': user_info.major,
            })
        return render(request, 'user/userinfo.html', {"forms": forms})     
    if request.method == 'POST':
        data = request.POST
        if request.session['is_manager']:
            forms = MaInfoForm(data)
        else:
            forms = StuInfoForm(data)
        if forms.is_valid():
            if request.session['is_manager']:
                user_id = request.session.get('user_id', None)
                manager = models.BookManager.objects.get(manager_id=user_id)
                manager.manager_name = forms.cleaned_data['name']
                manager.gender = forms.cleaned_data['gender']
                manager.phone_num = forms.cleaned_data['phone_num']
                manager.email = forms.cleaned_data['email']
                manager.save()
            else:
                user_id = request.session.get('user_id', None)
                stu = models.Student.objects.get(stu_id=user_id)
                stu.stu_name = forms.cleaned_data['stu_name']
                stu.gender = forms.cleaned_data['gender']
                stu.phone_num = forms.cleaned_data['phone_num']
                stu.email = forms.cleaned_data['email']
                stu.grade = forms.cleaned_data['grade']
                stu.major = forms.cleaned_data['major']
                stu.save()
            return JsonResponse({"status": True})  
        else:
            return JsonResponse({"status": False, "errors": forms.errors})
    return render(request, 'user/userinfo.html')

@csrf_exempt
def managerinfo(request):
    request.session['is_high_manager'] = 0
    if request.session.get('is_manager',None):
        #high_manager = models.HighManager.objects.get(manager_id=request.session.get('user_id',None))
        try:
            high_manager = models.HighManager.objects.get(manager_id=request.session.get('user_id',None))
            request.session['is_high_manager'] = 1
        except:
            request.session['is_high_manager'] = 0
    if request.method == "POST":
        ma_infoform = MaInfoForm_id(request.POST)
        if ma_infoform.is_valid():
            id = ma_infoform.cleaned_data['id']
            manager = models.BookManager.objects.get(manager_id=id)
            manager.manager_name = ma_infoform.cleaned_data['name']
            manager.gender = ma_infoform.cleaned_data['gender']
            manager.phone_num = ma_infoform.cleaned_data['phone_num']
            manager.email = ma_infoform.cleaned_data['email']
            manager.save()
    #ma_infoform = MaInfoForm()
    #Ma_model_form=MaInfoForm
    #Ma_form_set=formset_factory(form=Ma_model_form)
    context = dict()
    ma_infos = models.BookManager.objects.all()
    all_info = []
    #context['result'] = ma_infos
    for info in ma_infos:
        #form_name = info.manager_id
        form_info = MaInfoForm_id(initial={
            'id':info.manager_id,
            'name': info.manager_name,
            'gender': info.gender,
            'phone_num': info.phone_num,
            'email': info.email,
        })
        all_info.append({'info' : info,'forms' : form_info})
    #ma_info_formset = Ma_form_set(initial = formset_initial)
    context['all_info'] = all_info
    return render(request, 'user/managerinfo.html', context)

@csrf_exempt
def stuinfo(request):
    if request.method == "POST":
        ma_infoform = StuInfoForm_id(request.POST)
        if ma_infoform.is_valid():
            id = ma_infoform.cleaned_data['id']
            manager = models.Student.objects.get(stu_id=id)
            manager.stu_name = ma_infoform.cleaned_data['stu_name']
            manager.gender = ma_infoform.cleaned_data['gender']
            manager.phone_num = ma_infoform.cleaned_data['phone_num']
            manager.email = ma_infoform.cleaned_data['email']
            manager.grade = ma_infoform.cleaned_data['grade']
            manager.major = ma_infoform.cleaned_data['major']
            manager.save()
    #ma_infoform = MaInfoForm()
    #Ma_model_form=MaInfoForm
    #Ma_form_set=formset_factory(form=Ma_model_form)
    context = dict()
    ma_infos = models.Student.objects.all()
    all_info = []
    #context['result'] = ma_infos
    for info in ma_infos:
        #form_name = info.manager_id
        form_info = StuInfoForm_id(initial={
            'id':info.stu_id,
            'stu_name': info.stu_name,
            'gender': info.gender,
            'phone_num': info.phone_num,
            'email': info.email,
            'grade': info.grade,
            'major': info.major,
        })
        all_info.append({'info' : info,'forms' : form_info})
    #ma_info_formset = Ma_form_set(initial = formset_initial)
    context['all_info'] = all_info
    return render(request, 'user/stuinfo.html', context)

@csrf_exempt
def bookinfo(request):
    if request.method == "POST":
        search = Search_Form(request.POST)
        if search.is_valid():
            with connection.cursor() as cursor:
                cursor.execute("SELECT search_book(%s)", [search.cleaned_data['message']])
                result = cursor.fetchone()
            #print(result[0])
            if result[0]:
                temp_id = result[0].split(',')
                book_info = []
                for bid in temp_id:
                    book = models.BookInfo.objects.get(bid = bid)
                    book_info.append(book)
                return render(request,'user/bookinfo.html', {'search' : search , 'book_info' : book_info})
    search = Search_Form()
    return render(request,'user/bookinfo.html', {'search' : search})

@csrf_exempt
def manager_delete(request,id):
    if request.method == "POST":
        temp = 0
        with connection.cursor() as cursor:
            results = cursor.callproc('delete_user', (id,temp,))
            #results = cursor.fetchall()
            print(results)
        if results[1] == 1:
            message = "不能删除high_manager"
            return render(request, 'user/managerdelete.html', {'id' : id , 'message' : message})
        elif results[1] == 2:
            message = "没有对应id"
            return render(request, 'user/managerdelete.html', {'id' : id , 'message' : message})
        else:
            message = "删除成功"
            return redirect('/user/managerinfo')
            #return render(request, 'user/managerdelete.html', {'id' : id , 'message' : message})

    return render(request, 'user/managerdelete.html', {'id' : id})

@csrf_exempt
def stu_delete(request,id):
    if request.method == "POST":
        temp = 0
        borrow = models.Borrow.objects.filter(stu_id = id)
        if borrow:
            message = "存在借阅信息，不能删除"
            return render(request, 'user/studelete.html', {'id' : id , 'message' : message})
        with connection.cursor() as cursor:
            results = cursor.callproc('delete_user', (id,temp,))
            #results = cursor.fetchall()
            print(results)
        if results[1] == 1:
            message = "不能删除high_manager"
            return render(request, 'user/studelete.html', {'id' : id , 'message' : message})
        elif results[1] == 2:
            message = "没有对应id"
            return render(request, 'user/studelete.html', {'id' : id , 'message' : message})
        else:
            message = "删除成功"
            return redirect('/user/stuinfo')
            #return render(request, 'user/studelete.html', {'id' : id , 'message' : message})

    return render(request, 'user/studelete.html', {'id' : id})

def manager_register(request):
    #和register类似
    if request.method == "POST":
        register_form = ManagerRegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'user/manager_register.html', locals())
            else:
                same_id_user = models.User.objects.filter(id=username)
                print(username)

                if same_id_user:  # id唯一
                    message = '此id已注册！'
                    return render(request, 'user/manager_register.html', locals())
  
                # 当一切都OK的情况下，创建新用户(管理员)
                new_user = models.User(id = username,is_manager = 1,password = hash_code(password1))
                #new_user.id = username
                #new_user.is_manager = 0
                # 使用加密密码
                #new_user.password = hash_code(password1)
                # new_user.password = password1
                new_user.save()
                new_manager = models.BookManager(manager_id = username)
                #new_stu.stu_id = username
                new_manager.save()
                ma_info = models.BookManager.objects.all()
                return redirect('/user/managerinfo')
    register_form = ManagerRegisterForm()
    return render(request, 'user/manager_register.html', locals())

def stu_register(request):
    #和register类似
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'user/stu_register.html', locals())
            else:
                same_id_user = models.User.objects.filter(id=username)
                print(username)

                if same_id_user:  # id唯一
                    message = '此id已注册！'
                    return render(request, 'user/stu_register.html', locals())
  
                # 当一切都OK的情况下，创建新用户(学生)
                new_user = models.User(id = username,is_manager = 0,password = hash_code(password1))
                #new_user.id = username
                #new_user.is_manager = 0
                # 使用加密密码
                #new_user.password = hash_code(password1)
                # new_user.password = password1
                new_user.save()
                new_manager = models.Student(stu_id = username)
                #new_stu.stu_id = username
                new_manager.save()
                return redirect('/user/stuinfo')
    register_form = RegisterForm()
    return render(request, 'user/stu_register.html', locals())

def bookadd(request):
    if request.method == "POST":
        book = Book_Form(request.POST, request.FILES or None)
        if book.is_valid():
            bid = book.cleaned_data['bid']
            same_id_book = models.BookInfo.objects.filter(bid=bid)
            if same_id_book:
                message = "已存在此id"
                return render(request, 'user/bookadd.html', {'forms' : book , 'message' : message})
            new_book = models.BookInfo(
                bid = bid,
                isbn = book.cleaned_data['isbn'],
                bname = book.cleaned_data['bname'],
                author = book.cleaned_data['author'],
                publisher = book.cleaned_data['publisher'],
                publish_date = book.cleaned_data['publish_date'],
                btype = book.cleaned_data['btype'],
                inventory = book.cleaned_data['inventory'],
                store_loc = book.cleaned_data['store_loc'],
                book_pic = book.cleaned_data['book_pic'],
            )
            new_book.save()
            message = "添加成功！"
            book = Book_Form()
            return render(request, 'user/bookadd.html', {'forms' : book , 'message' : message})
    book = Book_Form()
    return render(request, 'user/bookadd.html', {'forms' : book})

@csrf_exempt
def book_delete(request,bid):
    if request.method == "POST":
        bid_borrow = models.Borrow.objects.filter(bid = bid)
        bid_reserve = models.Reserve.objects.filter(bid = bid)
        if bid_borrow or bid_reserve:
            message = '此书有人借阅/预定'
            return render(request, 'user/book_delete.html', {'bid' : bid , 'message' : message})
        try:
            book = models.BookInfo.objects.get(bid = bid)
            book.delete()
            message = '成功删除'
            return render(request, 'user/book_delete.html', {'bid' : bid , 'message' : message})
        except:
            message = '不存在此书'
            return render(request, 'user/book_delete.html', {'bid' : bid , 'message' : message})
        

    return render(request, 'user/book_delete.html', {'bid' : bid})

def book_change(request,bid):
    if request.method == "POST":
        book = Book_Form_edit(request.POST, request.FILES or None)
        print(request.POST)
        if book.is_valid():
            print(book.cleaned_data['bid'])
            bid = book.cleaned_data['bid']
            book_model = models.BookInfo.objects.get(bid = bid)
            book_model.isbn = book.cleaned_data['isbn']
            book_model.bname = book.cleaned_data['bname']
            book_model.author = book.cleaned_data['author']
            book_model.publisher = book.cleaned_data['publisher']
            book_model.publish_date = book.cleaned_data['publish_date']
            book_model.btype = book.cleaned_data['btype']
            book_model.inventory = book.cleaned_data['inventory']
            book_model.store_loc = book.cleaned_data['store_loc']
            book_model.book_pic = book.cleaned_data['book_pic']
            book_model.save()
            message = "修改成功！"
            bookform = Book_Form_edit(initial={
                'bid' : book_model.bid,
                'isbn' : book_model.isbn,
                'bname' : book_model.bname,
                'author' : book_model.author,
                'publisher' : book_model.publisher,
                'publish_date' : book_model.publish_date,
                'btype' : book_model.btype,
                'inventory' : book_model.inventory,
                'store_loc' : book_model.store_loc,
                'book_pic' : book_model.book_pic
                }
            )
            return render(request, 'user/book_change.html', {'bid' : bid,'forms' : bookform , 'message' : message})
    book = models.BookInfo.objects.get(bid = bid)
    bookform = Book_Form_edit(initial={
        'bid' : book.bid,
        'isbn' : book.isbn,
        'bname' : book.bname,
        'author' : book.author,
        'publisher' : book.publisher,
        'publish_date' : book.publish_date,
        'btype' : book.btype,
        'inventory' : book.inventory,
        'store_loc' : book.store_loc,
        'book_pic' : book.book_pic
        }
    )
    return render(request,'user/book_change.html', {'bid' : bid,'forms' : bookform})


@csrf_exempt
@transaction.atomic
def book_borrow(request,bid):
    if request.method == "POST":
      # 开启事务
      save_point = transaction.savepoint()
      try:
        book = models.BookInfo.objects.get(bid = bid)
        book_reserve = models.Reserve.objects.filter(bid = bid)
        book_al = models.Borrow.objects.filter(bid = bid , stu_id = request.session.get('user_id',None) , return_date__isnull = True)
        book_violation = models.Violation.objects.filter(stu_id = request.session.get('user_id',None))
        if book.inventory - book_reserve.count() <= 0:
            message = "无库存剩余！(被全部预定/借出)"
            return render(request, 'user/book_borrow.html', {'message' : message ,'bid' : bid})
        elif book_violation:
            message = "存在借阅违期信息，请先还书！"
            return render(request, 'user/bookreserve_borrow.html', {'message' : message ,'bid' : bid})
        elif book_al:
            message = "已借阅！"
            return render(request, 'user/book_borrow.html', {'message' : message ,'bid' : bid})
        else:
            temp_borrow = models.Borrow.objects.all().count()
            new_borrow = models.Borrow(
                id = 'borrow_' + str(temp_borrow+1),
                stu_id = request.session.get('user_id',None),
                bid = bid,
                borrow_date = date.today(),
                due_date = date.today() + timedelta(days = 2*30) #借书时限为两个月
            )
            new_borrow.save()
            transaction.savepoint_commit(save_point)
            message = "借书成功！"
            return render(request, 'user/book_borrow.html', {'message' : message ,'bid' : bid})
      except:
        message = "借书失败！"
        transaction.savepoint_rollback(save_point)

    return render(request, 'user/book_borrow.html', {'bid' : bid})

@csrf_exempt
def book_reserve(request,bid):
    if request.method == "POST":
        book = models.BookInfo.objects.get(bid = bid)
        book_reserve = models.Reserve.objects.filter(bid = bid)
        book_al = models.Borrow.objects.filter(bid = bid , stu_id = request.session.get('user_id',None),return_date__isnull = True)
        book_al_re = models.Reserve.objects.filter(bid = bid , stu_id = request.session.get('user_id',None))
        if book.inventory - book_reserve.count() <= 0:
            message = "无库存剩余！(被全部预定/借出)"
            return render(request, 'user/book_reserve.html', {'message' : message ,'bid' : bid})
        elif book_al:
            message = "已借阅！"
            return render(request, 'user/book_reserve.html', {'message' : message ,'bid' : bid})
        elif book_al_re:
            message = "已预定！"
            return render(request, 'user/book_reserve.html', {'message' : message ,'bid' : bid})
        else:
            temp_reserve = models.Reserve.objects.all().count()
            new_reserve = models.Reserve(
                id = 'reserve_' + str(temp_reserve+1),
                stu_id = request.session.get('user_id',None),
                bid = bid,
                reserve_date = date.today()
            )
            new_reserve.save()
            message = "预定成功！"
            return render(request, 'user/book_reserve.html', {'message' : message ,'bid' : bid})

    return render(request, 'user/book_reserve.html', {'bid' : bid})

def bookborrowinfo(request):
    id = request.session.get('user_id' , None)
    borrow = models.Borrow.objects.filter(stu_id = id , return_date__isnull = True)
    book_borrow_info = []
    for i in borrow:
        temp_dict = {}
        temp_dict['bid'] = i.bid
        temp_dict['borrow_date'] = i.borrow_date
        temp_dict['due_date'] = i.due_date
        book = models.BookInfo.objects.get(bid = i.bid)
        temp_dict['bname'] = book.bname
        book_borrow_info.append(temp_dict)
    return render(request,'user/bookborrowinfo.html',{'book_borrow_info' : book_borrow_info})
    

def bookreserveinfo(request):
    id = request.session.get('user_id' , None)
    reserve = models.Reserve.objects.filter(stu_id = id)
    book_reserve_info = []
    for i in reserve:
        temp_dict = {}
        temp_dict['bid'] = i.bid
        temp_dict['reserve_Date'] = i.reserve_date
        book = models.BookInfo.objects.get(bid = i.bid)
        temp_dict['bname'] = book.bname
        book_reserve_info.append(temp_dict)
    return render(request,'user/bookreserveinfo.html',{'book_reserve_info' : book_reserve_info})

@csrf_exempt
@transaction.atomic
def book_reserve_borrow(request,bid):
    if request.method == "POST":
        # 开启事务
        save_point = transaction.savepoint()
        try:
            book = models.BookInfo.objects.get(bid = bid)
            book_reserve = models.Reserve.objects.filter(bid = bid)
            book_al = models.Borrow.objects.filter(bid = bid , stu_id = request.session.get('user_id',None) , return_date__isnull = True)
            book_violation = models.Violation.objects.filter(stu_id = request.session.get('user_id',None))
            if book_al:
                message = "已借阅！"
                return render(request, 'user/bookreserve_borrow.html', {'message' : message ,'bid' : bid})
            elif book_violation:
                message = "存在借阅违期信息，请先还书！"
                return render(request, 'user/bookreserve_borrow.html', {'message' : message ,'bid' : bid})
            else:
                temp_borrow = models.Borrow.objects.all().count()
                new_borrow = models.Borrow(
                    id = 'borrow_' + str(temp_borrow+1),
                    stu_id = request.session.get('user_id',None),
                    bid = bid,
                    borrow_date = date.today(),
                    due_date = date.today() + timedelta(days = 2*30) #借书时限为两个月
                )
                new_borrow.save()
                transaction.savepoint_commit(save_point)
                message = "借书成功！"
                return render(request, 'user/bookreserve_borrow.html', {'message' : message ,'bid' : bid})
        except:
                message = "借书失败！"
                transaction.savepoint_rollback(save_point)

    return render(request, 'user/bookreserve_borrow.html', {'bid' : bid})

@csrf_exempt
def book_reserve_cancel(request,bid):
    stu_id = request.session.get('user_id' , None)
    if request.method == "POST":
        try:
            book_reserve = models.Reserve.objects.get(stu_id = stu_id,bid = bid)
            book_reserve.delete()
            message = "已取消预定！"
            return render(request, 'user/bookreserve_cancel.html', {'bid' : bid , 'message' : message})
        except:
            message = "已取消预定！"
            return render(request, 'user/bookreserve_cancel.html', {'bid' : bid , 'message' : message})
    return render(request, 'user/bookreserve_cancel.html', {'bid' : bid})

@csrf_exempt   
def bookreturn(request,bid):
    stu_id = request.session.get('user_id' , None)
    if request.method == "POST":
        try:
            book_borrow = models.Borrow.objects.get(stu_id = stu_id,bid = bid,return_date__isnull = True)
            book_borrow.return_date = date.today()
            book_borrow.save()
            book = models.BookInfo.objects.get(bid = bid)
            book.inventory += 1
            book.save()
        except:
            message = "无借阅信息！"
            return render(request, 'user/book_return.html', {'bid' : bid , 'message' : message})
        try:
            book_vio = models.Violation.objects.get(stu_id = stu_id,bid = bid)
            book_vio.delete()
        except:
            pass
        message = "已还书！"
        return render(request, 'user/book_return.html', {'bid' : bid , 'message' : message})

    return render(request, 'user/book_return.html', {'bid' : bid})