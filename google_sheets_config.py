"""
ملف إعدادات الاتصال بـ Google Sheets (معدل خصيصاً للعمل مع Streamlit Cloud)
"""

import gspread
from google.oauth2.service_account import Credentials
import streamlit as st

# 1. معرف الـ Google Sheet
try:
    SHEET_ID = st.secrets["google"]["sheet_id"]
except:
    # القيمة الافتراضية إذا لم يتم وضعها في الـ secrets
    SHEET_ID = "1URic7Z7Gm4fKDYILnH9meYnl25o2E6nbnVizgpXMijg"

# 2. أسماء أوراق العمل داخل الـ Sheet
SALES_WORKSHEET = "Sales"              # صفحة المبيعات
PRODUCTS_WORKSHEET = "Menu"            # صفحة المنيو
DAILY_SUMMARY_WORKSHEET = "Daily_Summary"  # الملخص اليومي
CATEGORIES_WORKSHEET = "Categories"    # التصنيفات
EXPENSES_WORKSHEET = "Expenses"        # المصروفات

# 3. نطاقات الصلاحيات المطلوبة
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

@st.cache_resource
def get_client():
    """الحصول على عميل Google Sheets والاتصال به بشكل صحيح (مع تخزين مؤقت لتسريع التطبيق)"""
    try:
        # التأكد من وجود البيانات في Streamlit Secrets
        if "gcp_service_account" not in st.secrets:
            st.error("❌ لم يتم العثور على [gcp_service_account] في إعدادات Secrets")
            return None
            
        # تحويل بيانات الاعتماد إلى قاموس
        creds_dict = dict(st.secrets["gcp_service_account"])
        
        # 🚨 الحل الجذري لمشكلة Invalid JWT Signature 🚨
        # استبدال النص العادي "\n" بالرمز الفعلي للنزول للسطر في المفتاح الخاص
        if "\\n" in creds_dict.get("private_key", ""):
            creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")

        # إنشاء كائن الاعتماد
        creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
        
        # الاتصال بمكتبة gspread
        client = gspread.authorize(creds)
        return client
        
    except Exception as e:
        st.error(f"❌ خطأ في إعداد بيانات الاعتماد: {e}")
        return None

def get_spreadsheet():
    """الحصول على ملف الـ Spreadsheet"""
    client = get_client()
    if client:
        return client.open_by_key(SHEET_ID)
    return None

def get_worksheet(worksheet_name, default_headers):
    """الحصول على ورقة عمل مع إنشائها تلقائياً إذا لم تكن موجودة"""
    try:
        spreadsheet = get_spreadsheet()
        if not spreadsheet:
            return None
            
        try:
            worksheet = spreadsheet.worksheet(worksheet_name)
        except gspread.exceptions.WorksheetNotFound:
            # إنشاء الورقة إذا لم تكن موجودة ووضع العناوين الأساسية
            worksheet = spreadsheet.add_worksheet(
                title=worksheet_name,
                rows=1000,
                cols=len(default_headers)
            )
            worksheet.append_row(default_headers)
        
        return worksheet
        
    except Exception as e:
        st.error(f"❌ خطأ في الاتصال بصفحة {worksheet_name}: {e}")
        return None

def get_sales_worksheet():
    """الحصول على ورقة المبيعات"""
    return get_worksheet(SALES_WORKSHEET, ["التاريخ", "المنتج", "الكمية", "إجمالي المبيعات", "التقييم"])

def get_products_worksheet():
    """الحصول على ورقة المنيو (Menu)"""
    return get_worksheet(PRODUCTS_WORKSHEET, ["اسم المنتج", "السعر", "التقييم", "التصنيف", "الوصف", "متاح"])

def get_daily_summary_worksheet():
    """الحصول على ورقة الملخص اليومي"""
    return get_worksheet(DAILY_SUMMARY_WORKSHEET, ["التاريخ", "إجمالي المبيعات", "عدد الفواتير", "عدد الأكواب", "متوسط التقييم"])

def get_categories_worksheet():
    """الحصول على ورقة التصنيفات"""
    return get_worksheet(CATEGORIES_WORKSHEET, ["اسم التصنيف", "الوصف", "الترتيب"])

def get_expenses_worksheet():
    """الحصول على ورقة المصروفات"""
    return get_worksheet(EXPENSES_WORKSHEET, ["التاريخ", "البند", "التصنيف", "المبلغ", "ملاحظات"])

def reset_connection():
    """إعادة تعيين الاتصال وتفريغ الذاكرة المؤقتة"""
    get_client.clear()
    st.cache_resource.clear()

def test_connection():
    """اختبار الاتصال بـ Google Sheets"""
    try:
        worksheet = get_sales_worksheet()
        if worksheet:
            print("✅ تم الاتصال بـ Google Sheets بنجاح!")
            return True
        return False
    except Exception as e:
        print(f"❌ فشل الاتصال: {e}")
        return False

if __name__ == "__main__":
    test_connection()
