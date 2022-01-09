from django.urls import path
from resume_shows import views

urlpatterns = [
    # 邮件发送模块
    path('email/', views.send_email),
    path('interest/', views.interest),
    path('uninterested/', views.uninterested),
    # mongodb数据库
    path('database/', views.look_database),
    # 导出pdf和word模块
    path('getpath/', views.get_path),
    path('download/', views.download_files),
]
