import streamlit as st
import plotly.express as px
import pandas as pd
import datetime

def render_dashboard(df):
    # 1. تنسيقات الـ CSS للمظهر العام والكروت
    st.markdown("""
        <style>
            .dashboard-header {
                background: linear-gradient(135deg, #7F5539 0%, #4E3526 100%);
                color: white;
                padding: 30px;
                border-radius: 20px;
                margin-bottom: 30px;
                margin-left: 5px;
                margin-right: 5px;
                text-align: center;
                box-shadow: 0 8px 30px rgba(127, 85, 57, 0.2);
            }
            .dashboard-title {
                color: white; 
                font-weight: 800; 
                font-size: 2.2rem;
                margin-bottom: 10px;
                text-shadow: 0 2px 4px rgba(0,0,0,0.2);
            }
            .dashboard-subtitle {
                color: #EDE0D4;
                font-size: 1.1rem;
                opacity: 0.9;
            }
            .kpi-container {
                display: flex;
                gap: 25px;
                margin-bottom: 40px;
                margin-left: 5px;
                margin-right: 5px;
            }
            .custom-kpi-card {
                background: linear-gradient(135deg, #FFFFFF 0%, #FDFAF7 100%);
                padding: 25px;
                border-radius: 18px;
                border-left: 5px solid #7F5539;
                box-shadow: 0 8px 25px rgba(127, 85, 57, 0.08);
                flex: 1;
                text-align: center;
                transition: all 0.3s ease;
                position: relative;
                overflow: hidden;
                margin-left: 2px;
                margin-right: 2px;
            }
            .custom-kpi-card::before {
                content: '';
                position: absolute;
                top: 0;
                right: 0;
                width: 100%;
                height: 4px;
                background: linear-gradient(90deg, #7F5539 0%, #B08968 100%);
            }
            .custom-kpi-card:hover {
                transform: translateY(-8px);
                box-shadow: 0 15px 35px rgba(127, 85, 57, 0.15);
            }
            .kpi-label {
                color: #B08968;
                font-size: 1rem;
                margin-bottom: 12px;
                font-weight: 600;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 10px;
            }
            .kpi-val {
                color: #4E3526;
                font-size: 2.2rem;
                font-weight: 800;
                margin: 15px 0;
                text-shadow: 0 2px 4px rgba(0,0,0,0.05);
            }
            .kpi-unit {
                color: #7F5539;
                font-size: 1rem;
                font-weight: 600;
                margin-top: 5px;
            }
            .section-title {
                color: #4E3526;
                font-weight: 700;
                font-size: 1.4rem;
                margin-top: 35px;
                margin-bottom: 20px;
                margin-left: 5px;
                margin-right: 5px;
                padding-bottom: 10px;
                border-bottom: 2px solid #EDE0D4;
            }
            .chart-container {
                background: linear-gradient(135deg, #FFFFFF 0%, #FDFAF7 100%);
                padding: 25px;
                border-radius: 18px;
                border: 1px solid #E6CCB2;
                box-shadow: 0 6px 20px rgba(127, 85, 57, 0.06);
                margin-bottom: 25px;
                margin-left: 5px;
                margin-right: 5px;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('''
        <div class="dashboard-header">
            <h1 class="dashboard-title">📊 لوحة التحكم والأداء المالي</h1>
            <p class="dashboard-subtitle">تحليل شامل للمبيعات والأداء المالي للمقهى</p>
        </div>
    ''', unsafe_allow_html=True)
    
    if not df.empty:
        # تحويل الأعمدة إلى الأنواع الصحيحة
        if "التاريخ" in df.columns:
            try:
                df["التاريخ"] = pd.to_datetime(df["التاريخ"], errors='coerce')
            except:
                pass
        
        # تحويل عمود التقييم إلى أرقام
        if "التقييم" in df.columns:
            try:
                df["التقييم"] = pd.to_numeric(df["التقييم"], errors='coerce').fillna(0)
            except:
                df["التقييم"] = 0
        
        # تحويل الأعمدة الرقمية
        for col in ["إجمالي المبيعات", "الكمية"]:
            if col in df.columns:
                try:
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
                except:
                    df[col] = 0

        # عرض فلاتر التصفية
        col_filter1, col_filter2 = st.columns(2)
        
        with col_filter1:
            all_products = list(df["المنتج"].dropna().unique())
            if not all_products:
                all_products = []
            selected_products = st.multiselect(
                "🛒 تصفية حسب المنتج:", 
                options=all_products, 
                default=all_products,
                help="اختر المنتجات المراد عرض بياناتها"
            )
        
        with col_filter2:
            today = datetime.date.today()
            default_start = today - datetime.timedelta(days=30)
            
            start_date = st.date_input(
                "📅 من تاريخ:",
                value=default_start,
                max_value=today,
                help="تاريخ بداية الفترة"
            )
            
            end_date = st.date_input(
                "📅 إلى تاريخ:",
                value=today,
                max_value=today,
                help="تاريخ نهاية الفترة"
            )
        
        # تطبيق فلتر المنتجات المحددة
        if selected_products:
            df_filtered = df[df["المنتج"].isin(selected_products)]
        else:
            df_filtered = df.copy()
        
        # تطبيق فلتر التاريخ
        try:
            start_dt = pd.Timestamp(start_date)
            end_dt = pd.Timestamp(end_date) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)
            
            if "التاريخ" in df_filtered.columns:
                df_filtered = df_filtered[
                    (df_filtered["التاريخ"] >= start_dt) & 
                    (df_filtered["التاريخ"] <= end_dt)
                ]
        except Exception as e:
            st.warning(f"⚠️ تعذر تطبيق فلتر التاريخ: {e}")

        # حساب المؤشرات المالية
        try:
            total_sales = float(df_filtered["إجمالي المبيعات"].sum()) if "إجمالي المبيعات" in df_filtered.columns else 0
            total_orders = int(df_filtered["الكمية"].sum()) if "الكمية" in df_filtered.columns else 0
            avg_rating = float(df_filtered["التقييم"].mean()) if "التقييم" in df_filtered.columns and not df_filtered.empty else 0
        except Exception as e:
            st.error(f"❌ خطأ في حساب المؤشرات: {e}")
            total_sales = 0
            total_orders = 0
            avg_rating = 0

        # عرض الكروت العلوية
        st.markdown(f'''
            <div class="kpi-container">
                <div class="custom-kpi-card" style="border-left-color: #7F5539;">
                    <div class="kpi-label">💰 إجمالي المبيعات النقدية</div>
                    <div class="kpi-val">{total_sales:,.0f}</div>
                    <div class="kpi-unit">ريال</div>
                </div>
                <div class="custom-kpi-card" style="border-left-color: #B08968;">
                    <div class="kpi-label">☕ الأكواب المبيعة</div>
                    <div class="kpi-val">{total_orders}</div>
                    <div class="kpi-unit">كوب</div>
                </div>
                <div class="custom-kpi-card" style="border-left-color: #DDB892;">
                    <div class="kpi-label">⭐ تقييم الجودة العام</div>
                    <div class="kpi-val">{avg_rating:.1f}</div>
                    <div class="kpi-unit">/ 5</div>
                </div>
            </div>
        ''', unsafe_allow_html=True)

        st.markdown('<h3 class="section-title">📈 تحليلات المبيعات وتوزيع الحصص</h3>', unsafe_allow_html=True)
        
        # تجهيز البيانات للرسوم البيانية
        try:
            df_grouped = df_filtered.groupby("المنتج").agg({"إجمالي المبيعات": "sum", "الكمية": "sum"}).reset_index()
        except Exception as e:
            df_grouped = pd.DataFrame(columns=["المنتج", "إجمالي المبيعات", "الكمية"])

        if not df_grouped.empty:
            # 3 أعمدة متجاورة للرسوم البيانية
            col_chart1, col_chart2, col_chart3 = st.columns(3)

            # العمود الأول: مخطط الأعمدة (إيرادات المنتجات)
            with col_chart1:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<p style="font-weight:bold; color:#7F5539; margin-bottom: 15px; font-size: 1.1rem; text-align: center;">💵 إيرادات المنتجات</p>', unsafe_allow_html=True)
                
                fig_bar = px.bar(
                    df_grouped, x="المنتج", y="إجمالي المبيعات", 
                    color="إجمالي المبيعات",
                    color_continuous_scale=["#EDE0D4", "#B08968", "#7F5539"],
                    text="إجمالي المبيعات"
                )
                fig_bar.update_traces(
                    texttemplate='%{text:.0f} ريال', 
                    textposition='outside',
                    marker_line_color='#4E3526',
                    marker_line_width=1
                )
                fig_bar.update_layout(
                    plot_bgcolor="rgba(0,0,0,0)", 
                    paper_bgcolor="rgba(0,0,0,0)", 
                    font_color="#4E3526",
                    coloraxis_showscale=False, 
                    height=320, 
                    margin=dict(t=20, b=20, l=20, r=20),
                    xaxis_title=None, 
                    yaxis_title=None,
                    xaxis=dict(tickangle=-45, tickfont=dict(size=10)),
                    yaxis=dict(gridcolor='#EDE0D4', gridwidth=1)
                )
                st.plotly_chart(fig_bar, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

            # العمود الثاني: المخطط الدائري (توزيع حصص الأكواب)
            with col_chart2:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<p style="font-weight:bold; color:#7F5539; margin-bottom: 15px; font-size: 1.1rem; text-align: center;">📊 توزيع الحصص</p>', unsafe_allow_html=True)
                
                fig_pie = px.pie(
                    df_grouped, names="المنتج", values="الكمية",
                    hole=0.4,
                    color_discrete_sequence=["#4E3526", "#7F5539", "#B08968", "#DDB892", "#EDE0D4", "#F5E9DC"]
                )
                fig_pie.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", 
                    font_color="#4E3526", 
                    height=320,
                    margin=dict(t=20, b=20, l=20, r=20),
                    legend=dict(
                        orientation="h", 
                        yanchor="bottom", 
                        y=-0.3, 
                        xanchor="center", 
                        x=0.5,
                        font=dict(size=10)
                    )
                )
                fig_pie.update_traces(
                    textinfo='percent',
                    textfont=dict(size=10),
                    marker=dict(line=dict(color='#FFFFFF', width=1))
                )
                st.plotly_chart(fig_pie, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

            # العمود الثالث: المخطط الخطي (اتجاهات المبيعات اليومية)
            with col_chart3:
                try:
                    if "التاريخ" in df_filtered.columns and "إجمالي المبيعات" in df_filtered.columns:
                        df_daily = df_filtered.groupby("التاريخ").agg({"إجمالي المبيعات": "sum"}).reset_index()
                        df_daily = df_daily.sort_values("التاريخ")
                        
                        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                        st.markdown('<p style="font-weight:bold; color:#7F5539; margin-bottom: 15px; font-size: 1.1rem; text-align: center;">📈 اتجاهات المبيعات</p>', unsafe_allow_html=True)
                        
                        fig_line = px.line(
                            df_daily, x="التاريخ", y="إجمالي المبيعات",
                            markers=True,
                            line_shape="spline",
                            color_discrete_sequence=["#7F5539"]
                        )
                        fig_line.update_traces(
                            line=dict(width=2),
                            marker=dict(size=6, color="#4E3526")
                        )
                        fig_line.update_layout(
                            plot_bgcolor="rgba(0,0,0,0)",
                            paper_bgcolor="rgba(0,0,0,0)",
                            font_color="#4E3526",
                            height=320,
                            margin=dict(t=20, b=20, l=20, r=20),
                            xaxis_title="التاريخ",
                            yaxis_title="المبيعات (ريال)",
                            xaxis=dict(gridcolor='#EDE0D4', gridwidth=1, tickfont=dict(size=10)),
                            yaxis=dict(gridcolor='#EDE0D4', gridwidth=1, tickfont=dict(size=10))
                        )
                        st.plotly_chart(fig_line, use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                        st.markdown('<p style="font-weight:bold; color:#7F5539; margin-bottom: 15px; font-size: 1.1rem; text-align: center;">📈 اتجاهات المبيعات</p>', unsafe_allow_html=True)
                        st.info("⚠️ لا توجد بيانات كافية لعرض مخطط اتجاهات المبيعات")
                        st.markdown('</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    st.markdown('<p style="font-weight:bold; color:#7F5539; margin-bottom: 15px; font-size: 1.1rem; text-align: center;">📈 اتجاهات المبيعات</p>', unsafe_allow_html=True)
                    st.info("⚠️ لا توجد بيانات كافية لعرض مخطط اتجاهات المبيعات")
                    st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("⚠️ لا توجد بيانات مبيعات متوفرة للمنتجات أو الفترة الزمنية المحددة.")
        
        # الجدول السفلي
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<h3 class="section-title">📋 سجل الحركات المسجلة (المفلترة)</h3>', unsafe_allow_html=True)
        
        if not df_filtered.empty:
            # تنسيق التاريخ للعرض
            display_df = df_filtered.copy()
            if "التاريخ" in display_df.columns:
                display_df["التاريخ"] = display_df["التاريخ"].dt.strftime("%Y-%m-%d")
            
            # تنسيق الأرقام
            if "إجمالي المبيعات" in display_df.columns:
                display_df["إجمالي المبيعات"] = display_df["إجمالي المبيعات"].apply(lambda x: f"{x:,.0f} ريال")
            
            st.dataframe(
                display_df, 
                use_container_width=True,
                height=400,
                column_config={
                    "التاريخ": st.column_config.TextColumn("التاريخ", width="medium"),
                    "المنتج": st.column_config.TextColumn("المنتج", width="large"),
                    "الكمية": st.column_config.NumberColumn("الكمية", width="small"),
                    "إجمالي المبيعات": st.column_config.TextColumn("الإجمالي", width="medium"),
                    "التقييم": st.column_config.NumberColumn("التقييم", width="small", format="%.1f")
                }
            )
            
            # أزرار التصدير
            st.markdown('<div style="background: linear-gradient(135deg, #F8F5F0 0%, #F5F0E9 100%); padding: 20px; border-radius: 15px; border: 1px solid #E6CCB2; margin-top: 20px;">', unsafe_allow_html=True)
            st.markdown('<p style="color:#4E3526; font-weight:600; margin-bottom: 15px;">📤 تصدير البيانات</p>', unsafe_allow_html=True)
            
            col_export1, col_export2 = st.columns(2)
            
            with col_export1:
                csv_data = df_filtered.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="📊 تصدير كملف CSV",
                    data=csv_data,
                    file_name=f"cafe_report_{datetime.date.today()}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col_export2:
                import io
                buffer = io.BytesIO()
                df_filtered.to_excel(buffer, index=False)
                st.download_button(
                    label="📥 تصدير كملف Excel",
                    data=buffer.getvalue(),
                    file_name=f"cafe_report_{datetime.date.today()}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("⚠️ لا توجد بيانات لعرضها بعد التصفية")
    else:
        st.markdown('''
            <div style="background: linear-gradient(135deg, #F8F5F0 0%, #F5F0E9 100%); 
                     padding: 40px; 
                     border-radius: 20px; 
                     border: 2px dashed #DDB892; 
                     text-align: center;
                     margin-top: 30px;">
                <h3 style="color:#7F5539; margin-bottom: 15px;">📭 سجل المبيعات فارغ حالياً</h3>
                <p style="color:#B08968;">ابدأ ببيع المنتجات من تبويب "المنيو والبيع" لرؤية البيانات هنا</p>
            </div>
        ''', unsafe_allow_html=True)