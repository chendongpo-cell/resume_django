#pdfplumber 是按页来处理 pdf 的，可以获得页面的所有文字，并且提供的单独的方法用于提取表格。
import pdfplumber

path = './pdf/西安电子科技大学-通信与信息系统-硕士-邢亚英.pdf'
pdf = pdfplumber.open(path)

for page in pdf.pages:
    # 获取当前页面的全部文本信息，包括表格中的文字
    print(page.extract_text())

    for table in page.extract_tables():
        # print(table)
        for row in table:
            print(row)
        print('---------- 分割线 ----------')


pdf.close()