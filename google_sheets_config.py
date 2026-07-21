"""
ملف إعدادات الاتصال بـ Google Sheets (معدل لمعالجة خطأ PEM File / InvalidByte)
"""

import gspread
from google.oauth2.service_account import Credentials
import streamlit as st

# 1. معرف الـ Google Sheet
try:
    SHEET_ID = st.secrets["google"]["sheet_id"]
except:
    SHEET_ID = "1URic7Z7Gm4fKDYILnH9meYnl25o2E6nbnVizgpXMijg"

# 2. أسماء أوراق العمل
SALES_WORKSHEET = "Sales"
PRODUCTS_WORKSHEET = "Menu"
DAILY_SUMMARY_WORKSHEET = "Daily_Summary"
CATEGORIES_WORKSHEET = "Categories"
EXPENSES_WORKSHEET = "Expenses"

# 3. الصلاحيات
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

@st.cache_resource
def get_client():
    """الحصول على عميل Google Sheets مع تنظيف تلقائي للمفتاح الخاص"""
    try:
        if "gcp_service_account" not in st.secrets:
            st.error("❌ لم يتم العثور على [gcp_service_account] في إعدادات Secrets")
            return None
            
        creds_dict = dict(st.secrets["gcp_service_account"])
        
        # 🚨 تنظيف ومعالجة المفتاح الخاص (Private Key) لحل خطأ PEM File 🚨
        private_key = str(creds_dict.get("private_key", "")).strip()
        
        # 1. تحويل \\n إلى \n حقيقية
        private_key = private_key.replace("\\n", "\n")
        
        # 2. قص المفتاح بين BGIN و END بدقة والتخلص من أي رموز أو نقاط زائدة قبله
        if "-----BEGIN PRIVATE KEY-----" in private_key and "-----END PRIVATE KEY-----" in private_key:
            start_pos = private_key.find("-----BEGIN PRIVATE KEY-----")
            end_pos = private_key.rfind("-----END PRIVATE KEY-----") + len("-----END PRIVATE KEY-----")
            private_key = private_key[start_pos:end_pos]
            
        # 3. إزالة أي علامات تنصيص محيطة بالمفتاح
        private_key = private_key.strip("'\"")
        
        # تحديث المفتاح بعد التنظيف
        creds_dict["private_key"] = private_key

        # إنشاء الاعتماد والاتصال
        creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
        return gspread.authorize(creds)
        
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
    return get_worksheet(SALES_WORKSHEET, ["التاريخ", "المنتج", "الكمية", "إجمالي المبيعات", "التقييم"])

def get_products_worksheet():
    return get_worksheet(PRODUCTS_WORKSHEET, ["اسم المنتج", "السعر", "التقييم", "التصنيف", "الوصف", "متاح"])

def get_daily_summary_worksheet():
    return get_worksheet(DAILY_SUMMARY_WORKSHEET, ["التاريخ", "إجمالي المبيعات", "عدد الفواتير", "عدد الأكواب", "متوسط التقييم"])

def get_categories_worksheet():
    return get_worksheet(CATEGORIES_WORKSHEET, ["اسم التصنيف", "الوصف", "الترتيب"])

def get_expenses_worksheet():
    return get_worksheet(EXPENSES_WORKSHEET, ["التاريخ", "البند", "التصنيف", "المبلغ", "ملاحظات"])

def reset_connection():
    get_client.clear()
    st.cache_resource.clear()
