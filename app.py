import streamlit as st
import pandas as pd
from datetime import datetime
import os
import json

# 📥 استيراد الصفحات المفصولة
# from tabs.dashboard import render_dashboard
# from tabs.cashier import render_cashier
# from tabs.add_product import render_add_product

from dashboard import render_dashboard 
from cashier import render_cashier
from add_product import render_add_product 
import config
from config import APP_TITLE, FILE_NAME, create_backup, COLORS, USE_GOOGLE_SHEETS

# استيراد Google Sheets إذا كان مفعلاً
if USE_GOOGLE_SHEETS:
    try:
        from google_sheets_config import get_sales_worksheet, get_products_worksheet
        GOOGLE_SHEETS_AVAILABLE = True
    except Exception as e:
        USE_GOOGLE_SHEETS = False
        GOOGLE_SHEETS_AVAILABLE = False
        st.error(f"❌ خطأ في تحميل Google Sheets: {e}")
else:
    GOOGLE_SHEETS_AVAILABLE = False
                    
                    # تحديث المسار في google_sheets_config
    import google_sheets_config
                    google_sheets_config.CREDENTIALS_FILE = temp_creds_file
            except Exception as e:
                st.warning(f"⚠️ خطأ في قراءة credentials من secrets: {e}")
        
        from google_sheets_config import get_sales_worksheet, get_products_worksheet
        GOOGLE_SHEETS_AVAILABLE = True
    except Exception as e:
        USE_GOOGLE_SHEETS = False
        GOOGLE_SHEETS_AVAILABLE = False
        st.error(f"❌ خطأ في تحميل Google Sheets: {e}")
else:
    GOOGLE_SHEETS_AVAILABLE = False

# 1. إعدادات الصفحة والـ CSS الموحد
st.set_page_config(page_title=APP_TITLE, layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    /* تصميم عام مع هوامش جانبية مريحة للعين (حوالي 4% لكل جانب) */
    .reportview-container .main .block-container { 
        direction: rtl; 
        padding-left: 4% !important;
        padding-right: 4% !important;
        max-width: none !important;
        padding-top: 20px !important;
        padding-bottom: 30px !important;
    }
    
    h1, h2, h3, h4, h5, h6, p, span, label, div { 
        text-align: right; 
        font-family: 'Segoe UI', 'Tahoma', 'Geneva', 'Verdana', sans-serif; 
    }
    
    /* هوامش للتبويبات */
    .stTabs [data-baseweb="tab-list"] {
        margin-left: 2% !important;
        margin-right: 2% !important;
        margin-top: 10px !important;
        margin-bottom: 20px !important;
    }
    
    /* هوامش للعناصر الداخلية */
    .stColumn {
        padding-left: 6px !important;
        padding-right: 6px !important;
    }
    
    /* هوامش للكروت والعناصر */
    .kpi-card, .menu-card, .invoice-container, .filter-container,
    .settings-card, .product-form-container {
        margin-left: 3px !important;
        margin-right: 3px !important;
    }
    
    /* هوامش للجداول */
    .dataframe {
        margin-left: 3px !important;
        margin-right: 3px !important;
    }
    
    /* هوامش للأزرار */
    div.stButton > button {
        margin-left: 1px !important;
        margin-right: 1px !important;
    }
    
    /* هوامش للرؤوس */
    .dashboard-header, .invoice-header {
        margin-left: 3px !important;
        margin-right: 3px !important;
    }
    
    /* هوامش عامة إضافية */
    .stMarkdown {
        margin-left: 3px !important;
        margin-right: 3px !important;
    }
    
    .stDataFrame {
        margin-left: 3px !important;
        margin-right: 3px !important;
    }
    
    .stPlotlyChart {
        margin-left: 3px !important;
        margin-right: 3px !important;
    }
    
    /* هوامش عامة لجميع العناصر */
    .main > div {
        padding-left: 4% !important;
        padding-right: 4% !important;
    }
    
    /* هوامش لجميع العناصر داخل التبويبات */
    .tab-content > div {
        padding-left: 4% !important;
        padding-right: 4% !important;
    }
    
    /* تصميم التبويبات */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #F8F5F0;
        padding: 12px 16px;
        border-radius: 12px;
        margin-bottom: 25px;
        max-width: 1200px;
        margin-left: auto;
        margin-right: auto;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        color: #7F5539;
        background-color: #FFFFFF;
        border: 1px solid #E6CCB2;
        transition: all 0.3s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #EDE0D4;
        transform: translateY(-2px);
    }
    .stTabs [aria-selected="true"] {
        background-color: #7F5539 !important;
        color: white !important;
        border-color: #7F5539 !important;
        box-shadow: 0 4px 12px rgba(127, 85, 57, 0.2);
    }
    
    /* ستايلات الإحصائيات */
    .kpi-card { 
        background: linear-gradient(135deg, #FFFFFF 0%, #FDFAF7 100%); 
        padding: 25px; 
        border-radius: 18px; 
        box-shadow: 0 8px 30px rgba(127, 85, 57, 0.08); 
        border-left: 5px solid #7F5539; 
        text-align: center; 
        width: 100%; 
        transition: all 0.3s ease; 
        position: relative;
        overflow: hidden;
    }
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #7F5539 0%, #B08968 100%);
    }
    .kpi-card:hover { 
        transform: translateY(-8px); 
        box-shadow: 0 15px 40px rgba(127, 85, 57, 0.15); 
    }
    .kpi-title { 
        font-size: 0.95rem; 
        color: #B08968; 
        font-weight: 600; 
        margin-bottom: 10px; 
        text-align: center; 
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
    }
    .kpi-value { 
        font-size: 2rem; 
        font-weight: 800; 
        color: #4E3526; 
        text-align: center; 
        margin: 10px 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* ستايلات المنيو */
    .menu-card { 
        background: #FFFFFF; 
        border: 1px solid #E6CCB2; 
        border-radius: 18px; 
        overflow: hidden; 
        box-shadow: 0 6px 20px rgba(127, 85, 57, 0.06); 
        margin-bottom: 20px; 
        text-align: center; 
        transition: all 0.3s ease;
        position: relative;
    }
    .menu-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 25px rgba(127, 85, 57, 0.12);
    }
    .menu-img { 
        width: 100% !important; 
        height: 180px !important; 
        object-fit: cover !important; 
        display: block; 
        transition: transform 0.3s ease;
    }
    .menu-card:hover .menu-img {
        transform: scale(1.05);
    }
    .menu-content { 
        padding: 20px 15px; 
        background-color: #FFFFFF; 
        position: relative;
    }
    .menu-title { 
        font-size: 1.2rem; 
        font-weight: 700; 
        color: #4E3526; 
        margin-bottom: 10px; 
        text-align: center; 
    }
    .menu-price { 
        font-size: 1rem; 
        color: #7F5539; 
        font-weight: 700; 
        background: linear-gradient(135deg, #EDE0D4 0%, #F5E9DC 100%); 
        padding: 8px 20px; 
        border-radius: 25px; 
        display: inline-block; 
        text-align: center; 
        box-shadow: 0 4px 8px rgba(127, 85, 57, 0.1);
    }

    /* ستايلات الأزرار */
    div.stButton > button { 
        width: 100% !important; 
        border-radius: 12px !important; 
        background: linear-gradient(135deg, #7F5539 0%, #B08968 100%) !important; 
        color: white !important; 
        font-weight: 700 !important; 
        border: none !important; 
        padding: 12px !important; 
        margin-top: 15px !important; 
        transition: all 0.3s ease !important; 
        box-shadow: 0 4px 12px rgba(127, 85, 57, 0.2) !important;
    }
    div.stButton > button:hover { 
        background: linear-gradient(135deg, #4E3526 0%, #7F5539 100%) !important; 
        transform: translateY(-2px);
        box-shadow: 0 6px 18px rgba(127, 85, 57, 0.3) !important;
    }
    
    /* ستايل الفاتورة */
    .invoice-container { 
        background: linear-gradient(135deg, #FFFDFB 0%, #FDFAF7 100%); 
        padding: 30px; 
        border-radius: 20px; 
        border: 2px solid #DDB892; 
        box-shadow: 0 8px 30px rgba(0,0,0,0.06); 
        position: sticky;
        top: 20px;
    }
    .invoice-header { 
        border-bottom: 2px dashed #DDB892; 
        padding-bottom: 15px; 
        margin-bottom: 20px; 
        text-align: center; 
        color: #7F5539; 
        font-weight: 800; 
        font-size: 1.3rem;
        letter-spacing: 1px;
    }
    .invoice-total { 
        background: linear-gradient(135deg, #7F5539 0%, #4E3526 100%); 
        color: white; 
        padding: 20px; 
        border-radius: 15px; 
        text-align: center; 
        margin-top: 25px; 
        font-size: 1.5rem; 
        font-weight: 800; 
        box-shadow: 0 6px 20px rgba(127, 85, 57, 0.2);
    }
    
    /* تصميم الفلاتر */
    .filter-container {
        background: linear-gradient(135deg, #F8F5F0 0%, #F5F0E9 100%);
        padding: 25px;
        border-radius: 18px;
        border: 1px solid #E6CCB2;
        box-shadow: 0 6px 20px rgba(127, 85, 57, 0.05);
        margin-bottom: 30px;
    }
    
    /* تصميم الجداول */
    .dataframe {
        border-radius: 12px !important;
        overflow: hidden !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important;
    }
    
    /* تصميم الإعدادات */
    .settings-card {
        background: linear-gradient(135deg, #FFFFFF 0%, #FDFAF7 100%);
        padding: 25px;
        border-radius: 18px;
        border: 1px solid #E6CCB2;
        box-shadow: 0 6px 20px rgba(127, 85, 57, 0.06);
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }
    .settings-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(127, 85, 57, 0.1);
    }
    
    /* تصميم المنتجات */
    .product-form-container {
        background: linear-gradient(135deg, #F8F5F0 0%, #F5F0E9 100%);
        padding: 30px;
        border-radius: 20px;
        border: 1px solid #E6CCB2;
        box-shadow: 0 8px 25px rgba(127, 85, 57, 0.08);
        margin-top: 25px;
    }
    </style>
""", unsafe_allow_html=True)

# FILE_NAME تم تعريفه في config.py

# تهيئة متغيرات الجلسة
if "current_invoice" not in st.session_state:
    st.session_state.current_invoice = []

if "authenticated" not in st.session_state:
    st.session_state.authenticated = True  # مؤقتاً للاختبار

if "backup_created" not in st.session_state:
    st.session_state.backup_created = False

# 💾 دوال إدارة البيانات المشتركة
def load_sales_data():
    """تحميل بيانات المبيعات من Google Sheets أو Excel"""
    if USE_GOOGLE_SHEETS and GOOGLE_SHEETS_AVAILABLE:
        return load_sales_from_google_sheets()
    else:
        return load_sales_from_excel()

def load_products_data():
    """تحميل بيانات المنتجات من Google Sheets"""
    if USE_GOOGLE_SHEETS and GOOGLE_SHEETS_AVAILABLE:
        return load_products_from_google_sheets()
    else:
        # إذا لم يكن Google Sheets، نستخدم المنتجات الافتراضية
        return pd.DataFrame(config.DEFAULT_PRODUCTS)

def load_sales_from_excel():
    """تحميل بيانات المبيعات من ملف Excel"""
    try:
        if not st.session_state.backup_created:
            if create_backup():
                st.session_state.backup_created = True
            
        df = pd.read_excel(FILE_NAME)
        if not df.empty and "التاريخ" in df.columns:
            df["التاريخ"] = pd.to_datetime(df["التاريخ"]).dt.strftime("%Y-%m-%d")
        return df
    except FileNotFoundError:
        df = pd.DataFrame(columns=["التاريخ", "المنتج", "الكمية", "إجمالي المبيعات", "التقييم"])
        df.to_excel(FILE_NAME, index=False)
        return df
    except Exception as e:
        st.error(f"❌ خطأ في تحميل بيانات المبيعات: {e}")
        return pd.DataFrame(columns=["التاريخ", "المنتج", "الكمية", "إجمالي المبيعات", "التقييم"])

def load_sales_from_google_sheets():
    """تحميل بيانات المبيعات من Google Sheets"""
    try:
        worksheet = get_sales_worksheet()
        data = worksheet.get_all_records()
        
        if not data:
            return pd.DataFrame(columns=["التاريخ", "المنتج", "الكمية", "إجمالي المبيعات", "التقييم"])
        
        df = pd.DataFrame(data)
        
        # تصفية الصفوف التي تحتوي على عناوين
        if not df.empty:
            if "التاريخ" in df.columns:
                df = df[df["التاريخ"] != "التاريخ"]
            if "المنتج" in df.columns:
                df = df.dropna(subset=["المنتج"], how="all")
        
        if not df.empty and "التاريخ" in df.columns:
            df["التاريخ"] = pd.to_datetime(df["التاريخ"], errors='coerce').dt.strftime("%Y-%m-%d")
        
        return df
    except Exception as e:
        st.error(f"❌ خطأ في تحميل بيانات المبيعات من Google Sheets: {e}")
        return pd.DataFrame(columns=["التاريخ", "المنتج", "الكمية", "إجمالي المبيعات", "التقييم"])

def load_products_from_google_sheets():
    """تحميل بيانات المنيو من Google Sheets (صفحة Menu)"""
    try:
        worksheet = get_products_worksheet()
        data = worksheet.get_all_records()
        
        if not data:
            # إذا كانت صفحة Menu فارغة، نستخدم المنتجات الافتراضية
            return pd.DataFrame(config.DEFAULT_PRODUCTS)
        
        df = pd.DataFrame(data)
        
        # إعادة تسمية الأعمدة لتتناسب مع التطبيق
        if not df.empty:
            df = df.rename(columns={
                "اسم المنتج": "name",
                "السعر": "price",
                "التقييم": "rating"
            })
            
            # تحويل السعر إلى رقم
            if "price" in df.columns:
                df["price"] = pd.to_numeric(df["price"], errors='coerce').fillna(15)
            
            # إضافة عمود الصورة افتراضياً
            if "image" not in df.columns:
                df["image"] = "https://images.unsplash.com/photo-1577968897966-3d4325b36b61?w=600&q=80"
            
            # التأكد من وجود عمود name
            if "name" not in df.columns:
                df["name"] = df.index.astype(str)
        
        return df
    except Exception as e:
        st.error(f"❌ خطأ في تحميل بيانات المنيو من Google Sheets: {e}")
        return pd.DataFrame(config.DEFAULT_PRODUCTS)

def save_invoice_to_excel():
    """حفظ الفاتورة في Google Sheets أو Excel"""
    if not st.session_state.current_invoice:
        st.warning("⚠️ لا توجد عناصر في الفاتورة للحفظ")
        return False
    
    if USE_GOOGLE_SHEETS and GOOGLE_SHEETS_AVAILABLE:
        return save_invoice_to_google_sheets()
    else:
        return save_invoice_to_excel_file()

def save_invoice_to_excel_file():
    """حفظ الفاتورة في ملف Excel"""
    try:
        df = load_sales_from_excel()
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        for item in st.session_state.current_invoice:
            product_name = item["المنتج"]
            new_qty = item["الكمية"]
            new_total = item["الإجمالي"]
            
            if not product_name or new_qty <= 0 or new_total <= 0:
                st.error(f"❌ بيانات غير صالحة للمنتج: {product_name}")
                continue
            
            condition = (df["المنتج"] == product_name) & (df["التاريخ"] == current_date)
            
            if not df.empty and condition.any():
                df.loc[condition, "الكمية"] += new_qty
                df.loc[condition, "إجمالي المبيعات"] += new_total
            else:
                new_row = pd.DataFrame([{
                    "التاريخ": current_date,
                    "المنتج": product_name,
                    "الكمية": new_qty,
                    "إجمالي المبيعات": new_total,
                    "التقييم": 4.8
                }])
                df = pd.concat([df, new_row], ignore_index=True)
        
        df.to_excel(FILE_NAME, index=False)
        create_backup()
        
        st.session_state.current_invoice = []
        try:
            st.cache_data.clear()
        except:
            pass
        
        return True
        
    except Exception as e:
        st.error(f"❌ خطأ في حفظ الفاتورة: {e}")
        return False

def save_invoice_to_google_sheets():
    """حفظ الفاتورة في Google Sheets (صفحة Sales)"""
    try:
        sales_worksheet = get_sales_worksheet()
        products_worksheet = get_products_worksheet()
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # عداد للمنتجات المضافة
        added_count = 0
        total_amount = 0
        
        # إضافة كل منتج في الفاتورة كصف جديد في صفحة Sales
        for item in st.session_state.current_invoice:
            product_name = item["المنتج"]
            new_qty = item["الكمية"]
            product_price = item["السعر"]  # السعر من الفاتورة
            
            if not product_name or new_qty <= 0 or product_price <= 0:
                continue
            
            # حساب الإجمالي = السعر × الكمية
            new_total = float(product_price) * int(new_qty)
            
            # إضافة صف جديد في صفحة Sales
            sales_worksheet.append_row([
                current_date,
                product_name,
                int(new_qty),
                float(new_total),
                4.5  # تقييم افتراضي
            ])
            
            added_count += 1
            total_amount += new_total
        
        # تفريغ السلة
        st.session_state.current_invoice = []
        
        # إعادة تعيين الاتصال لضمان تحديث البيانات
        from google_sheets_config import reset_connection
        reset_connection()
        
        # عرض رسالة نجاح مع التفاصيل
        st.success(f"✅ تم حفظ {added_count} منتج بإجمالي {total_amount} ريال")
        
        return True
        
    except Exception as e:
        st.error(f"❌ خطأ في حفظ الفاتورة في Google Sheets: {e}")
        return False

# 🔐 نظام مصادقة بسيط (مؤقتاً للاختبار)
if not st.session_state.authenticated:
    st.title("🔐 نظام المصادقة")
    password = st.text_input("كلمة المرور:", type="password")
    
    if st.button("تسجيل الدخول"):
        if password == "admin123":  # كلمة مرور افتراضية
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("❌ كلمة المرور غير صحيحة")
    st.stop()

# 🗂️ إنشاء التبويبات مع استدعاء load_data() داخل كل تبويب لضمان التحديث اللحظي
tab1, tab2, tab3, tab4 = st.tabs(["📊 لوحة التحكم", "☕ المنيو والبيع", "➕ إدارة المنتجات", "⚙️ الإعدادات"])

with tab1:
    df_sales = load_sales_data()
    render_dashboard(df_sales)

with tab2:
    df_products = load_products_data()
    render_cashier(df_products, save_invoice_to_excel)

with tab3:
    render_add_product(load_products_data, load_sales_data, save_invoice_to_excel)

with tab4:
    st.markdown('''
        <div style="background: linear-gradient(135deg, #7F5539 0%, #4E3526 100%); 
                 color: white; 
                 padding: 25px; 
                 border-radius: 20px; 
                 margin-bottom: 30px;
                 text-align: center;
                 box-shadow: 0 8px 30px rgba(127, 85, 57, 0.2);">
            <h1 style="color: white; font-size: 2rem; font-weight: 800; margin-bottom: 10px;">⚙️ إعدادات النظام</h1>
            <p style="color: #EDE0D4; font-size: 1.1rem;">إدارة النظام والأدوات المتقدمة</p>
        </div>
    ''', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('''
            <div class="settings-card">
                <h3 style="color: #4E3526; font-weight: 700; margin-bottom: 20px; text-align: center;">
                    📊 معلومات النظام
                </h3>
        ''', unsafe_allow_html=True)
        
        if USE_GOOGLE_SHEETS and GOOGLE_SHEETS_AVAILABLE:
            st.markdown('''
                <div style="background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%); 
                         color: white; 
                         padding: 15px; 
                         border-radius: 12px; 
                         margin-bottom: 20px;
                         text-align: center;">
                    <div style="font-size: 1.2rem; margin-bottom: 5px;">🌐</div>
                    <div style="font-weight: 700; font-size: 1.1rem;">متصل بـ Google Sheets</div>
                </div>
            ''', unsafe_allow_html=True)
            
            from google_sheets_config import SHEET_ID
            st.markdown(f'''
                <div style="background: #F5F0E9; 
                         padding: 15px; 
                         border-radius: 12px; 
                         margin-bottom: 15px;
                         border-left: 4px solid #7F5539;">
                    <div style="color: #4E3526; font-weight: 600; margin-bottom: 5px;">معرف الـ Sheet:</div>
                    <div style="color: #7F5539; font-family: monospace; background: #EDE0D4; padding: 8px; border-radius: 8px;">{SHEET_ID}</div>
                </div>
            ''', unsafe_allow_html=True)
            
            # عرض عدد السجلات
            try:
                df_temp = load_sales_data()
                sales_count = len(df_temp)
                df_products_temp = load_products_data()
                products_count = len(df_products_temp)
                
                st.markdown(f'''
                    <div style="display: flex; gap: 15px; margin-bottom: 20px;">
                        <div style="flex: 1; background: #F5F0E9; padding: 15px; border-radius: 12px; text-align: center; border-top: 4px solid #7F5539;">
                            <div style="color: #4E3526; font-weight: 600; margin-bottom: 5px;">📦 سجلات المبيعات</div>
                            <div style="color: #7F5539; font-size: 1.5rem; font-weight: 800;">{sales_count}</div>
                        </div>
                        <div style="flex: 1; background: #F5F0E9; padding: 15px; border-radius: 12px; text-align: center; border-top: 4px solid #B08968;">
                            <div style="color: #4E3526; font-weight: 600; margin-bottom: 5px;">☕ المنتجات</div>
                            <div style="color: #7F5539; font-size: 1.5rem; font-weight: 800;">{products_count}</div>
                        </div>
                    </div>
                ''', unsafe_allow_html=True)
            except:
                pass
        else:
            st.markdown(f'''
                <div style="background: #F5F0E9; 
                         padding: 15px; 
                         border-radius: 12px; 
                         margin-bottom: 15px;
                         border-left: 4px solid #7F5539;">
                    <div style="color: #4E3526; font-weight: 600; margin-bottom: 5px;">مسار ملف البيانات:</div>
                    <div style="color: #7F5539; font-family: monospace; background: #EDE0D4; padding: 8px; border-radius: 8px;">{FILE_NAME}</div>
                </div>
            ''', unsafe_allow_html=True)
            
            if os.path.exists(FILE_NAME):
                file_size = os.path.getsize(FILE_NAME) / 1024
                st.markdown(f'''
                    <div style="background: #F5F0E9; 
                             padding: 15px; 
                             border-radius: 12px; 
                             margin-bottom: 15px;
                             border-left: 4px solid #B08968;">
                        <div style="color: #4E3526; font-weight: 600; margin-bottom: 5px;">حجم ملف البيانات:</div>
                        <div style="color: #7F5539; font-size: 1.2rem; font-weight: 700;">{file_size:.2f} كيلوبايت</div>
                    </div>
                ''', unsafe_allow_html=True)
        
        # عرض عدد النسخ الاحتياطية
        from config import BACKUP_DIR
        if os.path.exists(BACKUP_DIR):
            backup_files = [f for f in os.listdir(BACKUP_DIR) if f.endswith('.xlsx')]
            st.markdown(f'''
                <div style="background: #F5F0E9; 
                         padding: 15px; 
                         border-radius: 12px; 
                         border-left: 4px solid #DDB892;">
                    <div style="color: #4E3526; font-weight: 600; margin-bottom: 5px;">💾 عدد النسخ الاحتياطية:</div>
                    <div style="color: #7F5539; font-size: 1.2rem; font-weight: 700;">{len(backup_files)}</div>
                </div>
            ''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('''
            <div class="settings-card">
                <h3 style="color: #4E3526; font-weight: 700; margin-bottom: 20px; text-align: center;">
                    🔧 أدوات النظام
                </h3>
        ''', unsafe_allow_html=True)
        
        # أزرار الأدوات
        tool_buttons = [
            ("🔄 إنشاء نسخة احتياطية الآن", "إنشاء نسخة احتياطية من جميع البيانات", "#7F5539"),
            ("🗑️ تفريغ ذاكرة التخزين المؤقت", "مسح ذاكرة التخزين المؤقت لتحسين الأداء", "#B08968"),
            ("🚪 تسجيل الخروج", "تسجيل الخروج من النظام", "#4E3526")
        ]
        
        for btn_text, btn_help, btn_color in tool_buttons:
            st.markdown(f'''
                <div style="margin-bottom: 15px;">
                    <div style="color: #4E3526; font-weight: 600; margin-bottom: 5px; font-size: 0.9rem;">{btn_help}</div>
            ''', unsafe_allow_html=True)
            
            if btn_text == "🔄 إنشاء نسخة احتياطية الآن":
                if st.button(btn_text, use_container_width=True, key=f"btn_{btn_text}"):
                    if create_backup():
                        st.success("✅ تم إنشاء نسخة احتياطية بنجاح")
                    else:
                        st.error("❌ فشل في إنشاء النسخة الاحتياطية")
            elif btn_text == "🗑️ تفريغ ذاكرة التخزين المؤقت":
                if st.button(btn_text, use_container_width=True, key=f"btn_{btn_text}"):
                    try:
                        st.cache_data.clear()
                        st.success("✅ تم تفريغ ذاكرة التخزين المؤقت")
                    except:
                        st.error("❌ فشل في تفريغ الذاكرة")
            elif btn_text == "🚪 تسجيل الخروج":
                if st.button(btn_text, use_container_width=True, key=f"btn_{btn_text}"):
                    st.session_state.authenticated = False
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
