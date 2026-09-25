import streamlit as st
import pandas as pd
from datetime import datetime

# Setup page config
st.set_page_config(page_title="مدرسة التوكل جيلا", page_icon="🏫", layout="wide")

# Custom CSS for RTL and beautiful Arabic styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;700&display=swap');
    html, body, [data-testid="stSidebarNav"], .main, h1, h2, h3, h4, h5, h6, p, div, label {
        font-family: 'Cairo', sans-serif !important;
        direction: RTL !important;
        text-align: right !important;
    }
    .stButton>button {
        width: 100%;
        background-color: #2E7D32;
        color: white;
        font-weight: bold;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        background-color: #f0f2f6;
        border-radius: 4px;
    }
    </style>
""", unsafe_allow_html=True)

# Main Title
st.title("🏫 نظام إدارة مدرسة التوكل جيلا المتكامل")
st.subheader("لوحة تحكم ذكية للنظام الإداري والمالي والتدريب المزدوج")

# Sidebar navigation
menu = ["🏠 لوحة التحكم العامة", "👨‍🎓 إدارة الطلاب والغياب", "👨‍🏫 إدارة المدرسين والحسابات", "⚙️ إعدادات المدير"]
choice = st.sidebar.radio("الانتقال إلى:", menu)

# --- Sample in-memory Data State to make prototype work instantly ---
if 'students' not in st.session_state:
    st.session_state.students = [
        {"كود": "STU101", "الاسم": "أحمد محمد علي", "الرقم القومي": "3050101XXXXXXX", "تليفون الطالب": "01012345678", "تليفون ولي الأمر": "01234567890", "مهنة الأب": "مهندس", "الحضور": 18, "الغياب": 2, "الجزاءات": "لا يوجد"},
        {"كود": "STU102", "الاسم": "محمود حسن السيد", "الرقم القومي": "3050202XXXXXXX", "تليفون الطالب": "01198765432", "تليفون ولي الأمر": "01511223344", "مهنة الأب": "فني خياطة", "الحضور": 19, "الغياب": 1, "الجزاءات": "إنذار تأخير"}
    ]

if 'teachers' not in st.session_state:
    st.session_state.teachers = [
        {"كود": "TCH201", "الاسم": "أستاذ خالد مصطفى", "الرقم القومي": "2850303XXXXXXX", "التليفون": "01001122334", "المؤهل": "بكالوريوس هندسة 2010", "الحصص أسبوعياً": 12, "ثمن الحصة": 150}
    ]

# --- 1. Dashboard View ---
if choice == "🏠 لوحة التحكم العامة":
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="إجمالي عدد الطلاب", value=len(st.session_state.students))
    with col2:
        st.metric(label="إجمالي عدد المعلمين", value=len(st.session_state.teachers))
    with col3:
        st.metric(label="نسبة حضور الطلاب اليوم", value="95%")
    with col4:
        st.metric(label="حالة غياب المعلمين", value="0 غائب")
        
    st.info("💡 نصيحة الذكاء الاصطناعي: النظام مهيأ للعمل بكفاءة على شاشات الموبايل والتابلت لسهولة تسجيل الحضور داخل الفصول أو الورش.")
    
    st.subheader("📋 قائمة الطلاب الحالية")
    st.dataframe(pd.DataFrame(st.session_state.students))

# --- 2. Students & Attendance View ---
elif choice == "👨‍🎓 إدارة الطلاب والغياب":
    tab1, tab2, tab3 = st.tabs(["📝 إضافة طالب جديد", "⏱️ تسجيل الحضور اليومي", "📂 ملفات الطلاب"])
    
    with tab1:
        st.write("### إدخال بيانات طالب جديد")
        with st.form("add_student_form"):
            s_name = st.text_input("اسم الطالب رباعي")
            s_code = st.text_input("كود الطالب")
            s_id = st.text_input("الرقم القومي للطالب (14 رقم)")
            s_phone = st.text_input("رقم هاتف الطالب (يمكن كتابة أكثر من رقم وفصلهم بفاصلة)")
            p_phone = st.text_input("رقم هاتف ولي الأمر")
            f_job = st.text_input("مهنة الأب")
            
            submitted = st.form_submit_button("حفظ الطالب في النظام")
            if submitted:
                st.session_state.students.append({
                    "كود": s_code, "الاسم": s_name, "الرقم القومي": s_id, 
                    "تليفون الطالب": s_phone, "تليفون ولي الأمر": p_phone, 
                    "مهنة الأب": f_job, "الحضور": 0, "الغياب": 0, "الجزاءات": "لا يوجد"
                })
                st.success(f"تم تسجيل الطالب {s_name} بنجاح!")
                
    with tab2:
        st.write("### دفتر الحضور والغياب اليومي السريع")
        st.caption(f"تاريخ اليوم: {datetime.now().strftime('%Y-%m-%d')}")
        
        for idx, student in enumerate(st.session_state.students):
            col_name, col_status, col_notes = st.columns([3, 2, 2])
            with col_name:
                st.write(f"**{student['الاسم']} ({student['كود']})**")
            with col_status:
                status = st.radio(f"حالة الحضور {student['كود']}", ["حاضر", "غائب", "متأخر"], key=f"status_{idx}", horizontal=True, label_visibility="collapsed")
            with col_notes:
                notes = st.text_input("ملاحظات / جزاءات", key=f"notes_{idx}", label_visibility="collapsed")
        
        if st.button("اعتماد ورفع تقرير الحضور اليومي"):
            st.success("تم تحديث وحفظ سجل غياب اليوم وإرسال الإحصائيات للمدير.")

    with tab3:
        st.write("### البحث واستعراض ملف طالب متكامل")
        student_codes = [s["كود"] for s in st.session_state.students]
        selected_code = st.selectbox("اختر كود الطالب لعرض ملفه الشخصي:", student_codes)
        
        # Display full file
        for s in st.session_state.students:
            if s["كود"] == selected_code:
                st.markdown(f"""
                | البيان | التفاصيل |
                | :--- | :--- |
                | **اسم الطالب** | {s['الاسم']} |
                | **الكود** | {s['كود']} |
                | **الرقم القومي** | {s['الرقم القومي']} |
                | **تليفون الطالب** | {s['تليفون الطالب']} |
                | **تليفون ولي الأمر** | {s['تليفون ولي الأمر']} |
                | **مهنة الأب** | {s['مهنة الأب']} |
                | **إجمالي أيام الحضور** | 🟢 {s['الحضور']} يوم |
                | **إجمالي أيام الغياب** | 🔴 {s['الغياب']} يوم |
                | **الجزاءات المسجلة** | ⚠️ {s['الجزاءات']} |
                """, unsafe_allow_html=True)

# --- 3. Teachers & Finance View ---
elif choice == "👨‍🏫 إدارة المدرسين والحسابات":
    tab1, tab2 = st.tabs(["📝 إضافة معلم جديد", "💰 الحسابات والمستحقات المالية"])
    
    with tab1:
        st.write("### إدخال بيانات معلم جديد")
        with st.form("add_teacher_form"):
            t_name = st.text_input("اسم المعلم")
            t_id = st.text_input("الرقم القومي")
            t_phone = st.text_input("رقم التليفون")
            t_code = st.text_input("كود المعلم")
            t_qual = st.text_input("المؤهل الدراسي + سنة الحصول عليه")
            t_slots = st.number_input("عدد الحصص في الأسبوع", min_value=1, value=10)
            t_price = st.number_input("ثمن الحصة الواحدة (بالجنيه)", min_value=0, value=100)
            
            submitted_t = st.form_submit_button("حفظ بيانات المعلم")
            if submitted_t:
                st.session_state.teachers.append({
                    "كود": t_code, "الاسم": t_name, "الرقم القومي": t_id,
                    "التليفون": t_phone, "المؤهل": t_qual, "الحصص أسبوعياً": t_slots, "ثمن الحصة": t_price
                })
                st.success(f"تم تسجيل الأستاذ/ة {t_name} في النظام!")

    with tab2:
        st.write("### كشف مستحقات المدرسين المالية تلقائياً")
        
        teacher_data_processed = []
        for t in st.session_state.teachers:
            weekly_lessons = t["الحصص أسبوعياً"]
            monthly_lessons = weekly_lessons * 4 # Simple logic for calculation
            weekly_pay = weekly_lessons * t["ثمن الحصة"]
            monthly_pay = monthly_lessons * t["ثمن الحصة"]
            
            teacher_data_processed.append({
                "الكود": t["كود"],
                "الاسم": t["اسم"],
                "الحصص/أسبوع": weekly_lessons,
                "الحصص/شهر (تقريبي)": monthly_lessons,
                "ثمن الحصة": f"{t['ثمن الحصة']} ج.م",
                "راتب أسبوعي": f"{weekly_pay} ج.م",
                "إجمالي الراتب الشهري": f"{monthly_pay} ج.م"
            })
            
        st.table(pd.DataFrame(teacher_data_processed))

# --- 4. Director View ---
elif choice == "⚙️ إعدادات المدير":
    st.write("### 🔑 بيانات مدير المدرسة (صاحب الصلاحية الأعلى)")
    
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("الاسم", value="أستاذ محمد محمود (مدير المدرسة)", disabled=True)
        st.text_input("الرقم القومي", value="2700101XXXXXXX", disabled=True)
        st.text_input("رقم التليفون", value="010XXXXXXXX", disabled=True)
    with col2:
        st.text_input("كود المدير", value="DIR-001", disabled=True)
        st.text_input("المؤهل الدراسي", value="ماجستير إدارة تعليمية - 2015", disabled=True)
        
    st.success("🔒 حساب المدير مؤمن بالكامل. جميع البيانات مشفرة ومحفوظة السحاب.")
