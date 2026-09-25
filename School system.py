import streamlit as st
import pandas as pd
from datetime import datetime

# إعدادات الصفحة الأساسية
st.set_page_config(
    page_title="نظام مدرسة التوكل جيلا",
    page_icon="🏫",
    layout="wide"
)

# --- حقن كود CSS لقلب الواجهة بالكامل من اليمين إلى اليسار (RTL) ---
st.markdown("""
    <style>
    /* قلب اتجاه الصفحة بالكامل */
    .main .block-container {
        direction: RTL;
        text-align: right;
    }
    /* قلب اتجاه القائمة الجانبية */
    [data-testid="stSidebar"] {
        direction: RTL;
        text-align: right;
    }
    /* ضبط محاذاة النصوص والعناصر */
    div.stButton > button {
        width: 100%;
    }
    .stRadio > div {
        flex-direction: row-reverse;
        justify-content: flex-end;
    }
    h1, h2, h3, h4, h5, h6, p, span, label {
        text-align: right !important;
        direction: RTL !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- تهيئة قاعدة البيانات وضخ بيانات افتراضية لمنع الشاشات الفارغة ---
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.logged_in = False
    st.session_state.role = None
    
    # بيانات المدير الافتراضية
    st.session_state.manager_data = {
        "الاسم": "الأستاذ محمد محمود (مدير المدرسة)",
        "الرقم القومي": "2700101XXXXXXX",
        "رقم التليفون": "010XXXXXXXX",
        "الكود": "DIR-001",
        "المؤهل الدراسي": "ماجستير إدارة تعليمية - 2015"
    }
    
    # حسابات تسجيل الدخول الجاهزة
    st.session_state.users = {
        "admin": {"password": "admin123", "role": "admin", "name": "المدير العام", "active": True},
        "teacher1": {"password": "123", "role": "teacher", "name": "أ/ أحمد علي (مدرس تجريبي)", "active": True}
    }
    
    # بيانات مدرسين افتراضية عشان الصفحة متظهرش سوداء وفارغة
    st.session_state.teachers = {
        "TCH-01": {
            "الاسم": "أحمد علي محمد",
            "الالرقم القومي": "2850302XXXXXXX",
            "رقم التليفون": "012XXXXXXXX",
            "المؤهل الدراسي": "بكالوريوس هندسة - 2010",
            "عدد الحصص": 12,
            "ثمن الحصة": 150,
            "إجمالي الحصص في الأسبوع": 1800,
            "إجمالي الحصص في الشهر": 7200
        }
    }
    
    # بيانات طلاب افتراضية
    st.session_state.students = {
        "STD-101": {
            "الاسم": "محمود كريم عبد الله",
            "الرقم القومي": "3080504XXXXXXX",
            "رقم تليفون الطالب": "015XXXXXXXX",
            "رقم تليفون ولي الأمر": "011XXXXXXXX",
            "مهنة الأب": "مهندس حر",
            "الجزاءات": ["⏱️ تم التنبيه عليه شفهياً للتأخر"],
            "الملاحظات": "طالب متفوق في التدريب العملي بالمصنع",
            "أيام الحضور": 15,
            "أيام الغياب": 1,
            "أيام التأخير": 2
        }
    }
    
    st.session_state.attendance_records = {}

# --- دالة شاشة تسجيل الدخول ---
def login_page():
    st.markdown("<h2 style='text-align: center; color: #FF4B4B;'>🏫 نظام إدارة مدرسة التوكل جيلا المتكامل</h2>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center;'>تسجيل الدخول للنظام</h4>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("اسم المستخدم", placeholder="ادخل اسم المستخدم هنا...")
            password = st.text_input("كلمة المرور", type="password", placeholder="ادخل كلمة المرور هنا...")
            submit_login = st.form_submit_button("دخول للنظام")
            
            if submit_login:
                if username in st.session_state.users:
                    user_info = st.session_state.users[username]
                    if not user_info["active"]:
                        st.error("❌ عذراً، هذا الحساب معطل حالياً من قِبل الإدارة.")
                    elif user_info["password"] == password:
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.role = user_info["role"]
                        st.session_state.user_display_name = user_info["name"]
                        st.success(f"👋 أهلاً بك يا {user_info['name']}")
                        st.rerun()
                    else:
                        st.error("❌ كلمة المرور غير صحيحة.")
                else:
                    st.error("❌ اسم المستخدم غير موجود.")

# التحقق من حالة تسجيل الدخول
if not st.session_state.logged_in:
    login_page()
else:
    # القائمة الجانبية (أصبحت يمين الآن)
    st.sidebar.markdown(f"### 👤 {st.session_state.user_display_name}")
    st.sidebar.markdown(f"**الصلاحية:** {'مدير النظام' if st.session_state.role == 'admin' else 'معلم ورصد غياب'}")
    
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.session_state.username = None
        st.rerun()
        
    st.sidebar.divider()
    
    if st.session_state.role == "admin":
        menu = ["🏠 لوحة التحكم العامة", "👨‍🎓 إدارة الطلاب والغياب", "👨‍🏫 إدارة المدرسين والحسابات", "🔐 إدارة حسابات المعلمين", "⚙️ إعدادات المدير"]
    else:
        menu = ["🏠 لوحة التحكم العامة", "📝 تسجيل غياب وحضور الطلاب"]
        
    choice = st.sidebar.radio("الانتقال إلى صفحات النظام:", menu)

    # ==================== 1. لوحة التحكم العامة ====================
    if choice == "🏠 لوحة التحكم العامة":
        st.markdown("<h2 style='text-align: right;'>📊 لوحة التحكم والإحصائيات العامة</h2>", unsafe_allow_html=True)
        st.divider()
        
        c1, c2, c3 = st.columns(3)
        c1.metric("إجمالي الطلاب بالمنظومة", len(st.session_state.students))
        c2.metric("إجمالي المعلمين المسجلين", len(st.session_state.teachers))
        c3.metric("الحسابات النشطة الآن", len(st.session_state.users))
        
        st.success("✨ تم قلب اتجاه البرنامج بالكامل ليصبح لغة عربية من اليمين إلى اليسار بنجاح!")

    # ==================== 2. إدارة الطلاب والغياب ====================
    elif choice == "👨‍🎓 إدارة الطلاب والغياب" and st.session_state.role == "admin":
        st.title("👨‍🎓 إدارة شؤون الطلاب والملفات الشخصية")
        
        tab1, tab2, tab3 = st.tabs(["➕ إضافة طالب جديد", "📂 ملفات الطلاب والجزاءات", "📝 تسجيل غياب وحضور اليوم"])
        
        with tab1:
            with st.form("add_student_form"):
                s_name = st.text_input("اسم الطالب بالكامل")
                s_code = st.text_input("كود الطالب")
                s_national_id = st.text_input("الرقم القومي للطالب")
                s_phones = st.text_input("أرقام تليفون الطالب")
                p_phones = st.text_input("أرقام تليفون ولي الأمر")
                father_job = st.text_input("مهنة الأب")
                if st.form_submit_button("حفظ بيانات الطالب"):
                    if s_name and s_code:
                        st.session_state.students[s_code] = {
                            "الاسم": s_name, "الرقم القومي": s_national_id, "رقم تليفون الطالب": s_phones,
                            "رقم تليفون ولي الأمر": p_phones, "مهنة الأب": father_job, "الجزاءات": [],
                            "الملاحظات": "لا يوجد ملاحظات", "أيام الحضور": 0, "أيام الغياب": 0, "أيام التأخير": 0
                        }
                        st.success(f"✅ تم إضافة الطالب {s_name}")
                        st.rerun()
                        
        with tab2:
            s_select = st.selectbox("اختر الطالب لاستعراض ملفه الشامل وملاحظاته:", list(st.session_state.students.keys()), format_func=lambda x: st.session_state.students[x]["الاسم"])
            s_info = st.session_state.students[s_select]
            
            col_s1, col_s2 = st.columns(2)
            with col_s1:
                st.write(f"**🔹 الاسم:** {s_info['الاسم']}")
                st.write(f"**🔹 كود الطالب:** {s_select}")
                st.write(f"**🔹 مهنة الأب:** {s_info['مهنة الأب']}")
            with col_s2:
                st.write(f"**🔹 هاتف ولي الأمر:** {s_info['رقم تليفون ولي الأمر']}")
                st.write(f"**📊 سجل الحضور:** حضور {s_info['أيام الحضور']} | غياب {s_info['أيام الغياب']}")
                
            st.divider()
            with st.form("add_jaza_form"):
                new_j = st.text_input("إضافة جزاء جديد للملف")
                if st.form_submit_button("تحديث ملف الطالب وإضافة الجزاء"):
                    if new_j:
                        st.session_state.students[s_select]["الجزاءات"].append(new_j)
                        st.success("تم تحديث الجزاءات")
                        st.rerun()
            st.write("**⚠️ الجزاءات الحالية:**", s_info["الجزاءات"])

        with tab3:
            st.write("دفتر الغياب والحضور السريع للطلاب")
            for s_id, s_data in st.session_state.students.items():
                st.write(f"👤 {s_data['الاسم']} ({s_id})")
                st.radio("الحالة", ["حاضر", "غائب", "متأخر"], key=f"adm_at_{s_id}", horizontal=True)

    # ==================== 3. تسجيل الغياب (واجهة المدرس) ====================
    elif choice == "📝 تسجيل غياب وحضور الطلاب":
        st.title("📝 دفتر رصد غياب وحضور الطلاب اليومي")
        for s_id, s_data in st.session_state.students.items():
            st.write(f"👤 {s_data['الاسم']}")
            st.radio("رصد الحالة اليومية:", ["حاضر", "غائب", "متأخر"], key=f"tch_at_{s_id}", horizontal=True)

    # ==================== 4. إدارة المدرسين والحسابات ====================
    elif choice == "👨‍🏫 إدارة المدرسين والحسابات" and st.session_state.role == "admin":
        st.title("👨‍🏫 إدارة شؤون المعلمين والحسابات المالية")
        
        tab_t1, tab_t2 = st.tabs(["➕ إضافة معلم جديد", "💰 كشف الرواتب والحساب المالي"])
        
        with tab_t1:
            with st.form("add_teacher_form"):
                t_name = st.text_input("اسم المدرس بالكامل")
                t_code = st.text_input("كود المعلم")
                t_qual = st.text_input("المؤهل الدراسي وسنة التخرج")
                t_lessons = st.number_input("عدد الحصص في الأسبوع", min_value=1, value=10)
