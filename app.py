from flask import render_template, request, redirect, url_for, session, send_from_directory, jsonify, Response
from store import Post,app
from supabase import create_client, Client
import os ,uuid ,time
import ai_chat
from storage import get_storage_size
from sender import send_email ,contact_body ,post_add_body
from datetime import date
from dotenv import load_dotenv
from user import user_verifiede ,get_user_data
from datetime import timedelta 
from werkzeug.utils import secure_filename
from PIL import Image
import io
load_dotenv()
app.secret_key = os.getenv("secret_key")
app.permanent_session_lifetime = timedelta(days =900)

# تهيئة Supabase
url = os.getenv('url')
key = os.getenv('key')
img_url=os.getenv('posts_url')
sport_post=[]
takafa_post=[]
news_post=[]
supabase: Client = create_client(url, key)
def load_posts():
    response = supabase.table('lahrour').select('*').execute()
    return response.data
@app.route('/')
def home():
    session.permanent = True
    global sport_post
    data=load_posts()
    global takafa_post
    sport_post.clear()
    takafa_post.clear()
    global news_post
    news_post.clear()
    for post in data :
        if post["page"] == "sport":
            for img in ["img1", "img2", "img3", "img4"] :
                value= post.get(img)
                print(value,"and data type is ",type(value))
                if str(value) != "<class 'NoneType'>":
                    post[img] = img_url + value
            sport_post.append(post)
        elif post["page"] == "takafa":
            for img in ["img1", "img2", "img3", "img4"] :
                value= post.get(img)
                print(value,"and data type is ",type(value))
                if str(value) != "<class 'NoneType'>":
                    post[img] = img_url + value
            takafa_post.append(post)
        elif post["page"] == "news":
            for img in ["img1", "img2", "img3", "img4"] :
                value= post.get(img)
                print(value,"and data type is ",type(value))
                if str(value) != "<class 'NoneType'>":
                    post[img] = img_url + value
            news_post.append(post)
    return render_template('pages/index.html')

@app.route("/message", methods=["POST"])
def subscribe():
    email = request.form.get("Email")
    if email:
        data = {"email": email}
        response = supabase.table("emails").insert(data).execute()
    return redirect(request.referrer)
@app.route('/sw.js')
def service_worker():
    return send_from_directory('static', 'sw.js')
@app.route('/robots.txt')
def robots():
    return send_from_directory(app.static_folder, 'robots.txt')
@app.route('/takafa',methods=['POST',"GET"])
def takafa():
    global takafa_post
    print(takafa_post)
    if request.method == "POST":
        name=request.form.get("name")
        return redirect(url_for("profile",name=name))
    return render_template('pages/takafa.html', posts=takafa_post[::-1])
@app.route('/sport',methods=["POST","GET"])
def sport():
    global sport_post
    print(sport_post)
    if request.method == "POST":
        name=request.form.get("name")
        return redirect(url_for("profile",name=name))
    return render_template('pages/sport.html', posts=sport_post[::-1])
@app.route('/news',methods=['POST',"GET"])
def news():
    global news_post
    print(news_post)
    if request.method == "POST":
        name=request.form.get("name")
        return redirect(url_for("profile",name=name))
    return render_template('pages/news.html', posts=news_post[::-1])
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    try:
        error = None
        admin= os.getenv("admin_email")
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            message = request.form['message']
            subject=request.form.get("subject")
            classe = request.form['class']
            body=contact_body(email,name,message,classe,subject)
            send_email(admin ,subject,body)
            return redirect(request.referrer)
    except Exception as e:
        print("Error during contact:", e)
    return render_template('pages/contact.html', error=error)
@app.route("/login", methods=["GET", "POST"])
def login():
    try:
        error = None
        if request.method == "POST":
            session.clear()
            email = request.form["email"]
            password = request.form["password"]
            Response=user_verifiede(email,password)
            if Response == True :
                print(session)
                return redirect(url_for("post_add"))
            else:
                error="اسم المستخدم أو كلمة المرور غير صحيحة"
    except Exception as e:
        print("Error during login:", e)
    return render_template("admin/login.html", error=error)
@app.route('/post_add', methods=['GET', 'POST'])
def post_add():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    error = None
    name_in_table = []

    if request.method == "POST":
        get_storage_size("images","posts")
        images = [
            request.files.get("img1"),
            request.files.get("img2"),
            request.files.get("img3"),
            request.files.get("img4")
        ]

        for file in images:
            if file and getattr(file, "filename", None):
                orig_name = file.filename
                ext = os.path.splitext(orig_name)[1].lower()
                if ext not in [".png", ".jpg", ".jpeg"]:
                    name_in_table.append(None)
                    continue

                # تقليص حجم الصورة باستخدام Pillow
                try:
                    img = Image.open(file)
                    img = img.convert("RGB")  # لضمان التوافق
                    img.thumbnail((800, 800))  # حدد الأبعاد المطلوبة (مثلاً 800x800 بكسل)
                    img_bytes = io.BytesIO()
                    img.save(img_bytes, format="JPEG", quality=80)  # يمكنك تغيير الجودة حسب الحاجة
                    img_bytes.seek(0)
                    file_content = img_bytes.read()
                except Exception as e:
                    print("Image resize error:", e)
                    name_in_table.append(None)
                    continue

                # تحقق من الحجم بعد التقليص
                if len(file_content) > 5 * 1024 * 1024:
                    error = "حجم الملف كبير جداً بعد التقليص. يجب أن يكون أقل من 2MB."
                    name_in_table.append(None)
                    continue

                # توليد اسم ملف فريد وآمن
                unique_id = uuid.uuid4().hex
                safe_basename = secure_filename(f"{unique_id}_{int(time.time())}")
                filename = f"{safe_basename}{ext}"

                # قراءة محتوى الملف ورفعه إلى Supabase Storage
                upload_response = supabase.storage.from_("images").upload(f"posts/{filename}", file_content)
                print("upload_response:", upload_response)

                # خزّن اسم الملف (أو المسار حسب ما تريد)
                name_in_table.append(filename)
            else:
                # لم تُحمّل صورة في هذا الحقل
                name_in_table.append(None)

        selected_page = request.form.get('page')
        # === هنا ننشئ كائن Post أولاً ===
        new_post = Post(
            img1=name_in_table[0],
            img2=name_in_table[1],
            img3=name_in_table[2],
            img4=name_in_table[3],
            title=request.form.get('title'),
            body=request.form.get('body'),
            name=session.get("name"),
            topic=request.form.get('topic'),
            page=selected_page,
            date=date.today(),
        )
        print(new_post.name)
        # بناء dict من خصائص new_post لإرسالها إلى Supabase
        data = {
            "img1": new_post.img1,
            "img2": new_post.img2,
            "img3": new_post.img3,
            "img4": new_post.img4,
            "title": new_post.title,
            "body": new_post.body,
            "date": new_post.date.isoformat() if hasattr(new_post.date, "isoformat") else new_post.date,
            "page": new_post.page,
            "name": new_post.name,
            "topic": new_post.topic
        }

        # حفظ في Supabase
        resp = supabase.table('lahrour').insert(data).execute()
        print("Insert response:", resp)

        # إرسال إشعارات بالبريد
        users = get_user_data(table="emails", coloms="email")
        body_excerpt = (data["body"][:150] + " ...") if data["body"] and len(data["body"]) > 150 else data["body"]
        body_html = post_add_body( body_excerpt,data['page'], data["date"], data['title'],data["topic"], data["name"])
        for user in users:
            send_email(user['email'], subject=f"📢 منشور جديد: {data['title']}", body=body_html)
            print("emailed:", user["email"])

        return redirect(url_for('home'))

    return render_template("admin/post-add.html", error=error)

if __name__ == '__main__':
    app.run(debug=True ,host="0.0.0.0",port=5000)
