import re
from itertools import groupby
from pyhanlp import *


class BaseInformation:
    #去除汉字,注意列表不能，需要转化为字符串
    def replace_chinese(self,text):
        try:
            if text == '':
                return []
            filtrate = re.compile(u'[\u4E00-\u9FA5]')
            text_without_chinese = filtrate.sub(r' ', " ".join(text))
            return text_without_chinese
        except:
            return ''

    # #提取姓名
    def extract_name(self,text,basic_information_re):
        try:
            name=""
            con_len = len(text)
            re_information = re.compile(basic_information_re)
            for i, c in enumerate(text):
                if re.search(re_information, c) and 2 <= len(c) <= 3 and i < con_len - 1:
                    if '\u4e00' <= text[i + 1] <= '\u9fff' and 2<=len(text[i + 1])<=4:
                        return text[i + 1]

                    else:
                        name = ""
                        break
                else:
                    name=""
            if name=="":
                surname_one=[]
                surname_two=[]
                name_path=os.path.join(os.getcwd(),'resume_extract','information_files','name.txt')
                with open(name_path, "r", encoding="utf8") as f:
                    surname = f.read().replace("\n", " ").split()
                    for s in surname:
                        if len(s)==1:
                            surname_one.append(s)
                        else:
                            surname_two.append(s)

                for str in text:
                    if len(str)==2 or len(str)==3:
                        for sur in surname_one:
                            if str.startswith(sur):
                                return str
                    else:
                        if len(str)==4:
                            for sur in surname_two:
                                if str.startswith(sur):
                                    return str
            return ""
        except:
            return ''

        # 获取地址
    #提取性别
    def extract_gender(self,text,basic_information_re):
        try:
            gender = ""
            con_len = len(text)
            re_information = re.compile(basic_information_re)
            for i, c in enumerate(text):
                if re.search(re_information, c) and 2 <= len(c) <= 3 and i < con_len - 1:
                    if '\u4e00' <= text[i + 1] <= '\u9fff' and len(text[i + 1]) ==1:
                        return text[i + 1]
                    else:
                        gender = ""
                        break
                else:
                    gender = ""
            if gender=="":
                for str in text:
                    if "男" in str:
                        gender="男"
                        return gender
                    else:
                        if "女" in str:
                            gender="女"
                            return gender
            return ""
        except:
            return ''
    #提取出生年月
    def extract_birthdata(self,text,basic_information_re):
        try:
            birthdata = ""
            con_len = len(text)
            re_information = re.compile(basic_information_re)
            birthday_re = re.compile('\d{4}')
            for i, c in enumerate(text):
                if re.search(re_information, c) and 2 <= len(c) <= 5 and i < con_len - 1:
                    if  6<= len(text[i + 1]) <= 12 and re.search(birthday_re,text[i + 1]):
                        return text[i + 1]
                    else:
                        birthdata = ""
                        break
            if birthdata=="":
                age_re=re.compile('年龄|年纪|岁数|年岁')
                age=""
                for i, c in enumerate(text):
                    birthday_re = re.compile('\d{2}')
                    if re.search(age_re, c) and 2 <= len(c) <= 4 and i < con_len - 1:
                        if 2 <= len(text[i + 1]) <= 4 and re.search(birthday_re, text[i + 1]):
                            age=re.search(birthday_re,text[i + 1]).group(0)
                            break
                        else:
                            age=""
                            break
                if age=="":
                    birthday_re = re.compile('\d{4}')
                    for c in text:
                        if re.search(birthday_re,c) and len(c) <= 10:
                            return c
                    return ""
                else:
                    import datetime
                    now_year=datetime.datetime.now().year
                    birthdata=now_year-int(age)
                    birthdata=str(birthdata)
                    return birthdata
        except:
            return ''
    def get_location(self,word_pos_list):
        try:
            location_list = []
            if word_pos_list == []:
                return []

            for i, t in enumerate(word_pos_list):
                word = t[0]
                nature = t[1]
                if nature == 'ns':
                    loc_tmp = word
                    count = i + 1
                    while count < len(word_pos_list):
                        next_word_pos = word_pos_list[count]
                        next_pos = next_word_pos[1]
                        next_word = next_word_pos[0]
                        if next_pos == 'ns' or 'n' == next_pos[0]:
                            loc_tmp += next_word
                        else:
                            break
                        count += 1
                    location_list.append(loc_tmp)

            return location_list  # max(location_list)
        except:
            return []
    #提取地址
    def extract_location(self,text,basic_information_re):
        try:
            con_len = len(text)
            re_information = re.compile(basic_information_re)
            for i, c in enumerate(text):
                if re.search(re_information, c) and 2 <= len(c) <= 6 and i < con_len - 1:
                    return text[i + 1]
            # if location=="":
            #     seg_list = [(str(t.word), str(t.nature)) for t in HanLP.segment(text)]
            #     location_list = self.get_location(seg_list)
            #     if location_list:
            #         for line in location_list:
            #             if len(line)>=len(location):
            #                 location=line
            #         return location
            #     else:
            #         return ""
            return ''
        except:
            return ''
    #提取英语水平
    def extract_english(self, text, basic_information_re):
        try:
            english = ""
            english_list=[]
            con_len = len(text)
            re_information = re.compile(basic_information_re)
            for i, c in enumerate(text):
                if re.search(re_information, c) and 2 <= len(c) <= 5 and i < con_len - 1:
                    if '4' in text[i + 1] or '4' in text[i + 1] or '四' in text[i + 1] or '六' in text[i + 1]:
                        return text[i + 1]
                    else:
                        english == ""
            if english=="":
                re_str="四级|4级|六级|6级"
                new_re_str = re.compile(re_str)
                for str in text:
                    if re.search(new_re_str, str) and 2<=len(str) <= 6:
                        english_list.append(str)
                if len(english_list)==1:
                    english=english_list[0]
                    return english
                else:
                    for str in english_list:
                        if "六" in str or "6" in str:
                            english="六级"
                            return  english
                    english = "四级"
                    return english
            return ""
        except:
            return ''
    #提取邮件号
    def extract_email(self,text,basic_information_re):
        try:
            email=""
            con_len = len(text)
            re_information = re.compile(basic_information_re)
            for i, c in enumerate(text):
                if re.search(re_information, c) and 2 <= len(c) <= 5 and i < con_len - 1:
                    if "@" in text[i + 1]:
                        return text[i + 1]
                    else:
                        email = ""
                        break
                else:
                    email = ""
            if email=="":
                eng_texts = self.replace_chinese(text)
                eng_texts = eng_texts.replace(' at ', '@').replace(' dot ', '.')
                sep = ',!?:：; ，。！？《》、|\\/'
                eng_split_texts = [''.join(g) for k, g in groupby(eng_texts, sep.__contains__) if not k]
                email_pattern = r'^[a-zA-Z0-9_-]+(\.|[a-zA-Z0-9_-]+)+@[a-zA-Z0-9_-]+(\.[a-zA-Z_-]+)+$'
                for eng_text in eng_split_texts:
                    result = re.search(email_pattern, eng_text, flags=0)
                    if result:
                        return result.group(0)
                    else:
                        email=''
            return email
        except:
            return ''
    # 提取手机号
    def extract_cellphone(self, text, basic_information_re):
        try:
            cellphone = ""
            con_len = len(text)
            re_information = re.compile(basic_information_re)
            cell_re=re.compile('\d{1}')
            for i, c in enumerate(text):
                if re.search(re_information, c) and 2 <= len(c) <= 5 and i < con_len - 1:
                    if re.search(cell_re,text[i+1]):
                        new_str=''.join(re.findall(cell_re,text[i+1]))
                        if 11<=len(new_str)<=15:
                            return new_str
                        else:
                            cellphone = ""
                            break
                    else:
                        cellphone = ""
                        break
            if cellphone == "":
                phone_re = re.compile('1\d{10}')
                another_phone_re = re.compile('1\d{2}.{1,2}\d{3,4}.{1,2}\d{3,4}')
                for c in text:
                    if re.search(phone_re,c):
                        cellphone=re.search(phone_re,c).group(0)
                        return cellphone
                    else:
                        if re.search(another_phone_re, c):
                            cell_re = re.compile('\d{1}')
                            cellphone = ''.join(re.findall(cell_re,c))
                            return cellphone
                return ""
        except:
            return ''
    #提取大学名
    def extract_university(self, text, basic_information_re):
        try:
            university=""
            con_len = len(text)
            re_information = re.compile(basic_information_re)
            for i, c in enumerate(text):
                if "大学" in c or "学院" in c:
                    if len(c)<=10:
                        return c
                else:
                    if re.search(re_information, c) and 2 <= len(c) <= 6 and i < con_len - 1:
                        if "大学" in text[i + 1] or "学院" in text[i + 1] :
                            if '路' in text[i + 1] or 10<=len(text[i + 1]):
                                continue
                            else:
                                return text[i + 1]

            if university=="":
                return ''
        except:
            return ''

    #提取专业：
    def extract_major(self, text, basic_information_re):
        try:
            con_len = len(text)
            major=''
            re_information = re.compile(basic_information_re)
            for i, c in enumerate(text):
                if re.search(re_information, c) and 2 <= len(c) <= 5 and i < con_len - 1:
                    if 2 <= len(text[i + 1]) <= 8:
                        return text[i + 1]
                    else:
                        major=''
                        break
            if major=='':
                return ''
        except:
            return
    #提取学历
    def extract_education(self, text, basic_information_re):
        try:
            education_re=re.compile('本科|学士|专科|大专|硕士|研究生|博')
            education = ""
            con_len = len(text)
            re_information = re.compile(basic_information_re)
            for i, c in enumerate(text):
                if re.search(re_information, c) and 2 <= len(c) <= 5 and i < con_len - 1:
                    if re.search(education_re,text[i + 1]):
                        return text[i + 1]
            if education == "":
                return ""
        except:
            return ''
    #提取工作年限
    def extract_years_working(self, text, basic_information_re):
        try:
            con_len = len(text)
            re_information = re.compile(basic_information_re)
            for i, c in enumerate(text):
                if re.search(re_information, c) and 2 <= len(c) <= 5 and i < con_len - 1:
                    if 2 <= len(text[i + 1]) <= 4:
                        return text[i + 1]
            return ''
        except:
            return ''
    #提取身份证号
    def extract_ids(self,text):
        """
        extract all ids from texts<string>
        eg: extract_ids('my ids is 150404198812011101 m and dsdsd@dsdsd.com,李林的邮箱是eewewe@gmail.com哈哈哈')


        :param: raw_text
        :return: ids_list<list>
        """
        if text == '':
            return []
        eng_texts = self.replace_chinese(text)
        sep = ',!?:; ：，.。！？《》、|\\/abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        eng_split_texts = [''.join(g) for k, g in groupby(eng_texts, sep.__contains__) if not k]
        eng_split_texts_clean = [ele for ele in eng_split_texts if len(ele) == 18]

        id_pattern = r'^[1-9][0-7]\d{4}((19\d{2}(0[13-9]|1[012])(0[1-9]|[12]\d|30))|(19\d{2}(0[13578]|1[02])31)|(19\d{2}02(0[1-9]|1\d|2[0-8]))|(19([13579][26]|[2468][048]|0[48])0229))\d{3}(\d|X|x)?$'

        phones = []
        for eng_text in eng_split_texts_clean:
            result = re.match(id_pattern, eng_text, flags=0)
            if result:
                phones.append(result.string.replace('+86', '').replace('-', ''))
        return phones






# if __name__ == 'main':
#     resume=ResumeAnalysi()
#     text = '急寻小明，男孩，于2020年4月27号11时在上海市浦东新区走失。' \
#            '丢失发型短发，...如有线索，请迅速与警方联系：手机号：18100065143，132-6156-2938，' \
#            '邮箱号1:   baizhantang1@sina.com.cn 和yangyangfuture at gmail dot com，' \
#            '邮箱号2：  dongpo.chen@Pactera.com' \
#            '邮箱号3:baizhantang3@sina.com.cn' \
#            '邮箱号4：zhaoyue.127@163.com' \
#            '邮箱号5 baizhantang5@sina.com.cn' \
#            '邮箱号6 898008559@qq.com'
#     resume.extract_email(text)
