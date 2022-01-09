import json
import uuid

from django.shortcuts import HttpResponse,render,redirect
from resume_django import settings

#自定义模块
from resume_extract.resume_parse.resume_chunk import *
from resume_extract.resume_parse.resume_clean import *
from resume_extract.resume_parse.extract_information import *

# 数据插入到mongodb数据库
# import pymongo
# myclient = pymongo.MongoClient("mongodb://localhost:27017/")

#windows下doc转docx需要包(win32com包windows环境专用,linux环境没有)
try:
    from win32com import client as wc
    from win32com.client import gencache
    from win32com.client import constants, gencache
#linux环境doc以及docx转pdf需要包
except:
    import subprocess
#主页
def index(request):  # index页面需要一开始就加载的内容写在这里
    return render(request, 'index.html')

#windows下word转pdf
def doc_pdf(wordPath, pdfPath):
        """
        word转pdf
        :param wordPath: word文件路径
        :param pdfPath:  生成pdf文件路径
        """
        import pythoncom
        pythoncom.CoInitialize()
        word = gencache.EnsureDispatch('Word.Application')
        doc = word.Documents.Open(wordPath, ReadOnly=1)
        doc.ExportAsFixedFormat(pdfPath,
                                constants.wdExportFormatPDF,
                                Item=constants.wdExportDocumentWithMarkup,
                                CreateBookmarks=constants.wdExportCreateHeadingBookmarks)
        word.Quit(constants.wdDoNotSaveChanges)
        return pdfPath

#简历上传并转化模块，返回转化后的简历路径
def upload_resume(request):
    if request.method == 'POST':
        # 1.获取到用户上传的文件
        file_obj = request.FILES.get('file_name')
        # 获取文件名
        first_file_name = file_obj.name
        path = os.path.join(settings.MEDIA_ROOT, first_file_name)
        # 判断当前路径是否存在，如果存在同名的文件，新建路径
        if os.path.exists(path):
            first_file_name, suffix = first_file_name.split('.')
            first_file_name = '{}-{}.{}'.format(first_file_name, uuid.uuid4().hex[:4], suffix)
            path = os.path.join(settings.MEDIA_ROOT, first_file_name)
        # 从上传文件对象里 一点一点读取数据
        with open(path, 'wb') as f:
            for chunk in file_obj.chunks():
                f.write(chunk)

        if first_file_name.endswith('.pdf'):
            new_file_name=first_file_name
            result = {'state': 0, 'file_name': new_file_name}
        # 直接解析docx，但doc不能直接解析，需要转化为docx，但解析docx时存在邮箱(链接形式)读取不到的情况。
        elif first_file_name.endswith('.docx'):
            # linux下docx转为pdf
            try:
                import subprocess
                #输出路径
                out_path = settings.MEDIA_ROOT
                #原文件路径
                file_path = os.path.join(out_path, first_file_name)
                ##修改原文件得到新文件名字
                new_file_name= first_file_name.split(".")[0] + ".pdf"

                # linux下将docx转化为pdf
                subprocess.check_output(
                    ["soffice", "--headless", "--invisible", "--convert-to", "pdf", file_path, "--outdir", out_path])

                new_file_path=os.path.join(out_path, new_file_name)
                if os.path.exists(new_file_path):
                    result = {'state': 0, 'file_name': new_file_name}
                else:
                    result = {'state': 1, 'file_name': ''}
            # windows可以直接解析docx
            except:
                out_path = settings.MEDIA_ROOT
                # 原文件路径
                file_path = os.path.join(out_path, first_file_name)
                ##修改原文件得到新文件名字
                new_file_name = first_file_name.split(".")[0]+ ".pdf"

                out_file_path = os.path.join(out_path, new_file_name)
                #doc转换pdf
                doc_pdf(file_path,out_file_path)

                if os.path.exists(out_file_path):
                    result = {'state': 0, 'file_name': new_file_name}
                else:
                    result = {'state': 1, 'file_name': ''}

        elif first_file_name.endswith('.doc'):
            try:
                import subprocess
                out_path = settings.MEDIA_ROOT
                file_path = os.path.join(out_path, first_file_name)

                new_file_name = first_file_name.split(".")[0]+ ".pdf"
                # linux下将doc转化为pdf
                subprocess.check_output(
                    ["soffice", "--headless", "--invisible", "--convert-to", "pdf", file_path, "--outdir", out_path])

                new_file_path = os.path.join(out_path, new_file_name)
                if os.path.exists(new_file_path):
                    result = {'state': 0, 'file_name': new_file_name}
                else:
                    result = {'state': 1, 'file_name': ''}

            # windows下doc生成pdf
            except:
                out_path = settings.MEDIA_ROOT
                # 原文件路径
                file_path = os.path.join(out_path, first_file_name)
                ##修改原文件得到新文件名字
                new_file_name = first_file_name.split(".")[0] + ".pdf"

                out_file_path = os.path.join(out_path, new_file_name)
                # doc转换pdf
                doc_pdf(file_path, out_file_path)

                if os.path.exists(out_file_path):
                    result = {'state': 0, 'file_name': new_file_name}
                else:
                    result = {'state': 1, 'file_name': ''}

        elif first_file_name.endswith('.html') or first_file_name.endswith('.txt'):
            new_file_name=first_file_name
            result = {'state': 0, 'file_name': new_file_name}
        elif first_file_name.endswith('.mht'):
            out_path=settings.MEDIA_ROOT
            file_path=os.path.join(out_path,first_file_name)
            rename_file_name=first_file_name.split(".")[0]+".doc"
            rename_file_path=os.path.join(out_path,rename_file_name)
            os.rename(file_path,rename_file_path)

            try:
                import subprocess

                file_path = os.path.join(out_path, rename_file_path)

                new_file_name = rename_file_name.split(".")[0]+ ".pdf"
                # linux下将doc转化为pdf
                subprocess.check_output(
                    ["soffice", "--headless", "--invisible", "--convert-to", "pdf", file_path, "--outdir", out_path])

                new_file_path = os.path.join(out_path, new_file_name)
                if os.path.exists(new_file_path):
                    result = {'state': 0, 'file_name': new_file_name}
                else:
                    result = {'state': 1, 'file_name': ''}

            # windows下doc生成pdf
            except:
                # 原文件路径
                file_path = rename_file_path
                ##修改原文件得到新文件名字
                new_file_name = rename_file_name.split(".")[0] + ".pdf"

                out_file_path = os.path.join(out_path, new_file_name)
                # doc转换pdf
                doc_pdf(file_path, out_file_path)

                if os.path.exists(out_file_path):
                    result = {'state': 0, 'file_name': new_file_name}
                else:
                    result = {'state': 1, 'file_name': ''}


        else:
            result = {'state': 1, 'file_name': ''}
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")

def resume_parse(request):
    if request.method == 'POST':
        file_path = request.POST.get('file_path')
        # 初始化简历清洗类,将获取到的简历读取并解析 ，pdfplumber包解析，对表格解析比较好
        resume_clean = ResumeClean()
        # 图片存储路径文件路径
        # linux写法
        pic_path = os.path.join('/opt/static', 'photo')
        # window写法
        # pic_path = os.path.join(settings.MEDIA_ROOT, 'photo')
        photo_name=resume_clean.pdf2pic(file_path,pic_path)

        #解析pdf简历
        content_str, content_table = resume_clean.resume_read(file_path)
        # 初始化简历解析类,并加载配置文件
        resume_parse = ResumeParse()
        # 注意分大块的时候不要按空格分词，不然就没法分块了
        chunk_all = resume_parse.resume_chunk(content_str, content_table)
        # print(chunk_all)
        # 提取基本信息的块,此处无论纯文本的简历还是带表格的简历，分块后都是以列表的形式返回
        basic_information = chunk_all["basic_information"]
        education_experience = chunk_all["education_experience"]
        # 将基本信息去掉无用字符并按空格分开
        basic_information = resume_clean.base_information_clean(basic_information)
        education_experience,time_list=resume_clean.education_experience_clean(education_experience)
        # 将基本信息进行内容提取
        #初始化基本信息抽取类
        extract_information = ExtractInformation()

        education_information_info = extract_information.education_information(education_experience, time_list)
        basic_information_info = extract_information.base_information(basic_information, education_information_info)


        # 注意，使用django模板渲染，不能转json，直接传字典格式数据
        # resume_json = json.dumps(info, ensure_ascii=False)
        basic_information_info["education_experience"] = education_information_info
        basic_information_info["skills"] = "\n".join(chunk_all["skills"]).strip().replace("#", '-')
        basic_information_info["work_experience"] = "\n".join(chunk_all["work_experience"]).strip().replace("#", '-')
        basic_information_info["projects_experience"] = "\n".join(chunk_all["projects_experience"]).strip().replace("#", '-')
        basic_information_info["my_rewards"] = "\n".join(chunk_all["my_rewards"]).strip().replace("#", '-')
        basic_information_info["my_introduction"] = "\n".join(chunk_all["my_introduction"]).strip().replace("#", '-')
        basic_information_info["additional_information"] = "\n".join(chunk_all["additional_information"]).strip().replace("#", '-')
        if photo_name:
            basic_information_info["photo"] = photo_name
        else:
            basic_information_info["photo"] = 'default.jpg'
        # print(basic_information_info)
        # 将json数据写入数据库
        # 连接数据库
        # 数据插入到mongodb数据库
        # 创建数据库
        # mydb = myclient["resume_data"]
        # 创建集合（相当于表）
        # table_mongo = mydb["resume_json"]
        # 插入数据
        # x = table_mongo.find_one({"email": basic_information_info['email']})
        # if x is None:
        #     table_mongo.insert_one(basic_information_info)
        return render(request, 'resume_content.html', {"resume_data": basic_information_info})

    else:
        return redirect('/')

def resume_path(request):
    if request.method == 'POST':
        file_name = request.POST.get('file_name')
        if file_name=='简历正在上传中...,请稍后':
            result = {'state': 1, 'default_alert':'请稍后，简历正在上传中...'}
            return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")
        else:
            file_path = os.path.join(settings.MEDIA_ROOT, file_name)
            result = {'state': 0, 'file_path': file_path}
            return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")

