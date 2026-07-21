"""فحص البيانات في Google Sheets"""

from google_sheets_config import get_google_sheets_client
import json

worksheet = get_google_sheets_client()
data = worksheet.get_all_records()

print('=== البيانات الخام من Google Sheets ===')
print(f'عدد السجلات: {len(data)}')
print()

for i, row in enumerate(data):
    print(f'السجل {i+1}: {json.dumps(row, ensure_ascii=False)}')

# عرض المنتجات الفريدة
if data:
    products = set()
    for row in data:
        product = row.get('المنتج')
        if product and product != 'المنتج':
            products.add(product)
    
    print(f'\n=== المنتجات الفريدة ({len(products)}) ===')
    for p in sorted(products):
        print(f'  • {p}')
