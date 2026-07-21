# 📚 دليل ربط النظام بـ Google Sheets

هذا الدليل يشرح خطوة بخطوة كيفية ربط نظام الكاشير بـ Google Sheets.

---

## 📋 المتطلبات

1. حساب Google (Gmail)
2. الوصول لـ Google Cloud Console
3. تثبيت المكتبات المطلوبة

---

## 🔧 الخطوة 1: إنشاء مشروع في Google Cloud Console

1. اذهب إلى [Google Cloud Console](https://console.cloud.google.com/)
2. سجل الدخول بحساب Google الخاص بك
3. اضغط على **"Select a project"** في أعلى الصفحة
4. اضغط على **"New Project"**
5. أدخل اسم المشروع (مثال: `cafe-sales-system`)
6. اضغط **"Create"**

---

## 🔑 الخطوة 2: تفعيل Google Sheets API

1. من القائمة الجانبية، اذهب إلى **"APIs & Services"** > **"Library"**
2. ابحث عن **"Google Sheets API"**
3. اضغط عليه ثم اضغط **"Enable"**

---

## 👤 الخطوة 3: إنشاء Service Account

1. من القائمة الجانبية، اذهب إلى **"APIs & Services"** > **"Credentials"**
2. اضغط على **"Create Credentials"** > **"Service account"**
3. أدخل اسم الحساب (مثال: `cafe-service-account`)
4. اضغط **"Continue"** ثم **"Done"**

---

## 📥 الخطوة 4: تحميل ملف الاعتماد (credentials.json)

1. في صفحة **"Credentials"**، اضغط على البريد الإلكتروني للـ Service Account الذي أنشأته
2. اذهب إلى تبويب **"Keys"**
3. اضغط **"Add Key"** > **"Create new key"**
4. اختر **"JSON"** ثم اضغط **"Create"**
5. سيتم تحميل ملف JSON - **احفظه باسم `credentials.json`** في مجلد المشروع

---

## 📊 الخطوة 5: إنشاء Google Sheet

1. اذهب إلى [Google Sheets](https://sheets.google.com/)
2. أنشئ Sheet جديد
3. سمه (مثال: `Cafe Sales Data`)
4. أنشئ ورقة عمل باسم **"المبيعات"**
5. أضف العناوين في الصف الأول:
   - A1: التاريخ
   - B1: المنتج
   - C1: الكمية
   - D1: إجمالي المبيعات
   - E1: التقييم

---

## 🔗 الخطوة 6: مشاركة الـ Sheet مع Service Account

1. من ملف الـ JSON الذي حملته، انسخ **client_email** (يبدو مثل: `xxx@xxx.iam.gserviceaccount.com`)
2. افتح Google Sheet الذي أنشأته
3. اضغط على **"Share"** (مشاركة)
4. الصق بريد الـ Service Account
5. اختر صلاحية **"Editor"**
6. اضغط **"Send"**

---

## 📝 الخطوة 7: الحصول على Sheet ID

من رابط الـ Sheet الخاص بك:
```
https://docs.google.com/spreadsheets/d/SHEET_ID_HERE/edit
```

انسخ الجزء بين `/d/` و `/edit` - هذا هو **Sheet ID**

---

## ⚙️ الخطوة 8: إعداد النظام

### 8.1 ضع ملف credentials.json
انسخ ملف `credentials.json` إلى مجلد المشروع:
```
coffee/
├── credentials.json  ← هنا
├── app.py
├── config.py
└── ...
```

### 8.2 عدّل ملف google_sheets_config.py
افتح ملف `google_sheets_config.py` وعدّل السطر التالي:
```python
SHEET_ID = "YOUR_SHEET_ID_HERE"  # استبدل هذا بـ Sheet ID الخاص بك
```

---

## 🚀 الخطوة 9: تثبيت المكتبات

```bash
pip install -r requirements.txt
```

---

## ✅ الخطوة 10: تشغيل النظام

```bash
streamlit run app.py
```

---

## 🔁 التبديل بين Google Sheets و Excel

للتبديل بين النظامين، عدّل ملف `config.py`:

```python
# استخدم Google Sheets
USE_GOOGLE_SHEETS = True

# أو استخدم Excel محلي
USE_GOOGLE_SHEETS = False
```

---

## ❓ أسئلة شائعة

### س: يظهر خطأ "FileNotFoundError"
**ج:** تأكد أن ملف `credentials.json` موجود في مجلد المشروع

### س: يظهر خطأ "Permission denied"
**ج:** تأكد من مشاركة الـ Sheet مع بريد الـ Service Account بصلاحية Editor

### س: البيانات لا تظهر
**ج:** تأكد من:
1. Sheet ID صحيح
2. ورقة العمل اسمها "المبيعات"
3. العناوين في الصف الأول

### س: كيف أضيف ورقة عمل جديدة؟
**ج:** النظام ينشئ ورقة العمل تلقائياً إذا لم تكن موجودة

---

## 🛡️ ملاحظات أمنية مهمة

1. **لا تشارك ملف `credentials.json` مع أحد**
2. أضف `credentials.json` إلى `.gitignore`
3. استخدم متغيرات البيئة للإنتاج

---

## 📞 الدعم

إذا واجهت أي مشكلة، تحقق من:
1. اتصالك بالإنترنت
2. صلاحيات الـ Service Account
3. صحة Sheet ID
