from resume_extract.resume_parse.base_information import *
import configparser
from resume_django import settings

class ResumeParse:
    def __init__(self):
        self.chunk_re = self.load_config('resume_re','chunk_re')

    def load_config(self,section,option):
        # config.ini文件路径
        configFilePath = os.path.join(settings.BASE_DIR,'config_files','config.txt')

        config = configparser.ConfigParser()
        config.read(configFilePath, encoding='utf8')
        # return config.items(section=section)
        result = config.get(section=section, option=option).replace('\n','')
        result=result.split(',')
        return result

    def resume_chunk(self,content_str,content_table):
        chunk_str_content = {"basic_information": [], "education_experience": [], "skills": '', "work_experience": [],
                 "projects_experience": [],"my_rewards":[],"my_introduction": [],'additional_information':[] }

        chunk_table = {"basic_information": [], "education_experience": [], "skills": [], "work_experience": [],
                     "projects_experience": [],"my_rewards":[], "my_introduction": [], 'additional_information': []}

        #教育背景，证书奖励，获奖情况，证书，奖励，获奖
        if content_str:
            content_str = self.content_set(content_str)
            chunk_str_content['basic_information'],new_content_str = self.chunk_information(content_str, self.chunk_re[0], self.choose_re(0,self.chunk_re))

            chunk_str_content['education_experience'],new_content_str = self.chunk_education(new_content_str, self.chunk_re[1], self.choose_re(1,self.chunk_re))

            chunk_str_content['skills'],new_content_str = self.chunk_skills(new_content_str, self.chunk_re[2], self.choose_re(2,self.chunk_re))

            chunk_str_content['work_experience'],new_content_str = self.chunk_work_experience(new_content_str, self.chunk_re[3], self.choose_re(3,self.chunk_re))

            chunk_str_content['projects_experience'],new_content_str = self.chunk_projects_experience(new_content_str, self.chunk_re[4], self.choose_re(4,self.chunk_re))

            chunk_str_content['my_rewards'],new_content_str = self.chunk_content(new_content_str, self.chunk_re[5],self.choose_re(5, self.chunk_re))

            chunk_str_content['my_introduction'],new_content_str= self.chunk_content(new_content_str, self.chunk_re[6], self.choose_re(6,self.chunk_re))

            chunk_str_content['additional_information']=new_content_str
        if content_table:
            content_table = self.content_set(content_table)
            chunk_table['basic_information'],new_content_table = self.chunk_information(content_table, self.chunk_re[0], self.choose_re(0,self.chunk_re))

            if chunk_table['basic_information']:
                re_chunk=re.compile('邮|姓|性|电话|手机|联系方式|院校|邮箱')
                re_mail=re.compile('@')
                if re.search(re_chunk,''.join(chunk_table['basic_information'][0])) or re.search(re_mail,''.join(chunk_table['basic_information'][0])):
                    chunk_table['basic_information']=chunk_table['basic_information']
                else:
                    chunk_table['basic_information']=[]

            chunk_table['education_experience'],new_content_table = self.chunk_education(new_content_table, self.chunk_re[1], self.choose_re(1,self.chunk_re))

            chunk_table['skills'],new_content_table = self.chunk_skills(new_content_table, self.chunk_re[2], self.choose_re(2,self.chunk_re))

            chunk_table['work_experience'] ,new_content_table= self.chunk_work_experience(new_content_table, self.chunk_re[3], self.choose_re(3,self.chunk_re))

            chunk_table['projects_experience'] ,new_content_table= self.chunk_projects_experience(new_content_table, self.chunk_re[4], self.choose_re(4,self.chunk_re))

            chunk_table['my_rewards'], new_content_table = self.chunk_content(new_content_str, self.chunk_re[5],self.choose_re(5, self.chunk_re))

            chunk_table['my_introduction'] ,new_content_table= self.chunk_content(new_content_table, self.chunk_re[6], self.choose_re(6,self.chunk_re))

            chunk_table['additional_information']=new_content_table
        if content_table:
            finally_chunk=self.finally_chunk(chunk_str_content,chunk_table)
        else:
            finally_chunk=chunk_str_content
        return finally_chunk

    ## 对简历文本去重
    def content_set(self,content):
        content_set = []
        for pstr in content:
            b = list(set(pstr))
            b.sort(key=pstr.index)
            if len(pstr) == 2 * (len(''.join(b))):
                content_set.append(''.join(b))
            else:
                content_set.append(pstr)
        return content_set
    def finally_chunk(self,chunk_str,chunk_table):
        chunk_table_values=[]
        for key,values in chunk_table.items():
            if key=='additional_information':
                continue
            if values:
                chunk_table_values.append(values)

        if 3<=len(chunk_table_values):
            finally_chunk=chunk_table
        else:
            finally_chunk=chunk_str
            return finally_chunk

        for key, values in chunk_table.items():
            if values==[]:
                finally_chunk[key]=chunk_str[key]
        return finally_chunk

    def choose_re(self,re_number, chunk_re):
        finally_chunk_re = []
        for i in range(len(chunk_re)):
            if i == re_number:
                continue
            else:
                finally_chunk_re.append(chunk_re[i])
        return finally_chunk_re

    def chunk_information(self,content, re_str, chunk_re):
        chunk_str = []
        resume_top = []
        remove_str=[]
        # 找到一大块的开头
        index_str = 0
        end=0
        for i,resume_str in enumerate(content):
            if end:
                break
            new_re_str = re.compile(re_str)
            new_resume_str=''.join(re.findall('[\u4e00-\u9fff]+|\d+', resume_str))
            if len(new_resume_str)<=6:
                if re.search(new_re_str, new_resume_str):
                    remove_str.append(resume_str)
                    index_str = i
                    break
                else:
                    for another_re in chunk_re:
                        new_re_str = re.compile(another_re)
                        if re.search(new_re_str, new_resume_str):
                            end=True
                            break
                if end:
                    break
                resume_top.append(resume_str)
            else:
                if re.search(new_re_str, new_resume_str[0:6]) or re.search(new_re_str, new_resume_str[-6:]):
                        index_str = i
                        break
                else:
                    for another_re in chunk_re:
                        new_re_str = re.compile(another_re)
                        if re.search(new_re_str, new_resume_str[0:6]) or re.search(new_re_str, new_resume_str[-6:]):
                            end=True
                            break
                        else:
                            # 如果匹配不到教育，尝试通过，学校，学历，时间进行教育模块分割
                            a_str = re.compile('硕士|研究生|本科|学士|专科|大专|博|大学|学院')
                            b_str = re.compile('\d{4}')
                            a = re.findall(a_str, new_resume_str)
                            b = re.search(b_str, new_resume_str)
                            if 2<= len(a) and b != None :
                                end=True
                                break
                if end:
                    break
                resume_top.append(resume_str)
        if end:
            for str in resume_top:
                if str in content:
                    content.remove(str)
            return resume_top,content
        else:
            end=0
            for i, resume_str in enumerate(content):
                if i==index_str and len(resume_str)>6:
                    chunk_str.append(resume_str)
                if i>index_str:
                    new_resume_str = ''.join(re.findall('[\u4e00-\u9fff]+|\d+', resume_str))
                    #小于6就不需要匹配学历，时间等了。
                    if len(new_resume_str) <= 6:
                        for another_re in chunk_re:
                            another_re = re.compile(another_re)
                            ignore_re = re.compile('年限|年份|时长|长短')
                            if re.search(another_re, new_resume_str):
                                if re.search(ignore_re, new_resume_str):
                                    continue
                                else:
                                    end=True
                                    break
                    else:
                        for another_re in chunk_re:
                            another_re = re.compile(another_re)
                            ignore_re=re.compile('年限|年份|时长|长短')
                            if re.search(another_re, new_resume_str[0:6]) or re.search(another_re, new_resume_str[-6:]):
                                if re.search(ignore_re, new_resume_str):
                                    continue
                                else:
                                    end=True
                                    break
                            else:
                                # 如果匹配不到教育，尝试通过，学校，学历，时间进行教育模块分割
                                a_str = re.compile('硕士|研究生|本科|学士|专科|大专|博|大学|学院')
                                b_str = re.compile('\d{4}')
                                a = re.findall(a_str, new_resume_str)
                                b = re.search(b_str, new_resume_str)
                                if 2<= len(a) and b != None:
                                    end = True
                                    break
                    if end:
                        break
                    chunk_str.append(resume_str)

            for str in resume_top + chunk_str+remove_str:
                if str in content:
                    content.remove(str)

            if resume_top:
                return resume_top + chunk_str,content
            else:
                return chunk_str,content

    def chunk_education(self,content, re_str, chunk_re):
        chunk_str = []
        remove_str = []
        # 找到一大块的开头
        index_str = 0
        for i, resume_str in enumerate(content):
            new_re_str = re.compile(re_str)
            new_resume_str = ''.join(re.findall('[\u4e00-\u9fff]+|\d+', resume_str))
            if len(new_resume_str)<=6:
                if re.search(new_re_str, new_resume_str):
                    remove_str.append(resume_str)
                    index_str = i
                    break
            else:
                #如果字体多于6个字的，即使匹配到也不再删除，避免误删信息
                if re.search(new_re_str, new_resume_str[0:6]) or re.search(new_re_str, new_resume_str[-6:]):
                        index_str = i
                        break
                else:
                    #如果匹配不到教育，尝试通过，学校，学历，时间进行教育模块分割
                    a_str = re.compile('硕士|研究生|本科|学士|专科|大专|博|大学|学院')
                    b_str = re.compile('\d{4}')
                    a = re.findall(a_str, new_resume_str)
                    b = re.search(b_str, new_resume_str)
                    if 1<= len(a) and b != None:
                        index_str = i
                        break
                    elif 2 <= len(a):
                        index_str = i
                        break
        end = 0
        for i, resume_str in enumerate(content):
            if i == index_str and len(resume_str) > 6:
                chunk_str.append(resume_str)
            if i >index_str:
                new_resume_str = ''.join(re.findall('[\u4e00-\u9fff]+', resume_str))
                if len(new_resume_str) <= 6:
                    for another_re in chunk_re:
                        another_re = re.compile(another_re)
                        if re.search(another_re, new_resume_str):
                            end=True
                            break
                        else:
                            end_re=re.compile('公司|集团|项目|工作|技能|评价|奖')
                            if re.search(end_re,new_resume_str):
                                end=True
                                break
                else:
                    for another_re in chunk_re:
                        another_re = re.compile(another_re)
                        if re.search(another_re, new_resume_str[0:6]) or re.search(another_re, new_resume_str[-6:]):
                            end=True
                            break
                        else:
                            end_re=re.compile('公司|集团|项目|工作|技能|评价')
                            if re.search(end_re,new_resume_str):
                                end=True
                                break

                if end:
                    break
                chunk_str.append(resume_str)
        for str in chunk_str + remove_str:
            if str in content:
                content.remove(str)

        return chunk_str, content

    def chunk_skills(self,content, re_str, chunk_re):
        chunk_str = []
        remove_str = []
        # 找到一大块的开头
        index_str = 0
        for i, resume_str in enumerate(content):
            new_re_str = re.compile(re_str)
            new_resume_str = ''.join(re.findall('[\u4e00-\u9fff]+', resume_str))
            if len(new_resume_str) <= 6:
                if re.search(new_re_str, new_resume_str):
                    remove_str.append(resume_str)
                    index_str = i
                    break
            else:
                if re.search(new_re_str, new_resume_str[0:6]) or re.search(new_re_str, new_resume_str[-6:]):
                    index_str = i
                    break

        end = 0
        for i, resume_str in enumerate(content):
            if i == index_str and len(resume_str) > 6:
                chunk_str.append(resume_str)
            if i >index_str:
                new_resume_str = ''.join(re.findall('[\u4e00-\u9fff]+', resume_str))
                end_re=re.compile('熟悉|了解|熟练')
                if len(new_resume_str) <= 6:
                    for another_re in chunk_re:
                        another_re = re.compile(another_re)
                        if re.search(another_re, new_resume_str):
                            if re.search(end_re, new_resume_str[0:4]):
                                continue
                            else:
                                end = True
                                break
                else:
                    for another_re in chunk_re:
                        another_re = re.compile(another_re)
                        if re.search(another_re, new_resume_str[0:6]) or re.search(another_re, new_resume_str[-6:]):
                            if re.search(end_re, new_resume_str[0:4]):
                                continue
                            else:
                                end = True
                                break

                if end:
                    break
                chunk_str.append(resume_str)

        for str in chunk_str + remove_str:
            if str in content:
                content.remove(str)
        return chunk_str, content

    def chunk_work_experience(self,content, re_str, chunk_re):
        chunk_str = []
        remove_str = []
        # 找到一大块的开头
        index_str = 0
        for i, resume_str in enumerate(content):
            new_re_str = re.compile(re_str)
            new_resume_str = ''.join(re.findall('[\u4e00-\u9fff]+', resume_str))
            if len(new_resume_str) <= 6:
                if re.search(new_re_str, new_resume_str):
                    remove_str.append(resume_str)
                    index_str = i
                    break
            else:
                if re.search(new_re_str, new_resume_str[0:6]) or re.search(new_re_str, new_resume_str[-6:]):
                    index_str = i
                    break

        end = 0
        for i, resume_str in enumerate(content):
            if i == index_str and len(resume_str) > 6:
                chunk_str.append(resume_str)
            if i > index_str:
                new_resume_str = ''.join(re.findall('[\u4e00-\u9fff]+', resume_str))
                if len(new_resume_str) <= 6:
                    for another_re in chunk_re:
                        another_re = re.compile(another_re)
                        if re.search(another_re, new_resume_str) :
                            end = True
                            break
                else:
                    for another_re in chunk_re:
                        another_re = re.compile(another_re)
                        if re.search(another_re, new_resume_str[0:6]) or re.search(another_re, new_resume_str[-6:]):
                            end = True
                            break
                if end:
                    break
                chunk_str.append(resume_str)
        for str in chunk_str + remove_str:
            if str in content:
                content.remove(str)
        return chunk_str, content

    def chunk_projects_experience(self,content, re_str, chunk_re):
        chunk_str = []
        remove_str = []
        # 找到一大块的开头
        index_str = 0
        for i, resume_str in enumerate(content):
            new_re_str = re.compile(re_str)
            new_resume_str = ''.join(re.findall('[\u4e00-\u9fff]+', resume_str))
            if len(new_resume_str) <= 6:
                if re.search(new_re_str, new_resume_str):
                    remove_str.append(resume_str)
                    index_str = i
                    break
            else:
                if re.search(new_re_str, new_resume_str[0:6]) or  re.search(new_re_str, new_resume_str[-6:]):
                    index_str = i
                    break

        end = 0
        for i, resume_str in enumerate(content):
            if i == index_str and len(resume_str) > 6:
                chunk_str.append(resume_str)
            if i > index_str:
                new_resume_str = ''.join(re.findall('[\u4e00-\u9fff]+', resume_str))
                if len(new_resume_str) <= 6:
                    for another_re in chunk_re:
                        another_re = re.compile(another_re)
                        if re.search(another_re, new_resume_str):
                            end = True
                            break
                else:
                    for another_re in chunk_re:
                        another_re = re.compile(another_re)
                        if re.search(another_re, new_resume_str[0:6]) or re.search(another_re, new_resume_str[-6:]):
                            end = True
                            break

                if end:
                    break
                chunk_str.append(resume_str)
        for str in chunk_str + remove_str:
            if str in content:
                content.remove(str)
        return chunk_str, content
    def chunk_content(self,content, re_str, chunk_re):
        chunk_str = []
        remove_str = []
        # 找到一大块的开头
        index_str = 0
        for i,resume_str in enumerate(content):
            new_re_str = re.compile(re_str)
            new_resume_str = ''.join(re.findall('[\u4e00-\u9fff]+', resume_str))
            if len(new_resume_str)<=6:
                if re.search(new_re_str, new_resume_str):
                    remove_str.append(resume_str)
                    index_str = i
                    break
            else:
                if re.search(new_re_str, new_resume_str[0:6]) or re.search(new_re_str, new_resume_str[-6:]):
                    index_str = i
                    break

        end=0
        for i, resume_str in enumerate(content):
            if i == index_str and len(resume_str) > 6:
                chunk_str.append(resume_str)
            if i > index_str:
                new_resume_str = ''.join(re.findall('[\u4e00-\u9fff]+', resume_str))
                if len(new_resume_str) <= 6:
                    for another_re in chunk_re:
                        another_re = re.compile(another_re)
                        if re.search(another_re, new_resume_str):
                            end=True
                            break
                else:
                    for another_re in chunk_re:
                        another_re = re.compile(another_re)
                        if re.search(another_re, new_resume_str[0:6]) or re.search(another_re, new_resume_str[-6:]):
                            end=True
                            break

                if end:
                    break
                chunk_str.append(resume_str)

        for str in chunk_str+remove_str:
            if str in content:
                content.remove(str)
        return chunk_str,content




