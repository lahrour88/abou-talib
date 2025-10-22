from flask import Flask, render_template, request ,session ,flash
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
    return render_template('chat/chat.html')

def eq_topic(message):
    try:
        message = message.lower()
        response = supabase.table("lahrour").select("body","topic").execute()
        topics = response.data[::-1]
        words = message.split()  
        
        best_match = None
        best_score = 0

        for topic in topics:
            # تقسيم الاحتمالات بعلامة # أو //
            possible_questions = topic["topic"].replace("|", "#").split("#")
            for question in possible_questions:
                question = question.strip().lower()
                if not question:
                    continue

                score_full = fuzz.partial_ratio(message, question)
                score_words = max(fuzz.partial_ratio(word, question) for word in words)
                score = int(0.7 * score_words + 0.3 * score_full)

                if score > best_score:
                    best_score = score
                    best_match = topic

        if best_score > 75:
            print(f"🔍 Debug: أفضل تطابق بنسبة {best_score}%")
            return best_match["body"]
        return False
    except Exception as error:
        print(error)
        return "نواجه مشكلة في الخادم"

@app.route("/chat", methods=["POST", "GET"])
def main():
    try:
        senders=session["senders"]
        genai.configure(api_key=os.getenv("api_key"))
        model = genai.GenerativeModel('gemini-2.5-flash')
        if request.method == "POST":
            message = request.form.get("message", "none")
            senders.append({"role": "user", "content": message})
            topic = eq_topic(message)
            if topic != False:
                promt = f"""أنت نمودج دكاء اصطناعي للمدرسة ، دورك هو الإجابة بشكل رسمي ودقيق عن سؤال التلميذ التالي:{message}"اعتمد حصرياً على المعطيات التالية: {topic}يجب أن تكون الإجابة واضحة، مختصرة وموجهة للتلميذ، دون أي بحث خارجي أو إضافة معلومات غير موجودة في البيانات."""
                chat = model.start_chat()
                response = chat.send_message(promt)
                response_text = response.text
                html_response = markdown.markdown(response_text, extensions=["fenced_code", "tables"])
                senders.append({"role": "ai", "content": html_response})
            else:
                senders.append({"role": "ai", "content": f"للاسف لم يتم العثور على نتائج مطابقة لبحثك {message}"})
    except Exception as error:
        return error
    return render_template("chat/repo.html", senders=senders)

def to_marckdone(text):
    if text :
        promte=f"""
        حول النص التالي إلى تنسيق Markdown صالح للعرض في HTML. 
        أجب **فقط بالنص المحول إلى Markdown**، بدون أي شرح أو تعليق.
        النص:
        {text}
        """
        genai.configure(api_key=os.getenv("api_key"))
        model = genai.GenerativeModel('gemini-2.5-flash')
        chat = model.start_chat()
        response = chat.send_message(promte)
        response_text = response.text
        markdone_text = markdown.markdown(
            response_text,
            extensions=[
            "fenced_code",
            "codehilite",
            "tables",
            "toc",
            "attr_list",
            "def_list",
            "abbr",
            "admonition",
            "footnotes",
            "meta",
            "nl2br",
            "sane_lists",
            "smarty",
            "wikilinks"
            ],
            extension_configs={
            "codehilite": {"guess_lang": False, "noclasses": True},
            "toc": {"permalink": True}
            }
        )

    return markdone_text
