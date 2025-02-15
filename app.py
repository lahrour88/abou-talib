from flask import Flask, render_template, request, redirect, url_for, session ,send_from_directory
from store import Post, PostStore
from supabase import create_client, Client
import os
import time
app = Flask(__name__)
app.secret_key='3ba55907a42e8314adce3fcf557c181a9c85d916f9ee657604bb79d058b55729'
url='https://biytrshphtxlywabygcc.supabase.co'
key='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJpeXRyc2hwaHR4bHl3YWJ5Z2NjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzczMTE4NjEsImV4cCI6MjA1Mjg4Nzg2MX0.G63kILbsKfvbtHzgMkJjZb8hAoPQG_S1FClE01GBTLY'
supabase: Client = create_client(url, key)
post_store = PostStore()
app.current_id = 2
USERNAME ='lahrour_1902'
PASSWORD = "admin123"
# تحميل المنشورات من Supabase عند بدء التشغيل
def load_posts():
    response = supabase.table('lahrour').select('*').execute()
    posts = response.data
    for post in posts:
        new_post = Post(id=post['id'],
                        photo_url=post['photo_url'],
                        date=post['date'],
                        body=post['body'],
                        vedio=post['vedio'],
                        page=post['page'])  # إضافة حقل الصفحة
        post_store.add(new_post)
        app.current_id = max(app.current_id, new_post.id + 1)

load_posts()

@app.route('/robots.txt')
def robots():
    return send_from_directory(app.static_folder, 'robots.txt')

# Route for sitemap.xml
@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory(app.static_folder, 'sitemap.xml')

@app.route('/takafa')
def takafa():
    posts = [post for post in post_store.get_all() if post.page == 'takafa']
    return render_template('takafa.html', posts=posts)

@app.route('/')
def sport():
    posts = [post for post in post_store.get_all() if post.page == 'sport']
    return render_template('index.html', posts=posts,)

@app.route('/google5af1f70e8206f4e3.html')
def google_verification():
    return send_from_directory(app.static_folder, 'google5af1f70e8206f4e3.html')

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory(app.static_folder, 'sitemap.xml')


@app.route('/arabec')
def arabec():
    posts = [post for post in post_store.get_all() if post.page == 'arabec']
    return render_template('arabec.html', posts=posts)

@app.route('/page1')
def home():
    posts = [post for post in post_store.get_all() if post.page == 'home']
    return render_template('page1.html', posts=posts)

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        gmail = request.form.get("gmail")
        password = request.form.get("password")

        if gmail == USERNAME and password == PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("post_add"))
        else:
            error = "خطأ: البريد الإلكتروني أو كلمة المرور غير صحيحة."
    return render_template("login.html", error=error)

@app.route('/post_add', methods=['GET', 'POST'])
def post_add():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        # أخذ البيانات من post-add
        selected_page = request.form['page']
        new_post = Post(id=app.current_id,
                        date=request.form['date'],
                        photo_url=request.form['photo_url'],
                        body=request.form['body'],
                        vedio=request.form['vedio'],
                        page=selected_page)  # إضافة الصفحة المرتبطة
        post_store.add(new_post)
        app.current_id += 1

        # حفظ البيانات في Supabase
        data = {
            "photo_url": new_post.photo_url,
            "date": new_post.date,
            "body": new_post.body,
            "vedio":new_post.vedio,
            "page": new_post.page  # إضافة حقل الصفحة
        }
        supabase.table('lahrour').insert(data).execute()

        # إعادة التوجيه إلى الصفحة المختارة
        if selected_page == 'home':
            return redirect(url_for('home'))
        elif selected_page == 'sport':
            return redirect(url_for('sport'))
        elif selected_page == 'takafa':
            return redirect(url_for('takafa'))
        elif selected_page == 'arabec':
            return redirect(url_for('arabec'))
    elif request.method == 'GET':
        return render_template('post-add.html')

if __name__ == '__main__':
    app.run (debug=True)