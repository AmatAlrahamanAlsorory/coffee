import streamlit as st
import pandas as pd

def render_cashier(df_products, save_invoice_fn):
    st.markdown('''
        <div style="background: linear-gradient(135deg, #7F5539 0%, #4E3526 100%); 
                 color: white; 
                 padding: 25px; 
                 border-radius: 20px; 
                 margin-bottom: 30px;
                 text-align: center;
                 box-shadow: 0 8px 30px rgba(127, 85, 57, 0.2);">
            <h1 style="color: white; font-size: 2rem; font-weight: 800; margin-bottom: 10px;">☕ شاشة البيع المباشر (الكاشير)</h1>
            <p style="color: #EDE0D4; font-size: 1.1rem;">نظام نقاط البيع المتكامل للمقهى</p>
        </div>
    ''', unsafe_allow_html=True)
    
    col_menu, col_invoice = st.columns([2.6, 1])
    
    # 1. تعريف الصور
    IMAGE_DEFAULT = "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=600&q=80"
    product_images = {
        "فلات وايت": "https://images.unsplash.com/photo-1577968897966-3d4325b36b61?w=600&q=80",
        "سبنش لاتيه": "https://images.unsplash.com/photo-1517701604599-bb29b565090c?w=600&q=80",
        "قهوة مقطرة V60": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=600&q=80",
        "V60 قهوة مقطرة": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=600&q=80",
        "كورتادو": "https://images.unsplash.com/photo-1534778101976-62847782c213?w=600&q=80",
        "إسبراسو": "https://images.unsplash.com/photo-1510591509382-74346262656e?w=600&q=80",
        "إسبريسو": "https://images.unsplash.com/photo-1510591509382-74346262656e?w=600&q=80",
        "كابتشينو": "https://images.unsplash.com/photo-1534778101976-62847782c213?w=600&q=80",
        "موكا": "https://images.unsplash.com/photo-1572442388796-11668a67e53d?w=600&q=80",
        "كاراميل لاتيه": "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=600&q=80",
        "آمريكانو": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=600&q=80"
    }

    # 2. جلب المنتجات ديناميكياً من بيانات المنتجات
    # التحقق من وجود بيانات
    if df_products.empty or "name" not in df_products.columns:
        st.warning("⚠️ لا توجد منتجات في القائمة. أضف منتجات من تبويب 'إدارة المنتجات'")
        return
    
    # جلب المنتجات الفريدة مع إزالة القيم الفارغة
    unique_products = df_products["name"].dropna().unique()
    
    if len(unique_products) == 0:
        st.warning("⚠️ لا توجد منتجات في القائمة. أضف منتجات من تبويب 'إضافة منتج'")
        return
    
    with col_menu:
        st.markdown('''
            <div style="background: linear-gradient(135deg, #F8F5F0 0%, #F5F0E9 100%); 
                     padding: 20px; 
                     border-radius: 18px; 
                     border: 1px solid #E6CCB2;
                     margin-bottom: 25px;">
                <h3 style="color:#4E3526; font-weight:700; margin-bottom:20px; text-align:center;">📋 قائمة المنيو المصورة</h3>
                <p style="color:#B08968; text-align:center; margin-bottom:20px;">انقر على "إضافة للطلب" لإضافة المنتج إلى الفاتورة</p>
            </div>
        ''', unsafe_allow_html=True)
        
        num_cols = 3
        sub_cols = st.columns(num_cols)
        
        for i, item in enumerate(unique_products):
            # جلب السعر من بيانات المنتجات
            prod_df = df_products[df_products["name"] == item]
            if not prod_df.empty:
                try:
                    price = int(prod_df.iloc[0]["price"])
                except (ValueError, TypeError, KeyError):
                    price = 15
            else:
                price = 15
            
            img_url = product_images.get(item, IMAGE_DEFAULT)
            
            with sub_cols[i % num_cols]:
                st.markdown(f'''
                    <div class="menu-card">
                        <img src="{img_url}" class="menu-img">
                        <div class="menu-content">
                            <div class="menu-title">{item}</div>
                            <div class="menu-price">{price} ريال</div>
                        </div>
                    </div>
                ''', unsafe_allow_html=True)
                
                if st.button(f"➕ إضافة للطلب", key=f"click_{item}_{i}"):
                    found = False
                    for idx, inv_item in enumerate(st.session_state.current_invoice):
                        if inv_item["المنتج"] == item:
                            st.session_state.current_invoice[idx]["الكمية"] += 1
                            st.session_state.current_invoice[idx]["الإجمالي"] += price
                            found = True
                            break
                    if not found:
                        st.session_state.current_invoice.append({"المنتج": item, "الكمية": 1, "السعر": price, "الإجمالي": price})
                    st.rerun()

    # 3. عرض الفاتورة
    with col_invoice:
        st.markdown('''
            <div style="background: linear-gradient(135deg, #F8F5F0 0%, #F5F0E9 100%); 
                     padding: 20px; 
                     border-radius: 18px; 
                     border: 1px solid #E6CCB2;
                     margin-bottom: 20px;">
                <h3 style="color:#4E3526; font-weight:700; margin-bottom:15px; text-align:center;">🧾 تفاصيل الفاتورة</h3>
            </div>
        ''', unsafe_allow_html=True)
        
        st.markdown('<div class="invoice-container"><div class="invoice-header">🧾 RECEIPT / فاتورة عميل</div>', unsafe_allow_html=True)
        
        if st.session_state.current_invoice:
            total_invoice_sum = 0
            
            st.markdown('''
                <div style="margin-bottom: 20px;">
                    <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #EDE0D4;">
                        <span style="font-weight: 600; color: #4E3526;">المنتج</span>
                        <span style="font-weight: 600; color: #4E3526;">الكمية</span>
                        <span style="font-weight: 600; color: #4E3526;">الإجمالي</span>
                    </div>
            ''', unsafe_allow_html=True)
            
            for item in st.session_state.current_invoice:
                st.markdown(f'''
                    <div style="display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px dashed #EDE0D4;">
                        <span style="color: #7F5539; font-weight: 600;">{item['المنتج']}</span>
                        <span style="color: #B08968;">× {item['الكمية']}</span>
                        <span style="color: #4E3526; font-weight: 600;">{item['الإجمالي']} ريال</span>
                    </div>
                ''', unsafe_allow_html=True)
                total_invoice_sum += item["الإجمالي"]
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown(f'''
                <div style="display: flex; justify-content: space-between; padding: 15px 0; margin-top: 10px; border-top: 2px solid #DDB892;">
                    <span style="font-weight: 700; color: #4E3526; font-size: 1.1rem;">المجموع الكلي:</span>
                    <span style="font-weight: 800; color: #7F5539; font-size: 1.2rem;">{total_invoice_sum} ريال</span>
                </div>
            ''', unsafe_allow_html=True)
            
            st.markdown(f'<div class="invoice-total">💰 المجموع النهائي: {total_invoice_sum} ريال</div></div><br>', unsafe_allow_html=True)
            
            # أزرار التحكم
            col_btn1, col_btn2 = st.columns(2)
            
            with col_btn1:
                if st.button("💾 ترحيل واعتماد البيع", use_container_width=True):
                    save_invoice_fn()
                    st.success("🎉 تم الحفظ بنجاح!")
                    st.rerun()
            
            with col_btn2:
                if st.button("🗑️ تفريغ السلة", key="clear_all", use_container_width=True):
                    st.session_state.current_invoice = []
                    st.rerun()
        else:
            st.markdown('''
                <div style="text-align: center; padding: 40px 20px;">
                    <div style="font-size: 3rem; color: #E6CCB2; margin-bottom: 15px;">🛒</div>
                    <p style="color: #B08968; font-size: 1.1rem; font-weight: 600;">السلة فارغة</p>
                    <p style="color: #A68A64; margin-top: 10px;">ابدأ بإضافة منتجات من القائمة</p>
                </div>
            ''', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)