"""
ملف إعدادات النظام
"""

import os
from datetime import datetime

# إعدادات الملفات
DATA_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_NAME = os.path.join(DATA_DIR, "cafe_sales.xlsx")
BACKUP_DIR = os.path.join(DATA_DIR, "backups")

# إعدادات Google Sheets
# True = Google Sheets (يحتاج credentials.json)
# False = Excel محلي
USE_GOOGLE_SHEETS = True

# إنشاء مجلد النسخ الاحتياطي إذا لم يكن موجوداً
if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

# إعدادات النظام
APP_TITLE = "نظام كاشير ومبيعات المقهى الذكي"
APP_ICON = "☕"
DEFAULT_CURRENCY = "ريال"
DEFAULT_RATING = 4.5

# إعدادات الألوان
COLORS = {
    "primary": "#7F5539",
    "secondary": "#B08968",
    "light": "#EDE0D4",
    "dark": "#4E3526",
    "accent": "#DDB892"
}

# إعدادات المنتجات الافتراضية
DEFAULT_PRODUCTS = [
    {"name": "فلات وايت", "price": 18, "image": "https://images.unsplash.com/photo-1577968897966-3d4325b36b61?w=600&q=80"},
    {"name": "سبنش لاتيه", "price": 20, "image": "https://images.unsplash.com/photo-1517701604599-bb29b565090c?w=600&q=80"},
    {"name": "قهوة مقطرة V60", "price": 15, "image": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=600&q=80"},
    {"name": "كورتادو", "price": 16, "image": "https://images.unsplash.com/photo-1534778101976-62847782c213?w=600&q=80"},
    {"name": "إسبريسو", "price": 12, "image": "https://images.unsplash.com/photo-1510591509382-74346262656e?w=600&q=80"},
    {"name": "كابتشينو", "price": 17, "image": "https://images.unsplash.com/photo-1534778101976-62847782c213?w=600&q=80"}
]

# دوال مساعدة
def create_backup():
    """إنشاء نسخة احتياطية من البيانات (Excel للنسخ المحلية)"""
    try:
        if USE_GOOGLE_SHEETS:
            # إنشاء نسخة احتياطية في مجلد backups كملف Excel
            from google_sheets_config import get_sales_worksheet, get_products_worksheet
            import pandas as pd
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(BACKUP_DIR, f"cafe_backup_{timestamp}.xlsx")
            
            # تحميل البيانات من Google Sheets
            sales_ws = get_sales_worksheet()
            sales_data = sales_ws.get_all_records()
            df_sales = pd.DataFrame(sales_data)
            
            # حفظ في ملف Excel
            with pd.ExcelWriter(backup_file, engine='openpyxl') as writer:
                df_sales.to_excel(writer, sheet_name='Sales', index=False)
            
            # حذف النسخ القديمة (الاحتفاظ بـ 20 نسخة)
            backup_files = sorted([f for f in os.listdir(BACKUP_DIR) if f.startswith("cafe_backup_")])
            if len(backup_files) > 20:
                for old_file in backup_files[:-20]:
                    os.remove(os.path.join(BACKUP_DIR, old_file))
            
            print(f"✅ تم إنشاء نسخة احتياطية: {backup_file}")
            return True
        
        # للنسخ المحلية (Excel)
        if os.path.exists(FILE_NAME):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(BACKUP_DIR, f"cafe_sales_backup_{timestamp}.xlsx")
            
            import shutil
            shutil.copy2(FILE_NAME, backup_file)
            
            # حذف النسخ القديمة (الاحتفاظ بـ 10 نسخ فقط)
            backup_files = sorted([f for f in os.listdir(BACKUP_DIR) if f.startswith("cafe_sales_backup_")])
            if len(backup_files) > 10:
                for old_file in backup_files[:-10]:
                    os.remove(os.path.join(BACKUP_DIR, old_file))
            
            return True
    except Exception as e:
        print(f"خطأ في إنشاء النسخة الاحتياطية: {e}")
        return False

def get_data_file_path():
    """الحصول على مسار ملف البيانات"""
    return FILE_NAME
