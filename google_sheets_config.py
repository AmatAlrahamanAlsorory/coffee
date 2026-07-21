"""
ملف إعدادات الاتصال بـ Google Sheets (للعمل مع Streamlit Cloud)
"""

import gspread
from google.oauth2.service_account import Credentials
import os
import json
import streamlit as st

# معرف الـ Google Sheet (يمكن ضبطه عبر متغير البيئة أو secrets)
SHEET_ID = os.environ.get("GOOGLE_SHEET_ID", st.secrets.get("google", {}).get("sheet_id", "1URic7Z7Gm4fKDYILnH9meYnl25o2E6nbnVizgpXMijg"))

# مسار ملف credentials (من secrets)
CREDENTIALS_FILE = st.secrets.get("google", {}).get("credentials_path", "credentials.json")

# أسماء أوراق العمل داخل الـ Sheet
SALES_WORKSHEET = "Sales"              # صفحة المبيعات
PRODUCTS_WORKSHEET = "Menu"            # صفحة المنيو
DAILY_SUMMARY_WORKSHEET = "Daily_Summary"  # الملخص اليومي
CATEGORIES_WORKSHEET = "Categories"    # التصنيفات
EXPENSES_WORKSHEET = "Expenses"        # المصروفات

# نطاقات الصلاحيات المطلوبة
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets"
]

# متغير عام لتخزين العميل (لمنع إعادة الاتصال المتكرر)
_client = None
_spreadsheet = None

def get_credentials():
    """الحصول على بيانات الاعتماد من ملف credentials.json"""
    global CREDENTIALS_FILE
    
    try:
        # التحقق مما إذا كان الملف موجوداً
        if not os.path.exists(CREDENTIALS_FILE):
            print(f"⚠️ ملف credentials.json غير موجود: {CREDENTIALS_FILE}")
            return None
        
        # قراءة الملف كـ JSON
        with open(CREDENTIALS_FILE, 'r', encoding='utf-8') as f:
            creds_data = json.load(f)
        
        # التحقق من وجود private_key
        if "private_key" not in creds_data:
            print("⚠️ لم يتم العثور على private_key في credentials.json")
            return None
        
        # إنشاء Credentials
        creds = Credentials.from_service_account_info(creds_data, scopes=SCOPES)
        return creds
        
    except Exception as e:
        print(f"❌ خطأ في قراءة credentials: {e}")
        return None

def get_client():
    """الحصول على عميل Google Sheets (مع التخزين المؤقت)"""
    global _client
    
    if _client is not None:
        return _client
    
    creds = get_credentials()
    if creds is None:
        raise RuntimeError("❌ لم يتم العثور على بيانات اعتماد Google Sheets")
    
    _client = gspread.authorize(creds)
    return _client

def get_spreadsheet():
    """الحصول على الـ Spreadsheet (مع التخزين المؤقت)"""
    global _spreadsheet
    
    if _spreadsheet is not None:
        return _spreadsheet
    
    client = get_client()
    _spreadsheet = client.open_by_key(SHEET_ID)
    return _spreadsheet

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

def get_worksheet(worksheet_name, default_headers):
    """
    الحصول على ورقة عمل مع إنشائها إذا لم تكن موجودة
    """
    try:
        spreadsheet = get_spreadsheet()
        
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
        st.error(f"❌ خطأ في الاتصال بـ Google Sheets: {e}")
        raise

def reset_connection():
    """إعادة تعيين الاتصال (للاستخدام عند الحاجة)"""
    global _client, _spreadsheet
    _client = None
    _spreadsheet = None

def test_connection():
    """اختبار الاتصال بـ Google Sheets"""
    try:
        worksheet = get_sales_worksheet()
        print("✅ تم الاتصال بـ Google Sheets بنجاح!")
        return True
    except Exception as e:
        print(f"❌ فشل الاتصال: {e}")
        return False


if __name__ == "__main__":
    test_connection()
