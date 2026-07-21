"""اختبار شامل لاتصال Google Sheets وعمليات القراءة والكتابة"""

from google_sheets_config import get_google_sheets_client
from datetime import datetime
import json

def test_read_data():
    """اختبار قراءة البيانات"""
    print("\n" + "="*60)
    print("اختبار قراءة البيانات من Google Sheets")
    print("="*60)
    
    try:
        worksheet = get_google_sheets_client()
        data = worksheet.get_all_records()
        
        print(f"\nتم قراءة {len(data)} سجل بنجاح!")
        
        if data:
            print("\nآخر 5 سجلات:")
            for i, row in enumerate(data[-5:], 1):
                print(f"\nالسجل {i}:")
                for key, value in row.items():
                    print(f"  {key}: {value}")
        else:
            print("\nالورقة فارغة - لا توجد بيانات")
        
        return True, data
        
    except Exception as e:
        print(f"\nخطأ في القراءة: {e}")
        return False, []

def test_write_data():
    """اختبار كتابة بيانات جديدة"""
    print("\n" + "="*60)
    print("اختبار كتابة بيانات جديدة")
    print("="*60)
    
    try:
        worksheet = get_google_sheets_client()
        
        # بيانات اختبارية
        test_date = datetime.now().strftime("%Y-%m-%d")
        test_product = "منتج اختبار - كابتشينو"
        test_qty = 2
        test_total = 34.0
        test_rating = 4.8
        
        # إضافة صف جديد
        new_row = [test_date, test_product, test_qty, test_total, test_rating]
        worksheet.append_row(new_row)
        
        print(f"\nتم إضافة سجل اختباري بنجاح!")
        print(f"  التاريخ: {test_date}")
        print(f"  المنتج: {test_product}")
        print(f"  الكمية: {test_qty}")
        print(f"  الإجمالي: {test_total} ريال")
        print(f"  التقييم: {test_rating}")
        
        return True
        
    except Exception as e:
        print(f"\nخطأ في الكتابة: {e}")
        return False

def test_delete_test_data():
    """حذف البيانات الاختبارية"""
    print("\n" + "="*60)
    print("تنظيف البيانات الاختبارية")
    print("="*60)
    
    try:
        worksheet = get_google_sheets_client()
        data = worksheet.get_all_records()
        
        # البحث عن البيانات الاختبارية
        test_product = "منتج اختبار - كابتشينو"
        found = False
        
        for i, row in enumerate(data):
            if row.get("المنتج") == test_product:
                found = True
                # حذف الصف (الصفوف تبدأ من 2 لأن الصف 1 هو العناوين)
                worksheet.delete_rows(i + 2)
                print(f"\nتم حذف السجل الاختباري")
                break
        
        if not found:
            print("\nلم يتم العثور على بيانات اختبارية")
        
        return True
        
    except Exception as e:
        print(f"\nخطأ في الحذف: {e}")
        return False

def test_update_data():
    """اختبار تحديث البيانات"""
    print("\n" + "="*60)
    print("اختبار تحديث البيانات")
    print("="*60)
    
    try:
        worksheet = get_google_sheets_client()
        data = worksheet.get_all_records()
        
        if data:
            # تحديث آخر صف (زيادة الكمية)
            last_row_idx = len(data)
            last_row = data[-1]
            
            # تحديث القيم
            updated_qty = int(last_row.get("الكمية", 0)) + 1
            updated_total = float(last_row.get("إجمالي المبيعات", 0)) + 15
            
            # تحديث الخلايا (العمود C = الكمية، العمود D = الإجمالي)
            worksheet.update_cell(last_row_idx + 1, 3, updated_qty)
            worksheet.update_cell(last_row_idx + 1, 4, updated_total)
            
            print(f"\nتم تحديث السجل الأخير:")
            print(f"  المنتج: {last_row.get('المنتج')}")
            print(f"  الكمية الجديدة: {updated_qty}")
            print(f"  الإجمالي الجديد: {updated_total}")
            
            return True
        else:
            print("\nلا توجد بيانات للتحديث")
            return False
        
    except Exception as e:
        print(f"\nخطأ في التحديث: {e}")
        return False

def run_all_tests():
    """تشغيل جميع الاختبارات"""
    print("\n" + "="*60)
    print("بدء الاختبار الشامل لنظام Google Sheets")
    print("="*60)
    
    results = {
        "القراءة": False,
        "الكتابة": False,
        "التحديث": False,
        "الحذف": False
    }
    
    # اختبار القراءة
    results["القراءة"], data = test_read_data()
    
    # اختبار الكتابة
    results["الكتابة"] = test_write_data()
    
    # إعادة قراءة للتأكد من الكتابة
    if results["الكتابة"]:
        print("\nإعادة قراءة للتأكد من الكتابة...")
        success, new_data = test_read_data()
        if success and len(new_data) > len(data):
            print("✅ تم التأكد من حفظ البيانات الجديدة!")
    
    # اختبار التحديث
    results["التحديث"] = test_update_data()
    
    # حذف البيانات الاختبارية
    results["الحذف"] = test_delete_test_data()
    
    # النتيجة النهائية
    print("\n" + "="*60)
    print("تقرير النتائج النهائي")
    print("="*60)
    
    all_passed = True
    for test_name, passed in results.items():
        status = "نجح" if passed else "فشل"
        print(f"  {test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "="*60)
    if all_passed:
        print("جميع الاختبارات نجحت! النظام يعمل بشكل صحيح.")
    else:
        print("بعض الاختبارات فشلت. يرجى مراجعة الأخطاء أعلاه.")
    print("="*60)
    
    return all_passed

if __name__ == "__main__":
    run_all_tests()
