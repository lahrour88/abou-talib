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
supabase: Client = create_client(url, key)
def load_posts(page_name):
    response = (supabase.table("lahrour").select("*").eq("page",page_name).execute())
    data=[]
    for post in response.data:
        for img in ["img1", "img2", "img3", "img4"] :
            value= post.get(img)
            if value is not None:
                post[f"{img}_name"]=post[img]
                post[img] = img_url + value
        data.append(post)
    return data
@app.route('/')
def home():
    session.permanent = True
    return render_template('pages/index.html')

@app.route("/sender",methods=["POST","GET"])
def sender():
    if request.method == "POST":
        post=request.form.get('post')
        print(post)
        message=""
        if session.get("send_email"):
            new=time.time()
            data=session.get("send_email")
            session.pop("send_email")
            body_excerpt=data["body"]
            body_html = post_add_body( body_excerpt,data['page'],data['date'],data['title'],data["topic"], data["name"])
            users = get_user_data(table="emails", coloms="email")
            for user in users:
                send_email(user['email'], subject=f"📢 منشور جديد: {data['title']}", body=body_html)
                print("emailed:", user["email"])
            print(int(time.time()-int(new))) 
            message="<span>.تم إرسال التنبيهات إلى المشتركين بنجاح</span>"
            return message
        else:
            message="<span>لا يوجد منشور لإرساله</span>"
            return message
@app.route("/message", methods=["POST"])
def subscribe():
    email = request.form.get("Email")
    if email:
        data = {"email": email}
        response = supabase.table("emails").insert(data).execute()
        print("Subscription response:", response)
    return redirect(request.referrer)
@app.route('/sw.js')
def service_worker():
    return send_from_directory('static', 'sw.js')
@app.route('/robots.txt')
def robots():
    return send_from_directory(app.static_folder, 'robots.txt')
@app.route('/takafa',methods=['POST',"GET"])
def takafa():
    data=load_posts("takafa")
    if request.method == "POST":
        name=request.form.get("name")
        return redirect(url_for("profile",name=name))
    return render_template('pages/takafa.html', posts=data[::-1])
@app.route('/sport',methods=["POST","GET"])
def sport():
    data=load_posts("sport")
    if request.method == "POST":
        name=request.form.get("name")
        return redirect(url_for("profile",name=name))
    return render_template('pages/sport.html', posts=data[::-1])
@app.route('/news',methods=['POST',"GET"])
def news():
    data=load_posts("news")
    if request.method == "POST":
        name=request.form.get("name")
        return redirect(url_for("profile",name=name))
    return render_template('pages/news.html', posts=data[::-1])
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

                try:
                    img = Image.open(file)
                    img = img.convert("RGB") 
                    img.thumbnail((800, 800))  
                    img_bytes = io.BytesIO()
                    img.save(img_bytes, format="JPEG", quality=70)
                    img_bytes.seek(0)
                    file_content = img_bytes.read()
                except Exception as e:
                    print("Image resize error:", e)
                    name_in_table.append(None)
                    continue
                if len(file_content) > 5 * 1024 * 1024:
                    error = "حجم الملف كبير جداً بعد التقليص. يجب أن يكون أقل من 2MB."
                    name_in_table.append(None)
                    continue

                unique_id = uuid.uuid4().hex
                safe_basename = secure_filename(f"{unique_id}_{int(time.time())}")
                filename = f"{safe_basename}{ext}"
                upload_response = supabase.storage.from_("images").upload(f"posts/{filename}", file_content)
                print("upload_response:", upload_response)
                name_in_table.append(filename)
            else:
                name_in_table.append(None)
        selected_page = request.form.get('page')
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
        resp = supabase.table('lahrour').insert(data).execute()
        body_excerpt = (data["body"][:150] + " ...") if data["body"] and len(data["body"]) > 150 else data["body"]
        sendent={
            "body":body_excerpt,"page":data["page"],"date":data['date'],'title':data['title'],'topic':data["topic"],"name":data["name"]
        }
        session["send_email"]=sendent
        return redirect(url_for(data["page"]))

    return render_template("admin/post-add.html", error=error)

if __name__ == '__main__':
    app.run(debug=True ,host="0.0.0.0",port=5000)
