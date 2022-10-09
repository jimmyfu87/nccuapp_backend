import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from ..env.config import get_logger

logger = get_logger('send_email')


def send_email(member_email: str, member_id: str, member_password: str):
    logger.info('send_email()')
    logger.info('member_email: {}'.format(member_email))
    logger.info('member_id: {}'.format(member_id))
    logger.info('member_password: {}'.format(member_password))
    sender_email = "nccugo105306@gmail.com"
    content = MIMEMultipart()  #建立MIMEMultipart物件
    content["subject"] = "iWant購-重設密碼通知信件"  #郵件標題
    content["from"] = sender_email  #寄件者
    content["to"] = member_email #收件者
    content.attach(MIMEText("您好:" + '\n' + "歡迎使用iWant購，以下是您的帳號及暫時密碼，請登入後立即重設您的密碼，感謝您的配合。"+ \
                            "\n\n" + "帳號:  "+ member_id + '\n' + '密碼:  ' + member_password))  #郵件內
    with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:  # 設定SMTP伺服器
        try:
            smtp.ehlo()  # 驗證SMTP伺服器
            smtp.starttls()  # 建立加密傳輸
            smtp.login(sender_email, "ediwjnlxcszvzblh")  # 登入寄件者gmail
            smtp.send_message(content)  # 寄送郵件
            return {'success': True, 'message': 'Send reset password mail successfully!' + '\n' + 'Please check your email and login again!'}
        except Exception as e:
            logger.error("Error occurs when send_email(), error message: {}".format(e))
            return {'success': False, 'message': e}
