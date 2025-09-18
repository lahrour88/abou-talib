
#ارسال ايميل الى المسؤول في route contact    user(1)  contient bady is hello user your login is ....
#ارسال ايميل التحقق من المستخدم في route oublier password user(1) bady is  hello admin thes user askin ....
# ارسال ايميل الى جميع المستخدمين في post_add  array users bady is hello user your school is add new post 
import smtplib ,os
from email.mime.text import MIMEText
from dotenv import load_dotenv
load_dotenv()
sender_email = os.getenv("email_sender")
password = os.getenv("email_password")
def send_email(user , subject , body):
    msg = MIMEText(body, "html", "utf-8")
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = str(user)
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.send_message(msg)
            print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")
