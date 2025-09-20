from flask import render_template, request, redirect, url_for, session, send_from_directory, jsonify, Response
from store import Post,app
from supabase import create_client, Client
import os ,uuid 
import ai_chat
from sender import send_email ,contact_body ,post_add_body
from datetime import date
from dotenv import load_dotenv
from user import user_verifiede ,get_user_data
from datetime import timedelta 
load_dotenv()
app.secret_key = os.getenv("secret_key")
app.permanent_session_lifetime = timedelta(days =10000)
# تهيئة Supabase
url = os.getenv('url')
key = os.getenv('key')
sport_post=[]
takafa_post=[]
news_post=[]
supabase: Client = create_client(url, key)
def load_posts():
    response = supabase.table('lahrour').select('*').execute()
    return response.data
@app.route('/')
def home():
    img_url="https://biytrshphtxlywabygcc.supabase.co/storage/v1/object/public/images//"
    session.permanent = True
    data=load_posts()
    for post in data :
        if post["page"] == "sport":
            if str(type(post['public_url'])) == "<class 'NoneType'>":
                post["public_url"]= ""
            else:
                img= post["public_url"]
                post["public_url"]=img_url+img
            print(post["public_url"])
            global sport_post
            sport_post.append(post)
        elif post["page"] == "takafa":
            print("and ",type(post["public_url"]))
            if str(type(post['public_url'])) == "<class 'NoneType'>":
                post["public_url"]= ""
            else:
                img= post["public_url"]
                post["public_url"]=img_url+img
            print(post["public_url"])
            global takafa_post
            takafa_post.append(post)
        elif post["page"] == "naws":
            print("and ",type(post["public_url"]))
            if str(type(post['public_url'])) == "<class 'NoneType'>":
                post["public_url"]= ""
            else:
                img= post["public_url"]
                post["public_url"]=img_url+img
            print(post["public_url"])
            global news_post
            news_post.append(post)

    return render_template('pages/index.html')

@app.route("/message", methods=["POST"])
def subscribe():
    email = request.form.get("Email")
    if email:
        data = {"email": email}
        response = supabase.table("emails").insert(data).execute()
        print(response.data)
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
    if request.method == "POST":
        name=request.form.get("name")
        return redirect(url_for("profile",name=name))
    return render_template('pages/takafa.html', posts=takafa_post[::-1])
@app.route('/sport',methods=["POST","GET"])
def sport():
    global sport_post
    if request.method == "POST":
        name=request.form.get("name")
        return redirect(url_for("profile",name=name))
    return render_template('pages/sport.html', posts=sport_post[::-1])
@app.route('/news',methods=['POST',"GET"])
def news():
    global news_post
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
    try:
        error = None
        print(f"Session logged_in: {session.get('logged_in')}")  # تتبع حالة الجلسة
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        public_url = None
        print(session)
        if request.method == "POST":
            file = request.files.get('image')
            if file:
                file.seek(0, os.SEEK_END)
                file_length = file.tell()
                print("file_length", file_length)
                file.seek(0, 0)
                if file_length > 2000 * 1024:  # 500 كيلوبايت
                    error = "حجم الملف كبير جداً. يجب أن يكون أقل من 1000 كيلوبايت."
                # تغيير اسم الملف إلى اسم فريد باستخدام uuid
                file_extension = os.path.splitext(file.filename)[1]
                new_filename = f"{uuid.uuid4()}{file_extension}"
                # تحميل الملف مباشرةإلى Supabase Storage
                file_content = file.read()
                upload_response = supabase.storage.from_("images").upload(new_filename, file_content)
            else:
                new_filename=None
            selected_page = request.form['page']
            new_post = Post(
                public_url=new_filename,  
                photo_url=request.form['photo_url'],
                title=request.form['title'],
                body=request.form['body'],
                name=session["name"],
                topic=request.form['topic'],
                page=selected_page,
                date=date.today()  
            )
            # حفظ البيانات في Supabase
            data = {
                "photo_url": new_post.photo_url,
                "title": new_post.title,
                "public_url": new_post.public_url,
                "body": new_post.body,
                "date": new_post.date.isoformat(),
                "page": new_post.page,
                "name":new_post.name,
                "topic":new_post.topic
            }
            supabase.table('lahrour').insert(data).execute()
            users=get_user_data(table="emails",coloms="email")
            body_excerpt = (data["body"][:150] + " ...") if len(data["body"]) > 150 else data["body"]
            data["body_excerpt"] = body_excerpt 

            body=post_add_body(data['photo_url'],data["body_excerpt"],data["date"],data['title'],data["public_url"],data["topic"],data["name"])
            for  user in users:
                send_email(user['email'], subject=f"📢 منشور جديد: {data['title']}", body=body)

    except Exception as e :
        print('ereur',e)
    return render_template('admin/post-add.html',error=error)

if __name__ == '__main__':
    app.run(debug=True ,host="0.0.0.0")
