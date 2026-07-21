#!/bin/bash
# سكربت إعداد للاستخدام على Streamlit Cloud

echo "📦 إعداد بيئة نظام كاشير المقهى..."

# إنشاء مجلد backups إذا لم يكن موجوداً
mkdir -p backups

# إنشاء مجلد .streamlit إذا لم يكن موجوداً
mkdir -p .streamlit

# إنشاء ملف بيانات افتراضي إذا لم يكن موجوداً
if [ ! -f "cafe_sales.xlsx" ]; then
    echo "📄 إنشاء ملف بيانات افتراضي..."
    python -c "
import pandas as pd
df = pd.DataFrame(columns=['التاريخ', 'المنتج', 'الكمية', 'إجمالي المبيعات', 'التقييم'])
df.to_excel('cafe_sales.xlsx', index=False)
print('✅ تم إنشاء ملف cafe_sales.xlsx')
"
fi

# إنشاء ملف config إذا لم يكن موجوداً
if [ ! -f ".streamlit/config.toml" ]; then
    echo "⚙️ إنشاء ملف إعدادات Streamlit..."
    cat > .streamlit/config.toml << EOF
[server]
headless = true
port = \$PORT
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#7F5539"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F5F0E9"
textColor = "#4E3526"
font = "sans serif"
EOF
    echo "✅ تم إنشاء ملف config.toml"
fi

echo "✅ تم إعداد المشروع بنجاح!"