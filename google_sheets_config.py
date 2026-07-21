"""
ملف إعدادات الاتصال بـ Google Sheets عبر Streamlit Secrets
"""

import gspread
from google.oauth2.service_account import Credentials
import streamlit as st

# معرف الـ Google Sheet
SHEET_ID = "1URic7Z7Gm4fKDYILnH9meYnl25o2E6nbnVizgpXMijg"

# أسماء أوراق العمل داخل الشيت
SALES_WORKSHEET = "Sales"
PRODUCTS_WORKSHEET = "Menu"
DAILY_SUMMARY_WORKSHEET = "Daily_Summary"
CATEGORIES_WORKSHEET = "Categories"
EXPENSES_WORKSHEET = "Expenses"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets"
]

_client = None
_spreadsheet = None

def is_google_sheets_enabled():
    """التحقق مما إذا كانت أسرار Google Sheets متوفرة في إعدادات التطبيق"""
    try:
        return "gcp_service_account" in st.secrets
    except Exception:
        return False

def get_client():
    """الحصول على عميل Google Sheets باستخدام Streamlit Secrets"""
    global _client
    
    if _client is not None:
        return _client
    
    if not is_google_sheets_enabled():
        raise RuntimeError("Google Sheets غير مفعل - يرجى إضافة gcp_service_account في Streamlit Secrets")
    
    # تحويل بيانات الـ secrets إلى قاموس بايثون متوافق مع جوجل
    creds_dict = dict(st.secrets["gcp_service_account"])
    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    _client = gspread.authorize(creds)
    return _client

def get_spreadsheet():
    """الحصول على الـ Spreadsheet"""
    global _spreadsheet
    
    if _spreadsheet is not None:
        return _spreadsheet
    
    client = get_client()
    _spreadsheet = client.open_by_key(SHEET_ID)
    return _spreadsheet

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

def get_worksheet(worksheet_name, default_headers):
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
        print(f"خطأ في الاتصال بـ Google Sheets: {e}")
        raise

def reset_connection():
    global _client, _spreadsheet
    _client = None
    _spreadsheet = None

def test_connection():
    try:
        worksheet = get_sales_worksheet()
        print("تم الاتصال بـ Google Sheets بنجاح!")
        return True
    except Exception as e:
        print(f"فشل الاتصال: {e}")
        return False
