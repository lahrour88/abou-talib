
from werkzeug.utils import secure_filename
from flask import redirect ,render_template ,url_for ,request ,session
from supabase import Client ,create_client
import os ,json , random
from sender import send_email ,oublier_body
from dotenv import load_dotenv
from store import app ,users
load_dotenv()
url = os.getenv('url')
key = os.getenv('key')
supabase: Client = create_client(url, key)
def get_user_data(table,coloms):
    response = supabase.table(table).select(coloms).execute()
    return response.data

@app.route('/delet',methods=['POST',"GET"])
def delet():
    if request.method == "POST":
        post_id=request.form.get("post_id")
        if post_id : 
            print(type(post_id))
            post_id=int(post_id)
            response = (supabase.table("lahrour").delete().eq("id",post_id).execute())
            resule ="تم حدف المنشور بنجاح"
    return f"<h6>{resule}</h6>"
@app.route("/del",methods=["POST","GET"])
def log_out():
    session.clear()
    return redirect(url_for("home"))

@app.route('/oublier',methods=["POST","GET"])
def oublier():
    error=""
    if request.method == "POST" :
        email =request.form.get("email")
        users = get_user_data(table="users",coloms="id,email")
        for user in users:
            if user['email'] == email:
                code__ = random.randint(100000,999999)
                session["code__"]=code__
                session["id"]=user["id"]
                body=oublier_body(email,code__)
                subject=f"{code__} هو رمز اعادة تعيين كلمة السر الخاصة بك"
                send_email(email ,subject , body)
                return redirect(url_for('code'))
        else:
            error= f"عنوان البريد الالكتروني هدا {email} غير مسجل من قبل"
    return render_template('admin/oublier.html',error = error)

@app.route("/code__user_admin")
def code():
    return render_template('admin/code.html')
@app.route('/user_code',methods=["POST","GET"])
def user_code():
    if not session["code__"]:
        return "false"
    else:
        code__=session["code__"]
    if request.method == "POST":
        user_code=request.form["code"]
        if int(code__)==int(user_code):
            session.pop('code__')
            return render_template("admin/up.html")
        else:
            return """<div id="result">
    <div id="code" class="login-container">
        <div class="login-header">
        <form hx-post="/user_code" hx-target="#result">
            <div class="form-group password">
                <label for="password">رمز التحقق</label>
                <input class="form-control" type="number" id="password" name="code" required placeholder="* * * * * *">
            </div>
            <span id="span">الرمز خير صحيح </span>
            <button type="submit" class="btn">تحقق</button>
        </form>
        </div>"""
        
@app.route("/update",methods=["POST","GET"])
def update():
    if request.method== "POST":
        password=request.form.get('password')
        configue=request.form.get('configue_password')
        if password != configue :
            return "لا يوجد تطابق "
        else:
            id=int(session["id"])
            response = (supabase.table("users").update({"password": password}).eq("id", id).execute())
            session.pop("id")
            return '<script>window.location.href = "/login"</script>'
def user_verifiede(email ,password):
    datas = get_user_data(table="users" , coloms="*")
    print(datas)
    for user in datas :
        if user["email"] == email and user["password"] == password :
            session["logged_in"] = True
            session["is_admin"] = user["is_admin"]
            session["name"] = user['name']
            return True
    else:
        print("not found ")
        return False
def post_data_():
    response=supabase.table("lahrour").select('*').execute()
    return response.data

img_url="https://biytrshphtxlywabygcc.supabase.co/storage/v1/object/public/profile/profile/"
img_post_url="https://biytrshphtxlywabygcc.supabase.co/storage/v1/object/public/images//"
@app.route("/profile",methods=["POST","GET"])
def profile():
    name =request.args.get("name")
    posts=[]
    datas=get_user_data(table="users",coloms="*")
    post_data=post_data_()
    data={}
    for user_ in datas :
        if user_["name"] == name :
            user={
                "name":name,
                "profile":f"{img_url}{user_["profile_filename"]}",
                "email":user_['email'],
                "matier":user_["matier"]
                }
            for post in post_data:
                if post["name"] == name:
                    if str(type(post['public_url'])) == "<class 'NoneType'>":
                        post["public_url"]= None
                    else:
                        img= post["public_url"]
                        post["public_url"]=img_url+img
                posts.append(post)
            data={"user":user,"post":posts}
            print(data)
            return render_template("pages/profile.html",datas=data)
    else:
        return "<h4> error reloud uder data </h4>"

@app.route("/add_user", methods=["GET", "POST"])
def add_user():
    if not session.get("logged_in"):
        return "نتاسف لكن عضويتك لا تسمح لك باضافة مستخدمين جدد "
    if not session.get("is_admin"):
        return "نتاسف لكن عضويتك لا تسمح لك باضافة مستخدمين جدد "
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        matier = request.form.get("matier")
        is_admin = request.form.get("is_admin")

        profile_file = request.files["profile"]
        profile_filename = ""
        if profile_file:
            
            # نجيب الامتداد الأصلي (png/jpg/jpeg)
            ext = os.path.splitext(profile_file.filename)[1].lower()
            print(ext)
            if ext not in [".png", ".jpg", ".jpeg"]:
                return "صيغة الصورة غير مدعومة"
            # اسم الملف يكون username + الامتداد
            safe_name = secure_filename(name)  
            filename = f"{safe_name}{ext}"
            print(filename)
            path = f"profile/{filename}"
            file_bytes = profile_file.read()
            response = supabase.storage.from_("profile").upload(
            path=path,
            file=file_bytes,
            file_options={"cache-control": "3600", "upsert": "true"})
            profile_filename = filename
        new_user = users(password, email, name, matier, is_admin, profile_filename)

        user = {
            "name": new_user.name,
            "password": new_user.password,
            "email": new_user.email,
            "matier": new_user.matier,
            "is_admin": new_user.is_admin,
            "profile_filename": new_user.profile_filename
        }

        response = supabase.table("users").insert(user).execute()
        print(response)
        print("تم إنشاء مستخدم:", new_user.__dict__)

        return redirect(url_for("add_user", response=response))

    return render_template("admin/add_user.html")

def to_int(val):
    try:
        return float(val)
    except Exception as e:
        print(f"error :{e}")


@app.route("/notes", methods=["POST", "GET"])
def notes():
    if request.method == "POST":
        # معاملات (coefficients) محولة ل int
        math = int(request.form.get("math", 0))
        pc   = int(request.form.get("pc", 0))
        svt  = int(request.form.get("svt", 0))
        en   = int(request.form.get("en", 0))
        ar   = int(request.form.get("ar", 0))
        fr   = int(request.form.get("fr", 0))
        fl   = int(request.form.get("fl", 0))
        ig   = int(request.form.get("ig", 0))
        isl  = int(request.form.get("isl", 0))
        sp   = int(request.form.get("sp", 0))
        n=int(request.form.get("n",0))



        # --------------------------
        #  Variables des notes
        # --------------------------
        math1, math2, math3 = map(lambda x: to_int(request.form.get(x, "0")), ["math1","math2","math3"])
        fr1, fr2, fr3, fr4, fr_n = map(lambda x: to_int(request.form.get(x,"0")), ["fr1","fr2","fr3","fr4","fr-n"])
        pc1, pc2, pc3, pc_n     = map(lambda x: to_int(request.form.get(x,"0")), ["pc1","pc2","pc3","pc-n"])
        sp1, sp2, sp_n          = map(lambda x: to_int(request.form.get(x,"0")), ["sp1","sp2","sp-n"])
        is1, is2, is_n          = map(lambda x: to_int(request.form.get(x,"0")), ["is1","is2","is-n"])
        ar1, ar2, ar_n          = map(lambda x: to_int(request.form.get(x,"0")), ["ar1","ar2","ar-n"])
        ig1, ig2, ig_n          = map(lambda x: to_int(request.form.get(x,"0")), ["ig1","ig2","ig-n"])
        fl1, fl2, fl_n          = map(lambda x: to_int(request.form.get(x,"0")), ["fl1","fl2","fl-n"])
        svt1, svt2, svt3, svt_n = map(lambda x: to_int(request.form.get(x,"0")), ["svt1","svt2","svt3","svt-n"])
        en1, en2, en_n     = map(lambda x: to_int(request.form.get(x,"0")), ["en1","en2","en-n"])
        # --------------------------
        #  Calcul des moyennes pondérées
        # --------------------------
        ig_m   = (((ig1 + ig2) / 2) * 0.75 + ig_n * 0.25)*ig
        print(f"ig {ig_m}")
        isl_m  = (((is1 + is2)/2) * 0.75 + is_n * 0.25)*isl
        print("isl",isl_m)
        sp_m   = (((sp1 + sp2) / 2) * 0.75 + sp_n * 0.25)*sp
        print("sport",sp_m)
        math_m = ((math1 + math2 + math3) / 3)*math
        print("math",math_m)
        fl_m   = (((fl1 + fl2) / 2) * 0.75 + fl_n * 0.25) *fl
        print("filo",fl_m)
        pc_m   = (((pc1 + pc2 + pc3) / 3) * 0.75 + pc_n * 0.25) *pc
        print("pc",pc_m)
        en_m   = (((en1 + en2 ) / 2) * 0.75 + en_n * 0.25)*en
        print("en",en_m)
        ar_m   = (((ar1 + ar2) / 2) * 0.75 + ar_n * 0.25)*ar
        print("ar",ar_m)
        fr_m   = (((fr1 + fr2 + fr3 + fr4) / 4) * 0.75 + fr_n * 0.25)*fr
        print("fr",fr_m)
        svt_m  = (((svt1 + svt2 + svt3) / 3) * 0.75 + svt_n * 0.25) *svt
        print("svt",svt_m)

        # --------------------------
        #  Moyenne générale
        # --------------------------
        total_coef = math + pc + svt + fr + en + fl + ig + isl + sp + ar+1
        if total_coef == 0:
            return "<h6> خطأ: المجموع الكلي للمعاملات = 0 </h6>"

        result = (math_m + pc_m + svt_m + fr_m + en_m +
                  fl_m + ig_m + isl_m + sp_m + ar_m + n) / total_coef

        return f"<h6> معدل الدورة: {round(result,2)} </h6>"

@app.route("/note", methods=["POST", "GET"])
def note():
    return render_template("pages/note.html")
