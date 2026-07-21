"""
ملف إعدادات الاتصال بـ Google Sheets (يدعم العمل المحلي والسحابي على Streamlit Cloud)
"""

import gspread
from google.oauth2.service_account import Credentials
import streamlit as st
import os
import re

# 1. معرف الـ Google Sheet
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
    """الاتصال التلقائي: يقرأ من Secrets على السحابة، ومن credentials.json محلياً"""
    # أولاً: تجربة القراءة من Secrets (Streamlit Cloud)
    if "gcp_service_account" in st.secrets:
        try:
            creds_dict = dict(st.secrets["gcp_service_account"])
            raw_key = str(creds_dict.get("private_key", "")).replace("\\n", "\n")
            
            # استخراج المفتاح النظيف
            match = re.search(r"(-----BEGIN PRIVATE KEY-----.+?-----END PRIVATE KEY-----)", raw_key, re.DOTALL)
            if match:
                creds_dict["private_key"] = match.group(1)
            
            creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
            return gspread.authorize(creds)
        except Exception as e:
            st.error(f"❌ خطأ عند الاتصال عبر Secrets: {e}")

    # ثانياً: إذا لم تتوفر Secrets، تجربة القراءة من الملف المحلي (Local)
    if os.path.exists("credentials.json"):
        try:
            creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
            return gspread.authorize(creds)
        except Exception as e:
            st.error(f"❌ خطأ عند الاتصال عبر credentials.json: {e}")

    st.error("❌ لم يتم العثور على بيانات الاعتماد (لا في Secrets ولا في credentials.json)")
    return None

def get_spreadsheet():
    """الحصول على ملف الـ Spreadsheet"""
    client = get_client()
    if client:
        return client.open_by_key(SHEET_ID)
    return None

def get_worksheet(worksheet_name, default_headers):
    """الحصول على ورقة عمل أو إنشائها"""
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
        st.error(f"❌ خطأ في الوصول لورقة {worksheet_name}: {e}")
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
