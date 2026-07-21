"""اختبار شامل للتطبيق - محاكاة عمليات البيع والحفظ"""

import sys
import os
sys.path.insert(0, r"c:\Users\Lenovo\Downloads\coffee")

from datetime import datetime
import pandas as pd
from google_sheets_config import get_google_sheets_client
from config import USE_GOOGLE_SHEETS

def print_header(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def test_add_products():
    """اختبار إضافة منتجات متعددة"""
    print_header("☕ اختبار إضافة منتجات جديدة")
    
    try:
        worksheet = get_google_sheets_client()
        
        products = [
            {"name": "فلات وايت", "qty": 3, "total": 54.0, "rating": 4.8},
            {"name": "سبنش لاتيه", "qty": 2, "total": 40.0, "rating": 4.7},
            {"name": "إسبريسو", "qty": 5, "total": 60.0, "rating": 4.9},
            {"name": "كابتشينو", "qty": 4, "total": 68.0, "rating": 4.6},
        ]
        
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        for product in products:
            row = [
                current_date,
                product["name"],
                product["qty"],
                product["total"],
                product["rating"]
            ]
            worksheet.append_row(row)
            print(f"  ✅ تم إضافة: {product['name']} - {product['qty']} كوب - {product['total']} ريال")
        
        return True
        
    except Exception as e:
        print(f"  ❌ خطأ: {e}")
        return False

def test_read_and_analyze():
    """اختبار قراءة البيانات وتحليلها"""
    print_header("📊 اختبار قراءة وتحليل البيانات")
    
    try:
        worksheet = get_google_sheets_client()
        data = worksheet.get_all_records()
        
        # تصفية البيانات الفعلية (استبعاد صف العناوين)
        real_data = [row for row in data if row.get("التاريخ") != "التاريخ" and row.get("المنتج")]
        
        if not real_data:
            print("  ⚠️ لا توجد بيانات للتحليل")
            return False
        
        df = pd.DataFrame(real_data)
        
        # تحويل الأعمدة إلى أرقام
        df["الكمية"] = pd.to_numeric(df["الكمية"], errors="coerce").fillna(0)
        df["إجمالي المبيعات"] = pd.to_numeric(df["إجمالي المبيعات"], errors="coerce").fillna(0)
        df["التقييم"] = pd.to_numeric(df["التقييم"], errors="coerce").fillna(0)
        
        total_sales = df["إجمالي المبيعات"].sum()
        total_qty = df["الكمية"].sum()
        avg_rating = df["التقييم"].mean()
        
        print(f"\n  📈 إحصائيات المبيعات:")
        print(f"     • إجمالي المبيعات: {total_sales:,.0f} ريال")
        print(f"     • عدد الأكواب المباعة: {int(total_qty)} كوب")
        print(f"     • متوسط التقييم: {avg_rating:.1f}/5")
        
        print(f"\n  📋 تفاصيل المنتجات:")
        for _, row in df.iterrows():
            print(f"     • {row['المنتج']}: {int(row['الكمية'])} كوب - {row['إجمالي المبيعات']:.0f} ريال")
        
        return True
        
    except Exception as e:
        print(f"  ❌ خطأ: {e}")
        return False

def test_update_existing():
    """اختبار تحديث منتج موجود"""
    print_header("🔄 اختبار تحديث منتج موجود")
    
    try:
        worksheet = get_google_sheets_client()
        data = worksheet.get_all_records()
        
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # البحث عن منتج لتحديثه
        for i, row in enumerate(data):
            if row.get("المنتج") == "فلات وايت" and row.get("التاريخ") == current_date:
                # تحديث الكمية والإجمالي
                new_qty = int(row.get("الكمية", 0)) + 2
                new_total = float(row.get("إجمالي المبيعات", 0)) + 36
                
                # تحديث الخلايا
                worksheet.update_cell(i + 1, 3, new_qty)
                worksheet.update_cell(i + 1, 4, new_total)
                
                print(f"  ✅ تم تحديث 'فلات وايت':")
                print(f"     الكمية الجديدة: {new_qty} كوب")
                print(f"     الإجمالي الجديد: {new_total} ريال")
                return True
        
        print("  ⚠️ لم يتم العثور على المنتج لتحديثه")
        return False
        
    except Exception as e:
        print(f"  ❌ خطأ: {e}")
        return False

def test_invoice_simulation():
    """محاكاة عملية فاتورة كاملة"""
    print_header("🧾 محاكاة عملية بيع كاملة")
    
    try:
        worksheet = get_google_sheets_client()
        
        # إنشاء فاتورة وهمية
        invoice = [
            {"المنتج": "قهوة مقطرة V60", "الكمية": 2, "السعر": 15, "الإجمالي": 30},
            {"المنتج": "كورتادو", "الكمية": 3, "السعر": 16, "الإجمالي": 48},
        ]
        
        print("\n  📝 تفاصيل الفاتورة:")
        total_invoice = 0
        for item in invoice:
            print(f"     • {item['المنتج']} × {item['الكمية']} = {item['الإجمالي']} ريال")
            total_invoice += item["الإجمالي"]
        print(f"\n  💰 إجمالي الفاتورة: {total_invoice} ريال")
        
        # حفظ الفاتورة
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        for item in invoice:
            row = [
                current_date,
                item["المنتج"],
                item["الكمية"],
                item["الإجمالي"],
                4.7
            ]
            worksheet.append_row(row)
        
        print("\n  ✅ تم حفظ الفاتورة بنجاح في Google Sheets!")
        return True
        
    except Exception as e:
        print(f"  ❌ خطأ: {e}")
        return False

def test_dashboard_data():
    """اختبار جاهزية البيانات للوحة التحكم"""
    print_header("📈 اختبار جاهزية البيانات للوحة التحكم")
    
    try:
        worksheet = get_google_sheets_client()
        data = worksheet.get_all_records()
        
        # تصفية البيانات
        real_data = [row for row in data if row.get("التاريخ") != "التاريخ" and row.get("المنتج")]
        
        if not real_data:
            print("  ⚠️ لا توجد بيانات")
            return False
        
        df = pd.DataFrame(real_data)
        df["الكمية"] = pd.to_numeric(df["الكمية"], errors="coerce").fillna(0)
        df["إجمالي المبيعات"] = pd.to_numeric(df["إجمالي المبيعات"], errors="coerce").fillna(0)
        
        # تجميع حسب المنتج
        grouped = df.groupby("المنتج").agg({
            "الكمية": "sum",
            "إجمالي المبيعات": "sum"
        }).reset_index()
        
        print("\n  📊 البيانات المجمعة للرسوم البيانية:")
        for _, row in grouped.iterrows():
            print(f"     • {row['المنتج']}: {int(row['الكمية'])} كوب - {row['إجمالي المبيعات']:.0f} ريال")
        
        # أفضل منتج مبيعاً
        best_product = grouped.loc[grouped["إجمالي المبيعات"].idxmax()]
        print(f"\n  🏆 أفضل منتج مبيعاً: {best_product['المنتج']} ({best_product['إجمالي المبيعات']:.0f} ريال)")
        
        return True
        
    except Exception as e:
        print(f"  ❌ خطأ: {e}")
        return False

def cleanup_test_data():
    """تنظيف البيانات الاختبارية"""
    print_header("🧹 تنظيف البيانات الاختبارية")
    
    try:
        worksheet = get_google_sheets_client()
        data = worksheet.get_all_records()
        
        current_date = datetime.now().strftime("%Y-%m-%d")
        test_products = ["فلات وايت", "سبنش لاتيه", "إسبريسو", "كابتشينو", "قهوة مقطرة V60", "كورتادو"]
        
        # البحث عن البيانات الاختبارية وحذفها
        rows_to_delete = []
        for i, row in enumerate(data):
            if row.get("التاريخ") == current_date and row.get("المنتج") in test_products:
                rows_to_delete.append(i + 1)  # الصفوف تبدأ من 1
        
        # حذف من الأسفل للأعلى
        for row_num in sorted(rows_to_delete, reverse=True):
            worksheet.delete_rows(row_num)
        
        print(f"  ✅ تم حذف {len(rows_to_delete)} سجل اختباري")
        return True
        
    except Exception as e:
        print(f"  ❌ خطأ: {e}")
        return False

def run_full_test():
    """تشغيل الاختبار الشامل"""
    print("\n" + "="*70)
    print("  🚀 الاختبار الشامل لنظام كاشير المقهى")
    print("  📅 التاريخ:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("  🌐 وضع التخزين:", "Google Sheets" if USE_GOOGLE_SHEETS else "Excel محلي")
    print("="*70)
    
    results = {}
    
    # 1. إضافة منتجات
    results["إضافة منتجات"] = test_add_products()
    
    # 2. قراءة وتحليل
    results["قراءة وتحليل"] = test_read_and_analyze()
    
    # 3. تحديث منتج
    results["تحديث منتج"] = test_update_existing()
    
    # 4. محاكاة فاتورة
    results["محاكاة فاتورة"] = test_invoice_simulation()
    
    # 5. جاهزية لوحة التحكم
    results["جاهزية لوحة التحكم"] = test_dashboard_data()
    
    # 6. تنظيف
    results["تنظيف البيانات"] = cleanup_test_data()
    
    # النتيجة النهائية
    print_header("📊 التقرير النهائي")
    
    all_passed = True
    for test_name, passed in results.items():
        status = "✅ نجح" if passed else "❌ فشل"
        print(f"  {test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "="*70)
    if all_passed:
        print("  🎉🎉 جميع الاختبارات نجحت! النظام جاهز للاستخدام! 🎉🎉")
    else:
        print("  ⚠️ بعض الاختبارات فشلت. يرجى مراجعة الأخطاء.")
    print("="*70 + "\n")
    
    return all_passed

if __name__ == "__main__":
    run_full_test()
