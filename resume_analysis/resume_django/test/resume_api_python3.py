# python3.x
# _*_ coding:utf-8 _*_
# coding=utf8
import sys
import importlib
import requests
import base64
import json

importlib.reload(sys)


# 注:需要安装requests模块


def main():
    cv_file = "./pdf/北京工业大学-李小龙-硕士-数字媒体专业历.docx" #请替换为您的简历
    print(cv_api(cv_file))


def cv_api(cv_file):
    cv_url = "http://127.0.0.1:8000/resume/"
    return upload_file(cv_url, cv_file)


def upload_file(url, file_path):
    json_data = {"file_name": open(file_path, 'rb')}
    result = requests.post(url, files=json_data, timeout=15, verify=False)
    return result.text


if __name__ == "__main__":
    main()
