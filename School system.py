import streamlit as st
import pandas as pd
from datetime import datetime

# إعداد الصفحة وتفعيل الاتجاه العربي الرسمي من إعدادات المنصة
st.set_page_config(
    page_title="نظام مدرسة التوكل جيلا",
    page_icon="🏫",
    layout="wide"
)

# فرض التنسيق من اليمين إلى اليسار (RTL) على عناصر الواجهة والقائمة الجانبية
st.markdown("""
    <style>
    [data-testid="stSidebar"], .main .block-container, div.stButton, .stTabs, label, span, p, h1, h2, h3 {
        direction: RTL !important;
        text-align: right !important;
    }
    div.stRadio > div {
        flex-direction: row-reverse !important;
        justify-content: flex-end !important;
    }
    </style>
""", unsafe_allow_html=True)

# تهيئة البيانات الأساسية والافتراضية لمنع ظهور الصفحات فارغة
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = None
    st.session_state.current_page = "🏠 لوحة التحكم العامة"
    
    st.session_state.manager_data = {
        "الاسم": "الأستاذ محمد محمود (مدير المدرسة)",
        "الرقم القومي": "2700101XXXXXXX",
        "رقم التليفون": "010XXXXXXXX",
        "الكود": "DIR-001",
        "المؤهل الدراسي": "ماجستير إدارة تعليمية"
    }
    
    st.session_state.users = {
        "admin": {"password": "admin123", "role": "admin", "name": "المدير العام", "active": True},
        "teacher1": {"password": "123", "role": "teacher", "name": "أ/ أحمد علي (مدرس تجريبي)", "active": True}
    }
    
    st.session_state.teachers = {
        "TCH-01": {"الاسم": "أحمد علي محمد", "الرقم القومي": "2850302XXXXXXX", "رقم التليفون": "012XXXXXXXX", "المؤهل الدراسي": "بكالوريوس هندسة", "عدد الحصص": 12, "ثمن الحصة": 150, "إجمالي الحصص في الأسبوع": 1800, "إجمالي الحصص في الشهر": 7200}
    }
    
    st.session_state.students = {
        "STD-101": {"الاسم": "محمود كريم عبد الله", "الرقم القومي": "3080504XXXXXXX", "رقم تليفون الطالب": "015XXXXXXXX", "رقم تليفون ولي الأمر": "011XXXXXXXX", "مهنة الأب": "مهندس حر", "الجزاءات": ["⏱️ تنبيه شفهي للتأخر"], "الملاحظات": "طالب متفوق", "أيام الحضور": 15, "أيام الغياب": 1, "أيام التأخير": 2}
    }

# شاشة تسجيل الدخول
if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align: center; color: #FF4B4B;'>🏫 نظام مدرسة التوكل جيلا المتكامل</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            user = st.text_input("اسم المستخدم")
            pwd = st.text_input("كلمة المرور", type="password")
            if st.form_submit_button("تسجيل الدخول"):
                if user in st.session_state.users:
                    u_info = st.session_state.users[user]
                    if not u_info["active"]:
                        st.error("❌ هذا الحساب معطل حالياً.")
                    elif u_info["password"] == pwd:
                        st.session_state.logged_in = True
                        st.session_state.username = user
                        st.session_state.role = u_info["role"]
                        st.session_state.user_display_name = u_info["name"]
                        st.rerun()
                    else: st.error("❌ كلمة المرور خاطئة")
                else: st.error("❌ المستخدم غير موجود")
else:
    # القائمة الجانبية المحدثة
    st.sidebar.markdown(f"### 👤 {st.session_state.user_display_name}")
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.logged_in = False
        st.rerun()
        
    st.sidebar.divider()
    
    # تحديد القوائم بناءً على الصلاحية
    if st.session_state.role == "admin":
        menu = ["🏠 لوحة التحكم العامة", "👨‍🎓 إدارة الطلاب والغياب", "👨‍🏫 إدارة المدرسين والحسابات", "🔐 إدارة حسابات المعلمين", "⚙️ إعدادات المدير"]
    else:
        menu = ["🏠 لوحة التحكم العامة", "📝 تسجيل غياب وحضور الطلاب"]
        
    st.session_state.current_page = st.sidebar.radio("الانتقال إلى:", menu)

    # 1. لوحة التحكم العامة
    if st.session_state.current_page == "🏠 لوحة التحكم العامة":
        st.title("📊 الإحصائيات العامة للمدرسة")
        c1, c2, c3 = st.columns(3)
        c1.metric("إجمالي الطلاب", len(st.session_state.students))
        c2.metric("إجمالي المعلمين", len(st.session_state.teachers))
        c3.metric("الحسابات النشطة", len(st.session_state.users))

    # 2. إدارة الطلاب
    elif st.session_state.current_page == "👨‍🎓 إدارة الطلاب والغياب":
        st.title("👨‍🎓 إدارة شؤون الطلاب")
        t1, t2 = st.tabs(["📂 ملفات الطلاب", "➕ إضافة طالب"])
        with t1:
            s_select = st.selectbox("اختر الطالب:", list(st.session_state.students.keys()), format_func=lambda x: st.session_state.students[x]["الاسم"])
            s = st.session_state.students[s_select]
            st.write(f"**الاسم:** {s['الاسم']} | **الهاتف:** {s['رقم تليفون الطالب']}")
            st.write(f"**حضور:** {s['أيام الحضور']} يوم | **غياب:** {s['أيام الغياب']} يوم")
            st.write("**الجزاءات الحالية:**", s["الجزاءات"])
        with t2:
            with st.form("add_s"):
                name = st.text_input("اسم الطالب")
                code = st.text_input("كode الطالب")
                if st.form_submit_button("حفظ"):
                    st.session_state.students[code] = {"الاسم": name, "الجزاءات": [], "أيام الحضور": 0, "أيام الغياب": 0, "أيام التأخير": 0, "رقم تليفون الطالب": "غير مسجل"}
                    st.success("تم الحفظ")
                    st.rerun()

    # 3. إدارة المدرسين
    elif st.session_state.current_page == "👨‍🏫 إدارة المدرسين والحسابات":
        st.title("👨‍🏫 الحسابات المالية للمدرسين")
        if st.session_state.teachers:
            df = pd.DataFrame.from_dict(st.session_state.teachers, orient='index')
            st.dataframe(df[["الاسم", "عدد الحصص", "ثمن الحصة", "إجمالي الحصص في الأسبوع", "إجمالي الحصص في الشهر"]])
        
        with st.form("add_t"):
            t_name = st.text_input("اسم المدرس")
            t_code = st.text_input("كود المدرس")
            t_lessons = st.number_input("الحصص أسبوعياً", value=10)
            t_price = st.number_input("ثمن الحصة", value=100)
            if st.form_submit_button("إضافة معلم"):
                st.session_state.teachers[t_code] = {"الاسم": t_name, "عدد الحصص": t_lessons, "ثمن الحصة": t_price, "إجمالي الحصص في الأسبوع": t_lessons*t_price, "إجمالي الحصص في الشهر": t_lessons*t_price*4}
                st.success("تمت الإضافة")
                st.rerun()

    # 4. حسابات المعلمين
    elif st.session_state.current_page == "🔐 إدارة حسابات المعلمين":
        st.title("🔐 إدارة صلاحيات وحسابات الدخول")
        for username, data in list(st.session_state.users.items()):
            if data["role"] != "admin":
                st.write(f"👤 {data['name']} (`{username}`) - الحالة: {'نشط' if data['active'] else 'معطل'}")
                if st.button(f"تغيير حالة الحساب لـ {username}", key=f"btn_{username}"):
                    st.session_state.users[username]["active"] = not st.session_state.users[username]["active"]
                    st.rerun()

    # 5. إعدادات المدير
    elif st.session_state.current_page == "⚙️ إعدادات المدير":
        st.title("⚙️ بيانات مدير المدرسة")
        st.write(f"**الاسم الحالي:** {st.session_state.manager_data['الاسم']}")
        st.write(f"**الكود:** {st.session_state.manager_data['الكود']}")
