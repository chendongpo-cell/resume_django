# -*- coding: utf-8 -*-
# from django.http import HttpResponse
import os

from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives

from django.utils.http import urlquote
import json
import uuid
from resume_django import settings
from django.http import HttpResponse
from docxtpl import DocxTemplate, Listing
import xlsxwriter

import pymongo
myclient = pymongo.MongoClient("mongodb://localhost:27017/")

def send_email(request):
    if request.method == "POST":
        email= request.POST.get('email')
        name = request.POST.get('name')
    if email:
        if email=='---':
            result = {'state': 0, 'reponse': '邮箱号不能为空'}
            # json返回为中文
            return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")
        else:
            try:
                # 'dongpo.chen@Pactera.com', '898008559@qq.com', '208177808@qq.com',
                #收件人的email，如果需要多人发送以列表形式填写
                email_list = []
                #将发送候选人的邮箱号添加到发送列表
                email_list.append(email)

                interest_url = "http://127.0.0.1:8000/shows/interest?useremail="
                new_interest_url=('%s%s%s%s' % (interest_url, email,'&username=',name))
                uninterested_url = "http://127.0.0.1:8000/shows/uninterested?useremail="
                new_uninterested_url=('%s%s%s%s' % (uninterested_url, email,'&username=',name))
                html_message = '<html>' \
                                    '<head></head>' \
                                    '<body>' \
                                        '<p>您好,我是文思海辉HR<br> ' \
                                            '您的简历与我们公司相关岗位非常匹配，请问您有兴趣接受我们的面试邀请吗？<br> ' \
                                            '请点击右边选项进行反馈：&nbsp; <a href='+new_interest_url+'>感兴趣？</a> &nbsp;&nbsp;&nbsp; <a href='+new_uninterested_url+'>不感兴趣？</a>' \
                                        '</p> ' \
                                    '</body>' \
                                '</html>'
                res = EmailMultiAlternatives('您好，我是文思海辉HR',
                                html_message,
                                'dongpo.chen@Pactera.com',
                                email_list)
                res.content_subtype = 'html'
                result = res.send()
                # print(result)
                if result==1:
                    result = {'state': 0, 'reponse': '邮件发送成功'}
                    # json返回为中文
                    return HttpResponse(json.dumps(result, ensure_ascii=False),content_type="application/json,charset=utf-8")

                else:
                    result = {'state': 0, 'reponse': '邮件发送失败'}
                    # json返回为中文
                    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")
            except:
                return HttpResponse('邮件发送失败')


def interest(request):
    username = request.GET['username']
    useremail = request.GET['useremail']
    # 创建数据库
    mydb = myclient["resume_data"]
    # 创建集合（相当于表）
    mycol = mydb["resume_interest"]
    import time
    time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    # 插入数据
    interest_data={'姓名':username,'邮箱号':useremail,'时间':time}
    mycol.insert_one(interest_data)
    # 获取感兴趣者邮箱
    return HttpResponse("谢谢您的反馈，稍后给您具体邮件通知")


    # return render(request, 'email_collect.html')

def uninterested(request):
    username = request.GET['username']
    useremail = request.GET['useremail']
    result={'姓名':username,'邮箱':useremail}
    # 创建数据库
    mydb = myclient["resume_data"]
    # 创建集合（相当于表）
    mycol = mydb["resume_uninterest"]
    # 插入数据
    mycol.insert_one(result)
    return HttpResponse("非常遗憾，打扰了")


def look_database(request):
    # 数据库
    db_collection = myclient['resume_data']  # 每个数据库包含多个集合，根据集合名称获取集合对象（Collection）
    # 获取集合
    table = db_collection['resume_interest']

    # 查询集合中所有数据,find() 方法可以查询集合中的所有数据，类似 SQL 中的 SELECT * 操作。
    interested_person=table.find()
    return render(request, 'database_show.html', {'interested_person': interested_person})

#获取下载文件路径
def get_path(request):
    #获取请求参数（图片存储位置）
    if request.method == "POST":
        template_type=request.POST.get('template_type')
        resume_data={}
        resume_data['name']=request.POST.get('name')
        resume_data['gender'] = request.POST.get('gender')
        resume_data['birthdata'] = request.POST.get('birthdata')
        resume_data['first_address'] = request.POST.get('first_address')
        resume_data['english'] = request.POST.get('english')
        resume_data['years_working'] = request.POST.get('years_working')

        resume_data['email'] = request.POST.get('email')
        resume_data['phone'] = request.POST.get('phone')
        resume_data['university'] = request.POST.get('university')
        resume_data['major'] = request.POST.get('major')
        resume_data['education'] = request.POST.get('education')
        resume_data['now_address'] = request.POST.get('now_address')
        #判断对方点击的模板类型
        if template_type=='Word模板':
            resume_data['education_experience'] = Listing(request.POST.get('education_experience').strip())
            resume_data['skills'] = Listing(request.POST.get('skills').strip())
            resume_data['work_experience'] = Listing(request.POST.get('work_experience').strip())
            resume_data['projects_experience'] = Listing(request.POST.get('projects_experience').strip())
            resume_data['my_rewards'] = Listing(request.POST.get('my_rewards').strip())
            resume_data['my_introduction'] = Listing(request.POST.get('my_introduction').strip())
            resume_data['additional_information'] = Listing(request.POST.get('additional_information').strip())

            path_name,file_name=create_word(resume_data)
            result = {'state': 0, 'path_name': path_name, 'file_name': file_name}
            return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")
        elif template_type=='Excel模板':
            resume_data['education_experience'] = request.POST.get('education_experience').strip()
            resume_data['skills'] = request.POST.get('skills').strip()
            resume_data['work_experience'] = request.POST.get('work_experience').strip()
            resume_data['projects_experience'] = request.POST.get('projects_experience').strip()
            resume_data['my_rewards'] = request.POST.get('my_rewards').strip()
            resume_data['my_introduction'] = request.POST.get('my_introduction').strip()
            resume_data['additional_information'] = request.POST.get('additional_information').strip()

            path_name,file_name=create_excel(resume_data)
            result = {'state': 0, 'path_name': path_name, 'file_name': file_name}
            return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")

#将json数据生成excel
def create_excel(resume_data):
    out_file_name = '{}{}{}.{}'.format(resume_data['name'],'-',uuid.uuid4().hex[:6], 'xlsx')
    excel_path=os.path.join(settings.MEDIA_ROOT,'create_files',out_file_name)
    # 注意：xlsxwriter 只能创建新文件，不可以修改原有文件。如果创建新文件时与原有文件同名，则会覆盖原有文件
    workbook = xlsxwriter.Workbook(excel_path)  # 新建文件

    worksheet = workbook.add_worksheet(resume_data['name'])  # 新建sheet

    # format = workbook.add_format()
    # format.set_font_size(6)
    worksheet.set_column('A:F', 20)

    bold = workbook.add_format({'bold': True})

    merge_format = workbook.add_format({
        'bold': True,
        'border': 6,
        'align': 'center',  # 水平居中
        'valign': 'vcenter',  # 垂直居中
        'fg_color': '#D7E4BC',  # 颜色填充
    })
    worksheet.merge_range('A1:F1', '基本信息', merge_format)
    worksheet.set_row(0, 20)

    style = workbook.add_format({
        # "fg_color": "yellow",  # 单元格的背景颜色
        'font_size': 10,
        "bold": 1,  # 字体加粗
        "align": "center",  # 对齐方式
        "valign": "vcenter",  # 字体对齐方式
        "font_color": "black"  # 字体颜色
    })
    style2 = workbook.add_format({
        # "fg_color": "yellow",  # 单元格的背景颜色
        'font_size': 10,
        # "bold": 1,  # 字体加粗
        "align": "center",  # 对齐方式
        "valign": "vcenter",  # 字体对齐方式
        "font_color": "black"  # 字体颜色
    })

    worksheet.write('A2', '姓名', style)  # 测试插入数据
    worksheet.write('B2', resume_data['name'], style2)  # 测试插入数据
    worksheet.write('C2', '性别', style)  # 测试插入数据
    worksheet.write('D2', resume_data['gender'], style2)  # 测试插入数据
    worksheet.write('E2', '出生年月', style)  # 测试插入数据
    worksheet.write('F2', resume_data['birthdata'], style2)  # 测试插入数据
    worksheet.set_row(1, 20)

    worksheet.write('A3', '户籍所在地', style)  # 测试插入数据
    worksheet.write('B3', resume_data['first_address'], style2)  # 测试插入数据
    worksheet.write('C3', '英语水平', style)  # 测试插入数据
    worksheet.write('D3', resume_data['english'], style2)  # 测试插入数据
    worksheet.write('E3', '工作年限', style)  # 测试插入数据
    worksheet.write('F3', resume_data['years_working'], style2)  # 测试插入数据
    worksheet.set_row(2, 20)

    worksheet.write('A4', '邮箱地址', style)  # 测试插入数据
    worksheet.write('B4', resume_data['email'], style2)  # 测试插入数据
    worksheet.write('C4', '手机号码', style)  # 测试插入数据
    worksheet.write('D4', resume_data['phone'], style2)  # 测试插入数据
    worksheet.write('E4', '毕业院校', style)  # 测试插入数据
    worksheet.write('F4', resume_data['university'], style2)  # 测试插入数据
    worksheet.set_row(3, 20)

    worksheet.write('A5', '专业', style)  # 测试插入数据
    worksheet.write('B5', resume_data['major'], style2)  # 测试插入数据
    worksheet.write('C5', '学历', style)  # 测试插入数据
    worksheet.write('D5', resume_data['education'], style2)  # 测试插入数据
    worksheet.write('E5', '现居住地址', style)  # 测试插入数据
    worksheet.write('F5', resume_data['now_address'], style2)  # 测试插入数据
    worksheet.set_row(4, 20)

    # 教育经历
    merge_format = workbook.add_format({
        'bold': True,
        'border': 6,
        'align': 'center',  # 水平居中
        'valign': 'vcenter',  # 垂直居中
        'fg_color': '#D7E4BC',  # 颜色填充
    })
    worksheet.merge_range('A6:F6', '教育经历', merge_format)
    worksheet.set_row(5, 20)
    merge_format = workbook.add_format({
        'font_size': 10,
        'align': 'left',
        'valign': 'top',  # 垂直居中
        'text_wrap': 1
    })
    worksheet.merge_range('A7:F7', resume_data['education_experience'], merge_format)
    worksheet.set_row(6, 150)  # 设置第8行的高度为30

    # 技能专长
    merge_format = workbook.add_format({
        'bold': True,
        'border': 6,
        'align': 'center',  # 水平居中
        'valign': 'vcenter',  # 垂直居中
        'fg_color': '#D7E4BC',  # 颜色填充
    })
    worksheet.merge_range('A8:F8', '技能专长', merge_format)
    worksheet.set_row(7, 20)
    merge_format = workbook.add_format({
        'font_size': 10,
        'align': 'left',
        'valign': 'top',  # 垂直居中
        'text_wrap': 1
    })
    worksheet.merge_range('A9:F9', resume_data['skills'], merge_format)
    worksheet.set_row(8, 200)  # 设置第8行的高度为30

    # 工作经历
    merge_format = workbook.add_format({
        'bold': True,
        'border': 6,
        'align': 'center',  # 水平居中
        'valign': 'vcenter',  # 垂直居中
        'fg_color': '#D7E4BC',  # 颜色填充
    })
    worksheet.merge_range('A10:F10', '工作经历', merge_format)
    worksheet.set_row(9, 20)
    merge_format = workbook.add_format({
        'font_size': 10,
        'align': 'left',
        'valign': 'top',  # 垂直居中
        'text_wrap': 1
    })
    worksheet.merge_range('A11:F11', resume_data['work_experience'], merge_format)
    worksheet.set_row(10, 200)  # 设置第8行的高度为30

    # 项目经历
    merge_format = workbook.add_format({
        'bold': True,
        'border': 6,
        'align': 'center',  # 水平居中
        'valign': 'vcenter',  # 垂直居中
        'fg_color': '#D7E4BC',  # 颜色填充
    })
    worksheet.merge_range('A12:F12', '项目经历', merge_format)
    worksheet.set_row(11, 20)
    merge_format = workbook.add_format({
        'font_size': 10,
        'align': 'left',
        'valign': 'top',  # 垂直居中
        'text_wrap': 1
    })
    worksheet.merge_range('A13:F13', resume_data['projects_experience'], merge_format)
    worksheet.set_row(12, 300)  # 设置第8行的高度为30

    # 证书奖项
    merge_format = workbook.add_format({
        'bold': True,
        'border': 6,
        'align': 'center',  # 水平居中
        'valign': 'vcenter',  # 垂直居中
        'fg_color': '#D7E4BC',  # 颜色填充
    })
    worksheet.merge_range('A14:F14', '证书奖项', merge_format)
    worksheet.set_row(13, 20)
    merge_format = workbook.add_format({
        'font_size': 10,
        'align': 'left',
        'valign': 'top',  # 垂直居中
        'text_wrap': 1
    })
    worksheet.merge_range('A15:F15', resume_data['my_rewards'], merge_format)
    worksheet.set_row(14, 150)  # 设置第8行的高度为30

    # 自我评价
    merge_format = workbook.add_format({
        'bold': True,
        'border': 6,
        'align': 'center',  # 水平居中
        'valign': 'vcenter',  # 垂直居中
        'fg_color': '#D7E4BC',  # 颜色填充
    })
    worksheet.merge_range('A16:F16', '自我评价', merge_format)
    worksheet.set_row(15, 20)
    merge_format = workbook.add_format({
        'font_size': 10,
        'align': 'left',
        'valign': 'top',  # 垂直居中
        'text_wrap': 1
    })
    worksheet.merge_range('A17:F17', resume_data['my_introduction'], merge_format)
    worksheet.set_row(16, 150)  # 设置第8行的高度为30

    # 补充信息
    merge_format = workbook.add_format({
        'bold': True,
        'border': 6,
        'align': 'center',  # 水平居中
        'valign': 'vcenter',  # 垂直居中
        'fg_color': '#D7E4BC',  # 颜色填充
    })
    worksheet.merge_range('A18:F18', '补充信息', merge_format)
    worksheet.set_row(17, 20)
    merge_format = workbook.add_format({
        'font_size': 10,
        'align': 'left',
        'valign': 'top',  # 垂直居中
        'text_wrap': 1
    })
    worksheet.merge_range('A19:F19', resume_data['additional_information'], merge_format)
    worksheet.set_row(18, 150)  # 设置第8行的高度为30
    workbook.close()  # 保存并关闭
    return excel_path, out_file_name


#将json数据利用word模板生成docx
def create_word(resume_data):
    resume_template_path=os.path.join(settings.MEDIA_ROOT,'resume_template','resume_template.docx')
    doc = DocxTemplate(resume_template_path)  # 加载模板文件
    out_file_name = '{}{}{}.{}'.format(resume_data['name'], '-', uuid.uuid4().hex[:6], 'docx')
    out_file_path=os.path.join(settings.MEDIA_ROOT,'create_files',out_file_name)
    doc.render(resume_data, autoescape=True)  # 填充数据
    doc.save(out_file_path)  # 保存目标文件
    return out_file_path,out_file_name

#下载文件
def download_files(request):
    if request.method == "POST":
        path_name = request.POST.get('path_name')
        file_name = request.POST.get('file_name')

        file = open(path_name, 'rb')
        response = HttpResponse(file)
        response['Content-Type'] = 'application/octet-stream'  # 设置头信息，告诉浏览器这是个文件
        response['Content-Disposition'] = 'attachment;filename="%s"'%(urlquote(file_name))
        return response

# from django.utils.http import urlquote
# file_name_chinese = obj.files.first().name
# response['Content-Disposition'] = 'attachment;filename="%s"'%(urlquote(file_name_chinese))
#
# outfile = open(filename, "rb")
# response = FileResponse(outfile)
# response['Content-Type'] = 'application/octet-stream'
# response['Content-Disposition'] = 'attachment;filename="%s"' % obj.files.first().name
# return response
#
#
# outfile = open(filename, "rb")
#             response = FileResponse(outfile)
#             response['Content-Type'] = 'application/octet-stream'
#             from django.utils.http import urlquote
#             file_name_chinese = obj.files.first().name
#             response['Content-Disposition'] = 'attachment;filename="%s"'%(urlquote(file_name_chinese))
#             print(obj.files.first().name)
#             return response
