from django.urls import path, include
from book_system import views
from django.contrib import admin
 
app_name = 'book_system'
 
urlpatterns = [
    path('admin', admin.site.urls),
    path('login/', views.login),
    path('index/', views.index),
    path('register/', views.register),
    path('logout/', views.logout),
    path('userinfo/', views.userinfo),
    path('managerinfo/',views.managerinfo),
    path('manager_register/',views.manager_register),
    path('managerinfo/delete/<slug:id>',views.manager_delete),
    path('stuinfo/',views.stuinfo),
    path('stuinfo/delete/<slug:id>',views.stu_delete),
    path('stu_register/',views.stu_register),
    path('bookinfo/',views.bookinfo),
    path('bookadd/',views.bookadd),
    path('bookinfo/delete/<slug:bid>',views.book_delete),
    path('bookinfo/change/<slug:bid>',views.book_change),
    path('bookinfo/borrow/<slug:bid>',views.book_borrow),
    path('bookinfo/reserve/<slug:bid>',views.book_reserve),
    path('bookborrowinfo/',views.bookborrowinfo),
    path('bookreserveinfo/',views.bookreserveinfo),
    path('bookreserveinfo/borrow/<slug:bid>',views.book_reserve_borrow),
    path('bookreserveinfo/cancel/<slug:bid>',views.book_reserve_cancel),
    path('bookborrowinfo/return/<slug:bid>',views.bookreturn),
]