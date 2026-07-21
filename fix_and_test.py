"""إصلاح البيانات واختبار النظام"""

from google_sheets_config import get_google_sheets_client
from datetime import datetime

# الاتصال بـ Google Sheets
worksheet = get_google_sheets_client()

# مسح البيانات القديمة
worksheet.clear()

# إضافة العناوين
worksheet.append_row(["التاريخ", "المنتج", "الكمية", "إجمالي المبيعات", "التقييم"])

# إضافة منتجات افتراضية
today = datetime.now().strftime("%Y-%m-%d")

products = [
    ["2026-07-21", "فلات وايت", 5, 90, 4.8],
    ["2026-07-21", "سبنش لاتيه", 3, 60, 4.7],
    ["2026-07-21", "إسبريسو", 4, 48, 4.9],
    ["2026-07-21", "كابتشينو", 6, 102, 4.6],
    ["2026-07-21", "كورتادو", 2, 32, 4.5],
    ["2026-07-21", "موكا", 3, 66, 4.7],
]

for product in products:
    worksheet.append_row(product)
    print(f"✅ تم إضافة: {product[1]}")

print("\n🎉 تم إضافة جميع المنتجات بنجاح!")

# التحقق
data = worksheet.get_all_records()
print(f"\n📊 إجمالي السجلات: {len(data)}")

products_list = set()
for row in data:
    if row.get('المنتج') and row['المنتج'] != 'المنتج':
        products_list.add(row['المنتج'])

print(f"☕ المنتجات المتاحة: {len(products_list)}")
for p in sorted(products_list):
    print(f"   • {p}")
