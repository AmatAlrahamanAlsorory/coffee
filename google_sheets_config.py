"""
ملف إعدادات الاتصال بـ Google Sheets مباشرة من ملف credentials.json
"""

import gspread
from google.oauth2.service_account import Credentials
import os

# مسار ملف الاعتماد بجانب الكود مباشرة
CREDENTIALS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "credentials.json")

# معرف الـ Google Sheet
SHEET_ID = "1URic7Z7Gm4fKDYILnH9meYnl25o2E6nbnVizgpXMijg"

# أسماء أوراق العمل
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
    """التحقق من وجود ملف الـ credentials.json"""
    return os.path.exists(CREDENTIALS_FILE)

def get_client():
    """الحصول على عميل Google Sheets باستخدام ملف الـ JSON مباشرة"""
    global _client
    if _client is not None:
        return _client
    
    if not is_google_sheets_enabled():
        raise RuntimeError("ملف credentials.json غير موجود!")
    
    creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
    _client = gspread.authorize(creds)
    return _client

def get_spreadsheet():
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
        print(f"خطأ في الاتصال: {e}")
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
