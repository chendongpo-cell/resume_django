from resume_extract.resume_parse.base_information import *
from resume_django import settings
import jieba
import configparser

class ExtractInformation:
    def __init__(self):
        self.resume_base_information = BaseInformation()
        self.basic_information_re=self.load_config('resume_re','basic_information_re')
        self.base_name=self.load_config('resume_re','base_name')
    def load_config(self,section,option):
        # config.ini文件路径
        configFilePath = os.path.join(settings.BASE_DIR,'config_files','config.txt')

        config = configparser.ConfigParser()
        config.read(configFilePath, encoding='utf8')
        # return config.items(section=section)
        result = config.get(section=section, option=option).replace('\n','')
        result=result.split(',')
        return result

    def base_information(self, content, education_information_info):
        content = [re.sub('[^\u4e00-\u9fa5^@^@^a-z^A-Z^0-9^.^-^-^_^——]', ' ',
                          c.strip()) for c in content]

        base_name = self.base_name
        try:
            base_content = []
            a = 0
            for i in range(len(content)):
                if i == a and i != 0:
                    continue
                if len(content[i]) == 1:
                    if content[i] + content[i + 1] in base_name:
                        base_content.append(content[i] + content[i + 1])
                        a = i + 1
                    else:
                        base_content.append(content[i])
                else:
                    base_content.append(content[i])
        except:
            base_content = content

        new_content = []
        # 合并相邻单个字
        try:
            n = 0
            m = 0
            for i in range(len(base_content) - 1):
                if i == n and i != 0:
                    continue
                if i == m and i != 0:
                    continue
                else:
                    if '\u4e00' <= base_content[i] <= '\u9fff' and len(base_content[i]) == 1:
                        if '\u4e00' <= base_content[i + 1] <= '\u9fff' and len(base_content[i + 1]) == 1:
                            try:
                                if '\u4e00' <= base_content[i + 2] <= '\u9fff' and len(base_content[i + 2]) == 1:
                                    new_content.append(base_content[i] + base_content[i + 1] + base_content[i + 2])
                                    n = i + 1
                                    m = i + 2
                                else:
                                    new_content.append(base_content[i] + base_content[i + 1])
                                    n = i + 1
                            except:
                                new_content.append(base_content[i] + base_content[i + 1])
                                break
                        else:
                            new_content.append(base_content[i])
                    else:
                        new_content.append(base_content[i])
                if i == (len(base_content) - 2):
                    new_content.append(base_content[i + 1])
                    break
                # if i ==len(content)-1:
                #     new_content.append(content[i])
        except Exception as e:
            new_content = base_content
        my_information = {'name': "", 'gender': "", 'birthdata': "", 'first_address': "", 'english': "",
                          'years_working': "",
                          'email': "", 'phone': "", 'university': "", 'major': "", 'education': "", 'now_address': "", }

        finally_education_list=self.education_list(education_information_info)

            # 判断基本信息的专业，学校是否为空，从教育经历拿
        # 提取字段
        basic_information_re = self.basic_information_re
        # 提取姓名
        my_information['name'] = self.resume_base_information.extract_name(new_content, basic_information_re[0])
        # 提取性别
        my_information['gender'] = self.resume_base_information.extract_gender(new_content, basic_information_re[1])
        # 提取出生年月
        my_information['birthdata'] = self.resume_base_information.extract_birthdata(new_content, basic_information_re[2])
        # 提取户籍
        my_information['first_address'] = self.resume_base_information.extract_location(new_content, basic_information_re[3])
        # 提取居住地址
        my_information['now_address'] = self.resume_base_information.extract_location(new_content, basic_information_re[4])
        # 提取英语水平
        my_information['english'] = self.resume_base_information.extract_english(new_content, basic_information_re[5])
        # 提取邮件
        my_information['email'] = self.resume_base_information.extract_email(new_content, basic_information_re[6])
        # 提取联系方式
        my_information['phone'] = self.resume_base_information.extract_cellphone(new_content, basic_information_re[7])
        # 提取院校
        my_information['university'] = self.resume_base_information.extract_university(new_content, basic_information_re[8])
        # 提取专业
        my_information['major'] = self.resume_base_information.extract_major(new_content, basic_information_re[9])
        # 提取学历
        my_information['education'] = self.resume_base_information.extract_education(new_content, basic_information_re[10])
        # 提取工作年限
        my_information['years_working'] = self.resume_base_information.extract_years_working(new_content, basic_information_re[11])
        # 提取照片

        #判断大学，学历，专业是否为空
        if my_information['university'] == '':
            my_information['university'] = finally_education_list[0]
        if my_information['education'] == '':
            my_information['education'] = finally_education_list[1]
        if my_information['major'] == '':
            my_information['major'] = finally_education_list[2]

        for key, value in my_information.items():
            if my_information[key] == '':
                my_information[key] = '---'

        return my_information
    def education_list(self,education_information_info):
        if len(education_information_info) == 1:
            university = education_information_info[0][0]
            education = education_information_info[0][2]
            major = education_information_info[0][3]
            finally_education_list = [university, education, major]
            return finally_education_list
        else:
            if len(education_information_info) > 1:
                major_re = re.compile('硕士|博|研究生')
                finally_education = []
                for education_list in education_information_info:
                    if re.search(major_re, education_list[3]):
                        finally_education += education_list
            if finally_education != []:
                university = finally_education[0]
                education = finally_education[2]
                major = finally_education[3]
                finally_education_list = [university, education, major]
                return finally_education_list
            else:
                finally_education = education_information_info[0]
                university = finally_education[0]
                education = finally_education[2]
                major = finally_education[3]
                finally_education_list = [university, education, major]
                return finally_education_list

    def education_information(self,education_content,time_list):
        finall_education_content=education_content

        university_list=[]
        degree_list=[]
        major_list=[]

        re_daxue = re.compile('大学')
        re_xueyuan=re.compile('学院')

        re_degree = "本科|学士|硕|研究生|博"

        for str in finall_education_content:
            if re.search(re_daxue,str) and re.search(re_xueyuan,str):
                strlist=self.split_content(str)
                for word in strlist:
                    if re.search(re_daxue,word):
                        university_list.append(word)
            else:
                if re.search(re_daxue,str):
                    strlist = self.split_content(str)
                    for word in strlist:
                        if re.search(re_daxue, word):
                            university_list.append(word)
                else:
                    if re.search(re_xueyuan, str):
                        strlist = self.split_content(str)
                        for word in strlist:
                            if re.search(re_xueyuan, word):
                                university_list.append(word)
        for str in finall_education_content:
            strlist=self.split_content(str)
            for str in strlist:
                if re.search(re_degree,str):
                    degree_list.append(str)
                else:
                    major_path = os.path.join(os.getcwd(), 'resume_extract', 'information_files', 'major.txt')
                    with open(major_path, "r", encoding="utf8") as f:
                        major_name = f.read().replace("\n", " ").split()
                        seg_list = jieba.cut(str, cut_all=False)
                        str_seg_list=[]
                        for i in seg_list:
                            str_seg_list.append(i)
                        if 2<=len(str_seg_list):
                            a_re=str_seg_list[0]
                            b_re=str_seg_list[-1]
                            for major in major_name:
                                if re.search(a_re, major) and re.search(b_re, major):
                                    major_list.append(major)
                        elif len(str_seg_list)==1:
                            a_re = str_seg_list[0]
                            for major in major_name:
                                if re.search(a_re, major):
                                    major_list.append(major)
                                    break
        if university_list ==[]:
            university_list=['---','---']
        if time_list ==[]:
            time_list=['---','---']
        if degree_list ==[]:
            degree_list=['---','---']
        if major_list ==[]:
            major_list=['---','---']

        education_information_info=zip(university_list,time_list,degree_list,major_list)
        education_information_data=[]
        for i in education_information_info:
            education_information_data.append(list(i))
        return education_information_data

    def split_content(self,content):
        strlist = []
        word = re.split('[:：#-_-——]', content)
        for w in word:
            strlist.append(w)
        strlist = list(filter(None, strlist))
        return strlist
