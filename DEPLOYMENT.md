# دليل نشر التطبيق على Streamlit Cloud 🚀

## أسرع طريقة مضمونة لنشر تطبيقك مجاناً

---

## 📋 الخطوات السريعة (5 دقائق)

### 1️⃣ رفع الكود على GitHub
1. تأكد من وجود حساب على [GitHub](https://github.com)
2. أنشئ مستودع (Repository) جديد
3. ارفع الملفات التالية:
   - `app.py`
   - `requirements.txt`
   - `setup.sh`
   - `.streamlit/config.toml`
   - `README.md`
   - `google_sheets_config.py`
   - `config.py`

⚠️ **مهم جداً**: **لا ترفع ملف `credentials.json`** - هذا ملف سري!

---

### 2️⃣ نشر على Streamlit Cloud

1. اذهب إلى [https://share.streamlit.io](https://share.streamlit.io)
2. سجّل دخولك باستخدام حساب GitHub
3. اضغط على **"New app"**
4. اختر المستودع الذي أنشأته
5. اختر الفرع (عادة `main` أو `master`)
6. أدخل اسم الملف الرئيسي: `app.py`
7. اضغط **"Deploy"**

---

### 3️⃣ إعداد Google Sheets (اختياري)

إذا أردت استخدام Google Sheets:

1. أنشئ Google Sheet جديد
2. شارك الـ Sheet مع البريد الإلكتروني الموجود في ملف `credentials.json`
3. انسخ معرف الـ Sheet (الجزء من الرابط)
4. في Streamlit Cloud، أضف متغير البيئة:
   ```
   GOOGLE_SHEET_ID = [معرف الـ Sheet الخاص بك]
   ```

---

## ⚙️ إعداد متغيرات البيئة على Streamlit Cloud

لإضافة متغيرات البيئة:

1. اذهب إلى إعدادات التطبيق على Streamlit Cloud
2. أضف المتغيرات التالية:

| الاسم | القيمة | نوع |
|------|-------|-----|
| `GOOGLE_SHEET_ID` | `1URic7Z7Gm4fKDYILnH9meYnl25o2E6nbnVizgpXMijg` | Secret |

---

## 🎯 النتيجة

بعد نشر التطبيق، ستحصل على رابط مباشر مثل:
```
https://your-username-streamlit-app-name.streamlit.app
```

يمكنك مشاركة هذا الرابط مع أصدقائك!

---

## 🆘 مشاكل شائعة وحلولها

### المشكلة: "credentials.json not found"
**الحل**: هذا طبيعي على Streamlit Cloud. تأكد من استخدام Excel محلي أو إعداد Google Sheets بشكل صحيح.

### المشكلة: "Permission denied"
**الحل**: تأكد من مشاركة Google Sheet مع البريد الإلكتروني في `credentials.json` (إذا كنت تستخدم Google Sheets).

### المشكلة: التطبيق لا يعمل
**الحل**: تحقق من سجلات الأخطاء (Logs) في Streamlit Cloud لرؤية التفاصيل.

---

## 📝 ملحوظات مهمة

1. **الأمان**: ملف `credentials.json` يجب أن يبقى سرياً ولا يرفع مع الكود
2. **النسخ الاحتياطي**: سيتم إنشاء نسخ احتياطية تلقائياً في مجلد `backups/`
3. **البيانات**: إذا كنت تستخدم Google Sheets، البيانات ستكون مركزية. إذا كنت تستخدم Excel، البيانات ستكون محليّة على الخادم

---

## 🌟 مزايا Streamlit Cloud

- ✅ مجاني تماماً
- ✅ لا يتطلب بطاقة ائتمانية
- ✅ تحديث تلقائي عند رفع كود جديد
- ✅ رابط مباشر جاهز للمشاركة
- ✅ يدعم مكتبات Python مثل pandas و plotly

---

## 📞 مساعدة إضافية

لأي استفسار، تحقق من:
- [توثيق Streamlit Cloud](https://docs.streamlit.io/streamlit-cloud)
- [Community forums](https://discuss.streamlit.io)