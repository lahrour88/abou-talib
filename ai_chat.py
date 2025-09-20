from flask import Flask, render_template, request ,session
import google.generativeai as genai
from supabase import Client ,create_client
import markdown, os
from rapidfuzz import fuzz
from dotenv import load_dotenv
from store import app
load_dotenv()
url = os.getenv('url')
key = os.getenv('key')
supabase: Client = create_client(url, key)
chat_session = None
@app.route("/chat_ai",methods=["POST","GET"])
def chat():
    senders=[]
    session["senders"]=senders
    global chat_session
    genai.configure(api_key=os.getenv("api_key"))
    model = genai.GenerativeModel('gemini-2.5-flash')
    chat_session = model.start_chat(history=[])
    return render_template("chat/home.html")

def eq_topic(message):
    message=message.lower()
    response = supabase.table("lahrour").select("body", "topic").execute()
    topics = response.data
    words = message.split()  
    best_match = None
    best_score = 0
    for topic in topics:
        score_full = fuzz.partial_ratio(message, topic["topic"])
        score_words = max(fuzz.partial_ratio(word, topic["topic"]) for word in words)
        score = int(0.7 * score_words + 0.3 * score_full)
        if score > best_score:
            best_score = score
            best_match = topic
    if best_score > 70:
        print(f"🔍 Debug: أفضل تطابق بنسبة {best_score}%")
        return best_match["body"]
    return False
@app.route("/chat", methods=["POST", "GET"])
def main():
    senders=session["senders"]
    global chat_session
    if request.method == "POST":
        message = request.form.get("message", "none")
        senders.append({"role": "user", "content": message})
        topic = eq_topic(message)
        if topic != False:  # فقط إذا وجد تطابق مناسب
            promt = f"""أنت مدير مدرسة، دورك هو الإجابة بشكل رسمي ودقيق عن سؤال التلميذ التالي:{message}"اعتمد حصرياً على المعطيات التالية: {topic}يجب أن تكون الإجابة واضحة، مختصرة وموجهة للتلميذ، دون أي بحث خارجي أو إضافة معلومات غير موجودة في البيانات."""
            genai.configure(api_key=os.getenv("api_key"))
            model = genai.GenerativeModel('gemini-2.5-flash')
            chat = model.start_chat()
            response = chat_session.send_message(promt)
            response_text = response.text
            html_response = markdown.markdown(response_text, extensions=["fenced_code", "tables"])
            senders.append({"role": "ai", "content": html_response})
        else:
            senders.append({"role": "ai", "content": f"للاسف لم يتم العثور على {message}"})
    return render_template("chat/repo.html", senders=senders)

