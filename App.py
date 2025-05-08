# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import datetime

# إعداد الصفحة
st.set_page_config(
    page_title="فعاليات روح الرياض",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تحميل الخطوط وتنسيق الصفحة
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap" rel="stylesheet">
    <style>
        html, body, [class*="css"]  {
            direction: rtl;
            text-align: right;
            font-family: 'Tajawal', sans-serif !important;
        }
        .stApp {
            background-color: #fdf6f9;
        }
    </style>
""", unsafe_allow_html=True)

# تحويل التاريخ من عربي إلى datetime
def convert_arabic_date(date_str):
    months = {
        'يناير': 1, 'فبراير': 2, 'مارس': 3, 'أبريل': 4, 'ابريل': 4, 'مايو': 5, 'يونيو': 6,
        'يوليو': 7, 'أغسطس': 8, 'اغسطس': 8, 'سبتمبر': 9, 'أكتوبر': 10, 'اكتوبر': 10,
        'نوفمبر': 11, 'ديسمبر': 12
    }
    try:
        parts = date_str.strip().split()
        day = int(parts[0])
        month = months.get(parts[1], 1)
        year = int(parts[2])
        return datetime.date(year, month, day)
    except:
        return None

# تحميل البيانات
file_path = '/mnt/c/Users/shmot/Downloads/فعاليات_الرياض_مايو2025.xlsx'
df = pd.read_excel(file_path)

# تحويل عمود التاريخ
df['التاريخ'] = df['التاريخ'].apply(lambda x: convert_arabic_date(str(x)))

# إضافة فعاليات يدوية
extra_events = pd.DataFrame([
    {"اسم الفعالية": "ورشة خزف فنية", "النوع": "خزف", "الموقع": "حي السفارات", "التاريخ": datetime.date(2025, 5, 10), "السعر": "150 ريال", "الرابط": "https://example.com"},
    {"اسم الفعالية": "تجربة نحت في الطبيعة", "النوع": "نحت", "الموقع": "وادي حنيفة", "التاريخ": datetime.date(2025, 5, 18), "السعر": "200 ريال", "الرابط": "https://example.com"},
    {"اسم الفعالية": "ليلة كاريوكي", "النوع": "كاريوكي", "الموقع": "بوليفارد رياض سيتي", "التاريخ": datetime.date(2025, 5, 22), "السعر": "100 ريال", "الرابط": "https://example.com"},
])
df = pd.concat([df, extra_events], ignore_index=True)

# التحقق من الأعمدة الأساسية
required_cols = ['اسم الفعالية', 'النوع', 'الموقع', 'التاريخ', 'السعر', 'الرابط']
if not all(col in df.columns for col in required_cols):
    st.error("⚠️ الأعمدة المطلوبة غير مكتملة في الملف.")
    st.write(df.columns.tolist())
    st.stop()

# حذف الفعاليات التي بدون تاريخ
df = df.dropna(subset=['التاريخ'])

# ====== الشريط الجانبي ======
st.sidebar.markdown("🎯 **اختر تجربتك:**")

event_types = df['النوع'].dropna().unique().tolist()
selected_type = st.sidebar.selectbox('نوع الفعالية', ['كل الأنواع'] + event_types)

min_date = df['التاريخ'].min()
max_date = df['التاريخ'].max()

use_date_filter = st.sidebar.checkbox("🔍 تفعيل فلترة التاريخ")
selected_date = st.sidebar.date_input("📅 اختر التاريخ", min_value=min_date, max_value=max_date, value=min_date)

# ====== الفلترة ======
filtered_df = df.copy()

if use_date_filter:
    filtered_df = filtered_df[filtered_df['التاريخ'] == selected_date]

if selected_type != 'كل الأنواع':
    filtered_df = filtered_df[filtered_df['النوع'] == selected_type]

# ====== العنوان ======
st.markdown("""
    <div style='
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        text-align: center;
        background-color: #fff0f5;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        margin-bottom: 30px;
    '>
        <h1 style="color:#d1007f; margin-bottom: 10px;">روح الرياض 🎡</h1>
        <p style='font-size:20px; color:#444;'>لعرض الفعاليات المختلفة المقامة في مدينة الرياض لشهر مايو لعام 2025، لتمنحك تجربة ترفيهية لا تُنسى ✨</p>
    </div>
""", unsafe_allow_html=True)

# ====== عرض النتائج ======
if not filtered_df.empty:
    for _, row in filtered_df.iterrows():
        st.markdown(f"""
            <div style="background-color:#ffe0f0; padding:20px; margin-bottom:10px; border-radius:15px;">
                <h3 style="color:#b30059;">🎫 {row['اسم الفعالية']}</h3>
                <p>📍 <strong>الموقع:</strong> {row['الموقع']}</p>
                <p>🗓️ <strong>التاريخ:</strong> {row['التاريخ']}</p>
                <p>💰 <strong>السعر:</strong> {row['السعر']}</p>
                <p>🎭 <strong>النوع:</strong> {row['النوع']}</p>
                <a href="{row['الرابط']}" target="_blank" style="color:#fff; background-color:#d1007f; padding:10px 20px; border-radius:10px; text-decoration:none;">🔗 احجز أو اعرف أكثر</a>
            </div>
        """, unsafe_allow_html=True)
else:
    st.warning("🙁 لا توجد فعاليات تطابق الفلاتر المختارة.")
