def look_database():
    from django.core.mail import send_mail, send_mass_mail, EmailMultiAlternatives
    # 求职意见接收者
    accept_email = ['898008559@qq.com']
    new_url='http://127.0.0.1:8000/database'
    html_message = '<html>' \
                   '<head></head>' \
                   '<body>' \
                   '<p> ' \
                   '求职者意见统计以通过链接形式发放<br> ' \
                   '<a href=' + new_url + '>请点击链接查看</a>' \
                   '</p> ' \
                   '</body>' \
                   '</html>'
    res = EmailMultiAlternatives('求职者意见反馈统计',
                                 '请点击链接查看' + html_message,
                                 'chen898008559@163.com',
                                 accept_email)
    res.content_subtype = 'html'
    res.send()
