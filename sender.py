
#ارسال ايميل الى المسؤول في route contact    user(1)  contient bady is hello user your login is ....
#ارسال ايميل التحقق من المستخدم في route oublier password user(1) bady is  hello admin thes user askin ....
# ارسال ايميل الى جميع المستخدمين في post_add  array users bady is hello user your school is add new post 
import smtplib ,os
from email.mime.text import MIMEText
from dotenv import load_dotenv
load_dotenv()
sender_email = os.getenv("email_sender")
password = os.getenv("email_password")
def send_email(users , subject , body):
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
      server.starttls()
      server.login(sender_email, password)
      if users :
          try:
              msg = MIMEText(body, "html", "utf-8")
              msg['Subject'] = subject
              msg['From'] = sender_email
              msg['To'] = ",".join([users])
              server.send_message(msg)
          except Exception as e:
              return e
          return "<span>.تم إرسال التنبيهات إلى المشتركين بنجاح</span>"

def contact_body(email,name,message,classe,subject):
    body=f"""
<!DOCTYPE html>
<html lang="ar">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>إشعار إلى المدير</title>
</head>
<body style="direction: rtl;background-color: rgba(233, 231, 231, 0.226); margin:0; padding:0; font-family: Arial, sans-serif;">
  <div style="background-color:#ffffff; margin:4px; padding:15px;">

    <!-- الشعار -->
    <nav>
      <img src="https://biytrshphtxlywabygcc.supabase.co/storage/v1/object/public/emails/logo-abou-talib.png" 
           alt="Logo" width="80%" style="display:block; margin:auto; margin-left:9%;">
    </nav>

    <!-- خط فاصل -->
    <hr style="background-color: rgba(133,136,136,0.5); height:1px; border:none;">

    <!-- المحتوى -->
    <main style="direction:rtl; text-align:right; padding:10px; color:#333;">
      <h2 style="color:#0645AD; font-size:18px;">إشعار جديد</h2>
      
      <p style="font-size:15px;">
        توصلتم برسالة جديدة من <strong style="color:blue;">{name}</strong>  
        <br>القسم: <strong>{classe}</strong>.
        <p>البريد الإلكتروني: <strong style="color:blue;">{email}</strong>
      </p>

      <p style="margin:20px 0; font-size:14px; line-height:1.6;">
        <strong>الموضوع:</strong> {subject} <br>
        <strong>الرسالة:</strong> <br>
        {message}
      </p>

      <p style="margin-top:30px; font-size:13px; color:rgba(97, 97, 97, 0.9);">
        هذا البريد مرسل آلياً عبر المنصة. المرجو الرد أو اتخاذ الإجراءات المناسبة عند الحاجة.
      </p>
    </main>

    <!-- خط فاصل -->
    <hr style="background-color: rgba(133,136,136,0.5); height:1px; border:none;">

    <!-- الفوتر -->
    <footer style="text-align:center;">
      <h6 style="margin-top:20px; padding-bottom:15px; color:rgb(110,149,167); font-size:12px;">
        .© 2025 ثانوية عبدالهادي بوطالب جميع الحقوق محفوظة
      </h6>
    </footer>
  </div>
</body>
</html>
"""
    return body

def post_add_body(body_excerpt,page,date,title,name):

    return f"""
<!DOCTYPE html>
<html lang="ar">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>منشور جديد بعنوان {title}</title>
</head>
<body style="direction: rtl;background-color: rgba(233, 231, 231, 0.226); margin:0; padding:0; font-family: Arial, sans-serif;">
  <div style="background-color:#ffffff; margin:4px; padding:15px;">

    <!-- الشعار -->
    <nav>
      <img src="https://biytrshphtxlywabygcc.supabase.co/storage/v1/object/public/emails/logo-abou-talib.png" 
           alt="Logo" width="80%" margin:auto; style="display:block; margin-left:9%;">
    </nav>

    <!-- خط فاصل -->
    <hr style="background-color: rgba(133,136,136,0.5); height:1px; border:none;">

    <!-- المحتوى -->
    <main style="direction:rtl; text-align:right; padding:10px; color:#333;">
      <h2 style="color:#0645AD; font-size:18px;">📢 إعلان عن منشور جديد</h2>
      
      <p style="font-size:15px; margin-top:10px;">
        قام <strong style="color:blue;">{name}</strong> بنشر مقال جديد بتاريخ <strong>{date}</strong>  
        ضمن موضوع: <strong>{title}</strong>.
      </p>

      <p style="font-size:14px; line-height:1.6; color:#555;">
        {body_excerpt}...
      </p>

      <!-- زر عرض المزيد -->
      <div style="text-align:center; margin:25px 0;">
        <a href="https://abou-talib.vercel.app{'/'+page}" target="_blank"
           style="background-color:#0645AD; color:white; padding:10px 20px; text-decoration:none; border-radius:6px; font-size:14px;">
          عرض المنشور كاملاً
        </a>
      </div>
    </main>

    <!-- خط فاصل -->
    <hr style="background-color: rgba(133,136,136,0.5); height:1px; border:none;">

    <!-- الفوتر -->
    <footer style="text-align:center;">
      <h6 style="margin-top:20px; padding-bottom:15px; color:rgb(110,149,167); font-size:12px;">
        .© 2025 ثانوية عبدالهادي بوطالب جميع الحقوق محفوظة
      </h6>
    </footer>
  </div>
</body>
</html>
"""
def oublier_body(email,code__):
    body=f"""
<!DOCTYPE html>
<html lang="ar">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Document</title>
</head>
<body style="background-color: rgba(233, 231, 231, 0.226); margin:0; padding:0; font-family: Arial, sans-serif;">
  <div style="background-color: #ffffff; margin:4px; height:auto;">
    
    <!-- الصورة -->
    <nav>
      <img src="https://biytrshphtxlywabygcc.supabase.co/storage/v1/object/public/emails/logo-abou-talib.png" alt="Logo" width="80%" style="display:block;margin:auto;  margin-left:9%;">
    </nav>

    <!-- الخط الفاصل -->
    <hr style="background-color: rgba(133,136,136,0.5); height:1px; border:none;">

    <!-- المحتوى -->
    <main style="position:relative; text-align:center;">
      <div style="margin:30px; color:black; font-size:17px;">
        <span id="email" style="color:blue;">{email}</span>, مرحبا
      </div>

      <p style="margin:20px; font-size:14px; color:#333; direction:rtl;">
        لقد طلبت رمز التحقق لاكمال عملية تسجيل الدخول.  
        إن لم تكن أنت من طلبه فالمرجو إبلاغ المسؤول بالأمر: 
        <a href="https://abou-talib.vercel.app/contact" style="text-decoration:none; color:#0645AD;">ابلاغ المسؤول</a>
      </p>

      <h1 style="background-color:aliceblue; width:120px; padding:7px; text-align:center; margin:30px auto 20px auto; border-radius:8px; font-size:20px; font-weight:bold;">
        {code__}
      </h1>

      <p style="margin: 3px; margin-top:50px; direction:rtl; color:rgba(97, 97, 97, 0.836); font-size:12px; line-height:1.5;">
        ستنتهي صلاحية هذا الرمز خلال 24 ساعة، يرجى عدم مشاركته مع الآخرين.<br>
        إذا لم تقم بتقديم هذا الطلب، يرجى تجاهل هذا البريد الإلكتروني.
      </p>
    </main>

    <!-- خط فاصل -->
    <hr style="background-color: rgba(133,136,136,0.5); height:1px; border:none;">

    <!-- الفوتر -->
    <footer style="text-align:center;">
      <h6 style="margin-top:25px; padding-bottom:20px; color:rgb(110,149,167); font-size:12px;">
        .© 2025 ثانوية عبدالهادي بوطالب جميع الحقوق محفوظة
      </h6>
    </footer>
  </div>
</body>
</html>

"""
    return body

def verify_subscription_body(email,host, token):
    body=f"""

<!DOCTYPE html>
<html lang="ar">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Document</title>
</head>
<body style="background-color: rgba(233, 231, 231, 0.226); margin:0; padding:0; font-family: Arial, sans-serif;">
  <div style="background-color: #ffffff; margin:4px; height:auto;">
    
    <!-- الصورة -->
    <nav>
      <img src="https://biytrshphtxlywabygcc.supabase.co/storage/v1/object/public/emails/logo-abou-talib.png" alt="Logo" width="80%" style="display:block;margin:auto;  margin-left:9%;">
    </nav>

    <!-- الخط الفاصل -->
    <hr style="background-color: rgba(133,136,136,0.5); height:1px; border:none;">

    <!-- المحتوى -->
    <main style="position:relative; text-align:center;">
      <div style="margin:30px; color:black; font-size:17px;">
        <span id="email" style="color:blue;">{email}</span>, مرحبا
      </div>

      <p style="margin:20px; font-size:14px; color:#333; direction:rtl;">
        لقد طلبت رمز التحقق لاكمال عملية تسجيل الدخول.  
        إن لم تكن أنت من طلبه فالمرجو إبلاغ المسؤول بالأمر: 
        <a href="https://abou-talib.vercel.app/contact" style="text-decoration:none; color:#0645AD;">ابلاغ المسؤول</a>
      </p>
      <a href="https://{host}/confirm_subscription?token={token}"><h1 style="background-color:aliceblue; width:120px; padding:7px; text-align:center; margin:30px auto 20px auto; border-radius:8px; font-size:20px; font-weight:bold;">تاكيد الاشتراك </h1></a>
      <p style="margin: 3px; margin-top:50px; direction:rtl; color:rgba(97, 97, 97, 0.836); font-size:12px; line-height:1.5;">
        ستنتهي صلاحية هذا الرمز خلال 24 ساعة، يرجى عدم مشاركته مع الآخرين.<br>
        إذا لم تقم بتقديم هذا الطلب، يرجى تجاهل هذا البريد الإلكتروني.
      </p>
    </main>

    <!-- خط فاصل -->
    <hr style="background-color: rgba(133,136,136,0.5); height:1px; border:none;">

    <!-- الفوتر -->
    <footer style="text-align:center;">
      <h6 style="margin-top:25px; padding-bottom:20px; color:rgb(110,149,167); font-size:12px;">
        .© 2025 ثانوية عبدالهادي بوطالب جميع الحقوق محفوظة
      </h6>
    </footer>
  </div>
</body>
</html>
"""
    return body