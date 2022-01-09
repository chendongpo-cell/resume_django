#!/usr/bin/env python
# coding:utf-8
import re
from io import StringIO
import pdfplumber
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

import fitz
import time
import re
import os
import uuid

import chardet
import html2text
import re

class ResumeClean:
    def resume_read(self, file_path):
        if file_path.endswith('.pdf'):
            strlist_str, strlist_table=self.pdfplumber_read(file_path)
            return strlist_str, strlist_table
        if file_path.endswith('.html'):
            strlist_str, strlist_table = self.html_read(file_path)
            return strlist_str, strlist_table
        if file_path.endswith('.txt'):
            strlist_str, strlist_table = self.txt_read(file_path)
            return strlist_str, strlist_table



    def pdfplumber_read(self,file_path):
        #文本是字符串形式
        content_str = ""
        #表格是列表形式
        content_table = []

        # 使用pdfminer提取非表格内容
        # content_str= self.pdfminer_read(file_path)
        pdf = pdfplumber.open(file_path)
        for page in pdf.pages:
            try:
                content_str += page.extract_text()
            except:
                content_str +=''
            # extract_tables()获取当前页面的全部表格信息，非表格文本提取不到
            for table in page.extract_tables():
                # row为列表形式，可以列表追加
                for row in table:
                    row += "\n"
                    content_table += row
        pdf.close()
        # 将简历按换行符分割
        if content_str != "":
            strlist_str = content_str.split("\n")
            #清洗列表元素
            strlist_str = [re.sub('[^\u4e00-\u9fa5^.^。^、^"^\'^“^”^;^；^，^,^：^:^!^！^?^？^%^%^-^-^——^-^_^:^/^\\^@^@^&^*^a-z^A-Z^0-9]', '#',
                                  c.strip()) for c in strlist_str]
            strlist_str = [re.sub('##', '#',c.strip()) for c in strlist_str]

            #去除只有#的字符串
            new_strlist_str=[]
            for c in strlist_str:
                if len(c.replace('#',''))!=0:
                    new_strlist_str.append(c)
            strlist_str = list(filter(None, new_strlist_str))
        else:
            strlist_str = []

        if content_table != []:
            content_table = list(filter(None, content_table))
            strlist_table = " ".join(content_table)
            strlist_table = strlist_table.strip().split("\n")
            strlist_table = [re.sub('[^\u4e00-\u9fa5^.^。^、^"^\'^“^”^;^；^，^,^：^:^!^！^?^？^%^%^-^-^——^-^_^:^/^\\^@^@^&^*^a-z^A-Z^0-9]', '#',
                                    c.strip()) for c in strlist_table]
            strlist_table = [re.sub('###', '#',
                                  c.strip()) for c in strlist_table]
            new_strlist_table = []
            for c in strlist_table:
                if len(c.replace('#', '')) != 0:
                    new_strlist_table.append(c)
            strlist_table=new_strlist_table
        else:
            strlist_table=[]

        return strlist_str, strlist_table
    def pdfminer_read(self, file_path):
        strlist = []
        content = ''
        # 解析pdf
        if file_path.endswith('.pdf'):
            rsrcmgr = PDFResourceManager(caching=True)
            laparams = LAParams()
            retstr = StringIO()
            device = TextConverter(rsrcmgr, retstr, laparams=laparams)
            with open(file_path, 'rb') as fp:
                interpreter = PDFPageInterpreter(rsrcmgr, device)
                for page in PDFPage.get_pages(fp, pagenos=set()):
                    page.rotate = page.rotate % 360
                    interpreter.process_page(page)
            device.close()
            content = retstr.getvalue()
        return content
    def html_read(self,file_path):
        str_file=''
        strlist_str = []
        strlist_table=[]
        fin = open(file_path, 'rb')
        strfile = fin.read()
        # 文本格式的编码方式统一为utf-8
        if ((chardet.detect(strfile)['encoding'] == 'utf-8') or (chardet.detect(strfile)['encoding'] == 'UTF-8-SIG')):
            str_file = html2text.html2text(strfile.decode())
        else:
            str_file = html2text.html2text(strfile.decode("gbk", 'ignore').encode("utf-8", 'ignore').decode())
        str_file = re.sub(r'[# * | -]?', '', str_file)  # drop #*
        if str_file != '':
            strlist_str = str_file.split('\n')
            #清洗列表元素
            strlist_str = [re.sub('[^\u4e00-\u9fa5^.^。^、^"^\'^“^”^;^；^，^,^：^:^!^！^?^？^%^%^-^-^——^-^_^:^/^\\^@^@^&^*^a-z^A-Z^0-9]', '#',
                                  c.strip()) for c in strlist_str]
            strlist_str = [re.sub('##', '#',c.strip()) for c in strlist_str]

            #去除只有#的字符串
            new_strlist_str=[]
            for c in strlist_str:
                if len(c.replace('#',''))!=0:
                    new_strlist_str.append(c)
            strlist_str = list(filter(None, new_strlist_str))
        else:
            strlist_str = []


        return strlist_str, strlist_table
    def txt_read(self,file_path):
        str_file = ''
        strlist_str = []
        strlist_table = []
        fin = open(file_path, 'rb')
        strfile = fin.read()
        # 文本格式的编码方式统一为utf-8
        if ((chardet.detect(strfile)['encoding'] == 'utf-8') or (chardet.detect(strfile)['encoding'] == 'UTF-8-SIG')):
            str_file = strfile
        else:
            str_file = strfile.decode("gbk", 'ignore').encode("utf-8", 'ignore').decode()

        if str_file != '':
            strlist_str = str_file.split('\n')
            #清洗列表元素
            strlist_str = [re.sub('[^\u4e00-\u9fa5^.^。^、^"^\'^“^”^;^；^，^,^：^:^!^！^?^？^%^%^-^-^——^-^_^:^/^\\^@^@^&^*^a-z^A-Z^0-9]', '#',
                                  c.strip()) for c in strlist_str]
            strlist_str = [re.sub('##', '#',c.strip()) for c in strlist_str]

            #去除只有#的字符串
            new_strlist_str=[]
            for c in strlist_str:
                if len(c.replace('#',''))!=0:
                    new_strlist_str.append(c)
            strlist_str = list(filter(None, new_strlist_str))
        else:
            strlist_str = []

        return strlist_str, strlist_table
    def base_information_clean(self, content):
        strlist = []
        if content != []:
            content= list(filter(None, content))
            words = [c.strip() for c in content]
            for word in words:
                word = re.split('[:：#]', word)
                for w in word:
                    strlist.append(w)
            strlist = list(filter(lambda x: x, strlist))
            return strlist
        else:
            return []
    def education_experience_clean(self, content):
        if content != []:
            a_re = re.compile('专科|大专|本科|学士|硕士|研究生|博|大学|学院')
            b_re = re.compile('\d{4}')
            new_education_content=[]
            for str in content:
                if re.search(a_re,str) or re.search(b_re,str):
                    new_education_content.append(str)
                else:
                    continue
            #抽取时间
            time_list=[]
            time_re=re.compile('(\d{4}.{1,10}至今|\d{4}.{1,10}\d{1,2})')
            for str in new_education_content:
                time_list+=time_re.findall(str)

            #合并断开的时间
            new_time_list=[]
            n=0
            if len(time_list)%2==0:
                for i in range(len(time_list)-1):
                    if i !=0 and i==n:
                        continue
                    if len(time_list[i])<=8 and len(time_list[i+1])<=8:
                        new_time_list.append(re.sub('[^.^\-^_^0-9^至今]','#',time_list[i])+'-'+re.sub('[^.^\-^_^0-9^至今]','#',time_list[i+1]))
                        n=i+1
                    else:
                        new_time_list.append(re.sub('[^.^\-^_^0-9^至今]','#',time_list[i]))
                        new_time_list.append(re.sub('[^.^\-^_^0-9^至今]','#',time_list[i+1]))
                        n=i+1
            else:
                if len(time_list)==1:
                    for i in range(len(time_list)):
                        new_time_list.append(re.sub('[^.^\-^_^0-9^至今]', '#', time_list[i]))
                elif 1<len(time_list):
                    for i in range(len(time_list) - 1):
                        if i != 0 and i == n:
                            continue
                        if len(time_list[i]) <= 8 and len(time_list[i + 1]) <= 8:
                            new_time_list.append(re.sub('[^.^\-^_^0-9^至今]', '#', time_list[i]) + '-' + re.sub('[^.^\-^_^0-9^至今]',
                                                                                                 '#', time_list[i + 1]))
                            n = i + 1
                        else:
                            new_time_list.append(re.sub('[^.^\-^_^0-9^至今]', '#', time_list[i]))
                            new_time_list.append(re.sub('[^.^\-^_^0-9^至今]', '#', time_list[i + 1]))
                            n = i + 1
            time_list=[]
            if new_time_list != []:
                for str in new_time_list:
                    aaa = [i for i in re.sub('[^.^\-^_^0-9^#^至今]', '.', str).split('#') if i != '']
                    aaa = '-'.join(aaa)
                    time_list.append(aaa)

            return new_education_content ,time_list
        else:
            return []
    def pdf2pic(self,file_path, pic_path):
        try:
            t0 = time.clock()  # 生成图片初始时间
            checkXO = r"/Type(?= */XObject)"  # 使用正则表达式来查找图片
            checkIM = r"/Subtype(?= */Image)"
            doc = fitz.open(file_path)  # 打开pdf文件
            imgcount = 0  # 图片计数
            lenXREF = doc._getXrefLength()  # 获取对象数量长度

            # 遍历每一个对象
            new_name=''
            for i in range(1, lenXREF):
                text = doc._getXrefString(i)  # 定义对象字符串
                isXObject = re.search(checkXO, text)  # 使用正则表达式查看是否是对象
                isImage = re.search(checkIM, text)  # 使用正则表达式查看是否是图片
                if not isXObject or not isImage:  # 如果不是对象也不是图片，则continue
                    continue
                pix = fitz.Pixmap(doc, i)  # 生成图像对象
                new_name=uuid.uuid4().hex[:10]
                new_name = "{}.png".format(new_name)  # 生成图片的名称
                if pix.n < 5:  # 如果pix.n<5,可以直接存为PNG
                    pix.writePNG(os.path.join(pic_path, new_name))
                else:  # 否则先转换CMYK
                    pix0 = fitz.Pixmap(fitz.csRGB, pix)
                    pix0.writePNG(os.path.join(pic_path, new_name))
                    pix0 = None
                pix = None  # 释放资源
                t1 = time.clock()  # 图片完成时间
            return new_name
        except:
            new_name = ''
            return new_name



