from django.urls import path
from resume_extract import views

#定义实例命名空间需要同时定义应用命名空间，否则会报错，定义应用命名空间有两种方法，
#第一种方法
# app_name = 'goods'
#第二种方法
# path('', include(('goods.urls', 'goods'), namespace='goods')),

urlpatterns = [
    path('', views.index, name='index'),  # 首页
    path('upload/', views.upload_resume),  # 简历上传
    path('resume_path/', views.resume_path),  # 新的简历路径
    path('resume/', views.resume_parse),  # 简历解析并展示

]
