# 🏫 School Portal Project

![Logo](https://biytrshphtxlywabygcc.supabase.co/storage/v1/object/public/emails/abou-talib.png)

موقع تعليمي متكامل لإدارة المدرسة، يسمح للمدرسين والإدارة بالتواصل مع التلاميذ، ونشر المنشورات، ومتابعة الحسابات الشخصية، وحساب المعدلات. كما يدمج نموذج ذكاء اصطناعي للإجابة على الأسئلة، ويدعم **PWA** للوصول السريع عبر الهواتف.

---

## 🔹 ميزات المشروع

- إضافة منشورات جديدة للإدارة والأساتذة.  
- صفحات عرض المنشورات والبروفايلات الشخصية للأساتذة.  
- تسجيل دخول مع خيار استرجاع كلمة المرور عبر البريد الإلكتروني.  
- نموذج ذكاء اصطناعي للإجابة على الأسئلة بناءً على قاعدة البيانات.  
- حساب المعدلات الأكاديمية للتلاميذ تلقائيًا.  
- إمكانية التواصل بين التلاميذ والإدارة.  
- دعم **PWA** لتثبيت التطبيق على الهواتف.  
- إدارة الصلاحيات لكل نوع مستخدم (أستاذ، إدارة، تلميذ).

---

## 🏗️ الهيكلية العامة

- **Front-end:** HTML / CSS / JavaScript  
- **Back-end:** Python + Flask  
- **قاعدة البيانات:** Supabase  
- **الأمان:** حماية الصفحات الحساسة، إدارة الصلاحيات  

---

## ⚡ المتطلبات

- Python 3.10+  
- pip  
- Git  

---

## 🚀 التثبيت والتشغيل

1. استنساخ المستودع:
```bash
git clone https://github.com/lahrour88/abou-talib.git
cd abou-talib
```

2. تثبيت المتطلبات:
```bash
pip install -r requirements.txt
```

3. تشغيل المشروع:
```bash
python app.py
```

4. الوصول إلى التطبيق عبر المتصفح:
```
http://localhost:5000
```

---

## 🤖 استخدام الذكاء الاصطناعي

يمكن للمستخدمين طرح أسئلة على النظام وسيجيب نموذج الذكاء الاصطناعي بناءً على البيانات الموجودة في قاعدة البيانات.

---

## 👨‍💻 المساهمة

مرحب بالمطورين لإضافة ميزات جديدة أو تحسين الأداء.  
- افتح Issue لوصف المشكلة أو الاقتراح.  
- قدم Pull Request مع وصف التعديلات.  

---

## 📸 صور توضيحية

![نمودج gemini](./readm/code.png)  
![صفحة المنشورات](./readm/Screenshot_20250920_162753_Gmail.jpg)  
![صفحة البروفايل](./readm/Screenshot_20250920_163740_Brave.jpg)  

---

## 🛠️ الفريق والمطور

![صورة المستخدم](./assets/me.png)  
**المطور:** lahrour abdelaadime

[رابط GitHub](https://github.com/lahrour88)  
[رابط Instagram](https://instagram.com/lahrour_1902)    

---

## 🔗 روابط الموقع على Vercel
[abou-talib.vercel.app](https://abou-talib.vercel.app)  

---

## 🗂️ المخططات التوضيحية

### 🔐 تدفق تسجيل الدخول
```mermaid
sequenceDiagram
    participant User as 👨‍🎓 مستخدم
    participant FE as 💻 واجهة المستخدم (Frontend)
    participant BE as ⚙️ خادم Flask
    participant DB as 🗄️ قاعدة بيانات Supabase

    User->>FE: يدخل البريد وكلمة المرور
    FE->>BE: إرسال بيانات تسجيل الدخول
    BE->>DB: التحقق من الحساب
    DB-->>BE: نتيجة التحقق (نجاح / فشل)
    alt نجاح
        BE-->>FE: إنشاء Session وإرجاع Dashboard
        FE-->>User: عرض لوحة التحكم
    else فشل
        BE-->>FE: رسالة خطأ
        FE-->>User: عرض إشعار فشل الدخول
    end
```

---

### ⚙️ بنية المشروع
```mermaid
graph TD
    subgraph Client [💻 الواجهة الأمامية]
        A[👨‍🏫 أستاذ]
        B[👨‍🎓 تلميذ]
        C[🏫 إدارة]
    end

    subgraph Backend [⚙️ Flask Backend]
        R[app.py - Routes]
        U[user.py]
        S[store.py]
        N[sender.py]
        AI[ai_chat.py]
    end

    subgraph DB [🗄️ Supabase]
        D[(Users)]
        P[(Posts)]
        G[(Grades)]
    end

    A --> R
    B --> R
    C --> R

    R --> U
    R --> S
    R --> N
    R --> AI

    U --> D
    S --> P
    AI --> D
    AI --> G
```

---

### 🧩 العلاقات بين الجداول
```mermaid
erDiagram
    USERS ||--o{ POSTS : "ينشئ"
    USERS ||--o{ GRADES : "يحصل"
    TEACHERS ||--o{ POSTS : "يكتب"
    STUDENTS ||--o{ GRADES : "يمتلك"

    USERS {
        int id PK
        string name
        string email
        string role
    }

    POSTS {
        int id PK
        string title
        string body
        int user_id FK
    }

    GRADES {
        int id PK
        int student_id FK
        int value
        string subject
    }
```
