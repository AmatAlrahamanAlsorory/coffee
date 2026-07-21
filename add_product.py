import streamlit as st
import pandas as pd
from datetime import datetime

def render_add_product(load_products_fn, load_sales_fn, save_invoice_fn):
    """صفحة إدارة المنتجات"""
    from config import COLORS, USE_GOOGLE_SHEETS
    
    st.markdown('''
        <div style="background: linear-gradient(135deg, #7F5539 0%, #4E3526 100%); color: white; padding: 25px; border-radius: 20px; margin-bottom: 30px; text-align: center; box-shadow: 0 8px 30px rgba(127, 85, 57, 0.2);">
            <h1 style="color: white; font-size: 2rem; font-weight: 800; margin-bottom: 10px;">إدارة المنتجات</h1>
            <p style="color: #EDE0D4; font-size: 1.1rem;">إضافة وتعديل منتجات قائمة المقهى</p>
        </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('''
    <div style="background: linear-gradient(135deg, #F8F5F0 0%, #F5F0E9 100%); padding: 20px; border-radius: 18px; border: 1px solid #E6CCB2; margin-bottom: 25px; box-shadow: 0 6px 20px rgba(127, 85, 57, 0.06);">
        <div style="display: flex; align-items: center; gap: 15px;">
            <div style="font-size: 1.5rem; color: #7F5539;">💡</div>
            <div>
                <p style="color: #4E3526; margin: 0; font-weight: 700; font-size: 1.1rem;">
                    إدارة منتجات القائمة
                </p>
                <p style="color: #B08968; margin: 5px 0 0 0;">
                    هذه الصفحة لإضافة منتجات جديدة للقائمة فقط. للبيع استخدم تبويب "المنيو والبيع"
                </p>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # تحميل بيانات المنتجات
    df_products = load_products_fn()
    
    # عرض المنتجات الموجودة حالياً
    if not df_products.empty:
        st.markdown(f'''
            <div style="background: linear-gradient(135deg, #F8F5F0 0%, #F5F0E9 100%); padding: 25px; border-radius: 18px; border: 1px solid #E6CCB2; margin-bottom: 30px; box-shadow: 0 6px 20px rgba(127, 85, 57, 0.06);">
                <h3 style="color: #4E3526; font-weight: 700; margin-bottom: 20px; text-align: center;">المنتجات الحالية في القائمة</h3>
                <div style="background: #7F5539; color: white; padding: 10px 20px; border-radius: 10px; display: inline-block; margin-bottom: 20px;">
                    <span style="font-weight: 600;">عدد المنتجات:</span> {len(df_products)}
                </div>
        ''', unsafe_allow_html=True)
        
        # عرض جدول المنتجات
        display_df = df_products.copy()
        if 'price' in display_df.columns:
            display_df['price'] = display_df['price'].apply(lambda x: f"{x:,.0f} ريال")
        if 'image' in display_df.columns:
            display_df = display_df.drop(columns=['image'])
        
        st.dataframe(
            display_df, 
            use_container_width=True, 
            hide_index=True,
            height=350,
            column_config={
                "name": st.column_config.TextColumn("اسم المنتج", width="large"),
                "price": st.column_config.TextColumn("السعر", width="medium"),
                "rating": st.column_config.NumberColumn("التقييم", width="small", format="%.1f"),
                "category": st.column_config.TextColumn("التصنيف", width="medium"),
                "description": st.column_config.TextColumn("الوصف", width="large")
            }
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('''
        <div style="height: 2px; background: linear-gradient(90deg, #7F5539 0%, #B08968 50%, #EDE0D4 100%); margin: 40px 0; border-radius: 2px;"></div>
    ''', unsafe_allow_html=True)
    
    # نموذج إضافة منتج جديد
    st.markdown('''
        <div class="product-form-container">
            <h3 style="color: #4E3526; font-weight: 700; margin-bottom: 25px; text-align: center;">إضافة منتج جديد للقائمة</h3>
    ''', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div style="margin-bottom: 20px;">', unsafe_allow_html=True)
        product_name = st.text_input(
            "اسم المنتج:", 
            placeholder="مثال: موكا، كاراميل لاتيه، آمريكانو",
            help="أدخل اسم المنتج الجديد"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div style="margin-bottom: 20px;">', unsafe_allow_html=True)
        product_price = st.number_input(
            "السعر (ريال):", 
            min_value=1, 
            max_value=500, 
            value=15,
            step=1,
            help="أدخل سعر المنتج بالريال السعودي"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # زر الحفظ
    col_btn = st.columns([1, 2, 1])
    with col_btn[1]:
        if st.button("حفظ المنتج الجديد", use_container_width=True):
            if not product_name or product_name.strip() == "":
                st.error("الرجاء إدخال اسم المنتج")
            elif product_price <= 0:
                st.error("السعر يجب أن يكون أكبر من صفر")
            else:
                product_name = product_name.strip()
                
                # التحقق من عدم وجود المنتج مسبقاً
                if not df_products.empty and 'name' in df_products.columns:
                    if product_name in df_products['name'].values:
                        st.warning(f"المنتج '{product_name}' موجود بالفعل في القائمة!")
                    else:
                        # إضافة المنتج الجديد
                        if add_new_product(product_name, product_price, load_products_fn):
                            st.success(f"تم إضافة '{product_name}' بسعر {product_price} ريال بنجاح!")
                            st.balloons()
                            try:
                                st.cache_data.clear()
                            except:
                                pass
                            st.rerun()
                        else:
                            st.error("حدث خطأ أثناء الحفظ")
                else:
                    # إضافة المنتج الجديد
                    if add_new_product(product_name, product_price, load_products_fn):
                        st.success(f"تم إضافة '{product_name}' بسعر {product_price} ريال بنجاح!")
                        st.balloons()
                        try:
                            st.cache_data.clear()
                        except:
                            pass
                        st.rerun()
                    else:
                        st.error("حدث خطأ أثناء الحفظ")


def add_new_product(product_name, price, load_products_fn):
    """إضافة منتج جديد إل�� صفحة المنتجات"""
    try:
        from config import USE_GOOGLE_SHEETS
        
        if USE_GOOGLE_SHEETS:
            from google_sheets_config import get_products_worksheet
            worksheet = get_products_worksheet()
            
            # إضافة المنتج الجديد إلى صفحة Menu مع جميع الأعمدة
            worksheet.append_row([
                product_name,
                float(price),
                4.5,  # تقييم افتراضي
                "مشروبات ساخنة",  # التصنيف
                "منتج جديد",  # الوصف
                "نعم"  # متاح
            ])
        else:
            # حفظ في Excel محلي
            from config import FILE_NAME
            import os
            
            # إنشاء ملف منتجات منفصل إذا لم يكن موجوداً
            products_file = os.path.join(os.path.dirname(FILE_NAME), "products.xlsx")
            
            if os.path.exists(products_file):
                df_products = pd.read_excel(products_file)
            else:
                df_products = pd.DataFrame(columns=["name", "price", "image", "category", "description"])
            
            new_product = pd.DataFrame([{
                "name": product_name,
                "price": float(price),
                "image": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=600&q=80",
                "category": "قهوة",
                "description": "منتج جديد",
                "rating": 4.5
            }])
            
            df_products = pd.concat([df_products, new_product], ignore_index=True)
            df_products.to_excel(products_file, index=False)
        
        return True
    except Exception as e:
        st.error(f"خطأ في الحفظ: {e}")
        return False