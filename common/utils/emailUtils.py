from django.core.mail import EmailMessage
from django.template.loader import render_to_string

class EmailUtils():

    def comm_send_mail(subject, mail_content, to_email):
        mail_subject = 'smtp를 사용하여 이메일 보내기'
        message = render_to_string('common/forgot_password.html', {
            'content': mail_content
        })
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()
    