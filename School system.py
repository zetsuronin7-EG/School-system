import streamlit as st
import pandas as pd
from datetime import datetime

# إعدادات الصفحة الأساسية وتغيير المظهر للداكن تلقائياً ليناسب طلبك
st.set_page_config(
    page_title="نظام إدارة مدرسة التوكل جيلا",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 1. تهيئة قاعدة البيانات في الذاكرة (Session State) للحفاظ على البيانات أثناء التنقل
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    
    # بيانات المدير الافتراضية الثابتة
    st.session_state.manager_data = {
        "الاسم": "الأستاذ محمد محمود (مدير المدرسة)",
        "الرقم القومي": "2700101XXXXXXX",
        "رقم التليفون": "010XXXXXXXX",
        "الكود": "DIR-001",
        "المؤهل الدراسي": "ماجستير إدارة تعليمية - 2015"
    }
    
    # قاعدة بيانات المستخدمين (تسجيل الدخول والصلاحيات)
    st.session_state.users = {
        "admin": {"password": "admin123", "role": "admin", "name": "المدير العام", "active": True}
    }
    
    # قاعدة بيانات المدرسين (البيانات الشخصية والمالية)
    st.session_state.teachers = {}
    
    # قاعدة بيانات الطلاب
    st.session_state.students = {}
    
    # سجل الحضور والغياب اليومي (مفاتيح السجل تكون بصيغة التاريخ)
    st.session_state.attendance_records = {}

# --- دالة تسجيل الدخول ---
def login_page():
    st.markdown("<h2 style='text-align: center; color: #FF4B4B;'>🏫 نظام إدارة مدرسة التوكل جيلا المتكامل</h2>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center;'>تسجيل الدخول للنظام</h4>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("اسم المستخدم", placeholder="ادخل اسم المستخدم هنا...")
            password = st.text_input("كلمة المرور", type="password", placeholder="ادخل كلمة المرور هنا...")
            submit_login = st.form_submit_button("دخول")
            
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
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    login_page()
else:
    # --- القائمة الجانبية للتنقل والصلاحيات ---
    st.sidebar.markdown(f"### 👤 مرحباً: {st.session_state.user_display_name}")
    st.sidebar.markdown(f"**الصلاحية:** {'مدير النظام' if st.session_state.role == 'admin' else 'معلم'}")
    
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.session_state.username = None
        st.rerun()
        
    st.sidebar.divider()
    
    # تحديد خيارات القائمة بناء على الصلاحية
    if st.session_state.role == "admin":
        menu = ["🏠 لوحة التحكم العامة", "👨‍🎓 إدارة الطلاب والغياب", "👨‍🏫 إدارة المدرسين والحسابات", "🔐 إدارة حسابات المعلمين", "⚙️ إعدادات المدير"]
    else:
        menu = ["🏠 لوحة التحكم العامة", "📝 تسجيل غياب وحضور الطلاب"]
        
    choice = st.sidebar.radio("الانتقال إلى:", menu)

    # ==================== 1. لوحة التحكم العامة ====================
    if choice == "🏠 لوحة التحكم العامة":
        st.markdown("<h1 style='text-align: center;'>📊 لوحة التحكم والإحصائيات العامة</h1>", unsafe_allow_html=True)
        st.divider()
        
        c1, c2, c3 = st.columns(3)
        c1.metric("إجمالي الطلاب المسجلين", len(st.session_state.students))
        c2.metric("إجمالي المعلمين", len(st.session_state.teachers))
        
        # حساب غياب اليوم بشكل افتراضي تقريبي
        today_str = datetime.today().strftime('%Y-%m-%d')
        today_att = st.session_state.attendance_records.get(today_str, {})
        absent_count = sum(1 for status in today_att.values() if status.get('الحالة') == 'غائب')
        c3.metric("غياب الطلاب اليوم", absent_count)
        
        st.info("💡 نصيحة ذكية: يمكنك التنقل بين الواجهات المختلفة باستخدام القائمة الجانبية على اليسار.")

    # ==================== 2. إدارة الطلاب والغياب (خاص بالمدير) ====================
    elif choice == "👨‍🎓 إدارة الطلاب والغياب" and st.session_state.role == "admin":
        st.title("👨‍🎓 إدارة شؤون الطلاب والملفات الشخصية")
        
        tab1, tab2, tab3 = st.tabs(["➕ إضافة طالب جديد", "📂 ملفات الطلاب والجزاءات", "📝 تسجيل غياب وحضور اليوم"])
        
        with tab1:
            st.subheader("إضافة طالب جديد في المنظومة")
            with st.form("add_student_form"):
                s_name = st.text_input("اسم الطالب بالكامل")
                s_code = st.text_input("كود الطالب (رقم فريد)")
                s_national_id = st.text_input("الرقم القومي للطالب")
                s_phones = st.text_input("أرقام تليفون الطالب (يمكن كتابة أكثر من رقم وفصلهم بفاصلة)")
                p_phones = st.text_input("أرقام تليفون ولي الأمر (يمكن كتابة أكثر من رقم وفصلهم بفاصلة)")
                father_job = st.text_input("مهنة الأب")
                
                submit_s = st.form_submit_button("حفظ بيانات الطالب")
                if submit_s:
                    if s_name and s_code:
                        if s_code in st.session_state.students:
                            st.error("❌ كود الطالب هذا مسجل مسبقاً طالما هو فريد!")
                        else:
                            st.session_state.students[s_code] = {
                                "الاسم": s_name,
                                "الرقم القومي": s_national_id,
                                "رقم تليفون الطالب": s_phones,
                                "رقم تليفون ولي الأمر": p_phones,
                                "مهنة الأب": father_job,
                                "الجزاءات": [],
                                "الملاحظات": "لا يوجد ملاحظات",
                                "أيام الحضور": 0,
                                "أيام الغياب": 0,
                                "أيام التأخير": 0
                            }
                            st.success(f"✅ تم إضافة الطالب {s_name} بنجاح إلى النظام.")
                    else:
                        st.error("❌ يرجى ملء حقول الاسم والكود على الأقل.")
                        
        with tab2:
            st.subheader("🔎 البحث واستعراض الملف الشخصي الشامل للطالب")
            if not st.session_state.students:
                st.warning("⚠️ لا يوجد طلاب مسجلين في النظام حتى الآن.")
            else:
                s_select = st.selectbox("اختر الطالب لعرض ملفه بالكامل:", list(st.session_state.students.keys()), format_func=lambda x: st.session_state.students[x]["الاسم"])
                st.divider()
                
                s_info = st.session_state.students[s_select]
                
                col_s1, col_s2 = st.columns(2)
                with col_s1:
                    st.markdown(f"**🔹 الاسم:** {s_info['الاسم']}")
                    st.markdown(f"**🔹 كود الطالب:** {s_select}")
                    st.markdown(f"**🔹 الرقم القومي:** {s_info['الالرقم القومي'] if 'الالرقم القومي' in s_info else s_info.get('الرقم القومي', '')}")
                    st.markdown(f"**🔹 مهنة الأب:** {s_info['مهنة الأب']}")
                with col_s2:
                    st.markdown(f"**🔹 هاتف الطالب:** {s_info['رقم تليفون الطالب']}")
                    st.markdown(f"**🔹 هاتف ولي الأمر:** {s_info['رقم تليفون ولي الأمر']}")
                    st.markdown(f"**📊 إحصائيات الحضور والغياب المجمعة لهذا الطالب:**")
                    st.write(f"حضور: {s_info['أيام الحضور']} يوم | غياب: {s_info['أيام الغياب']} يوم | تأخير: {s_info['أيام التأخير']} يوم")
                
                st.divider()
                st.subheader("⚖️ إدخال وإدارة الجزاءات السلوكية والملاحظات")
                with st.form("sanction_form"):
                    new_sanction = st.text_input("أضف جزاء أو عقوبة جديدة")
                    new_note = st.text_area("تحديث الملاحظات التعليمية والسلوكية العامة للطالب", value=s_info['الملاحظات'])
                    submit_sanction = st.form_submit_button("تحديث ملف الطالب")
                    
                    if submit_sanction:
                        if new_sanction:
                            st.session_state.students[s_select]["الجزاءات"].append(f"⏱️ {datetime.today().strftime('%Y-%m-%d')}: {new_sanction}")
                        st.session_state.students[s_select]["الملاحظات"] = new_note
                        st.success("✅ تم تحديث ملف الطالب والجزاءات بنجاح.")
                        st.rerun()
                        
                st.markdown("**📋 السجل الحالي للجزاءات المدرجة في الملف:**")
                if s_info["الجزاءات"]:
                    for j in s_info["الجزاءات"]:
                        st.error(j)
                else:
                    st.info("🕊️ ملف الطالب خالٍ من الجزاءات العقابية حتى الآن.")

        with tab3:
            st.subheader("📝 تسجيل الحضور والغياب اليومي السريع (لوحة المدير)")
            if not st.session_state.students:
                st.warning("⚠️ لا يوجد طلاب لتسجيل حضورهم.")
            else:
                date_input = st.date_input("اختر تاريخ اليوم المراد رصده:", datetime.today())
                date_str = date_input.strftime('%Y-%m-%d')
                
                if date_str not in st.session_state.attendance_records:
                    st.session_state.attendance_records[date_str] = {}
                    
