import streamlit as st
from migration_utils import collect_user_input, create_demo_data, build_json_for_ai, build_system_info

st.set_page_config(
    page_title="Demo Fill Data",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 Demo: Fill Data vào Form")

# Toggle để bật/tắt demo mode
use_demo = st.sidebar.checkbox("📊 Sử dụng Demo Data", value=True)

if use_demo:
    st.sidebar.success("✅ Demo mode đã bật")
    st.sidebar.markdown("**Demo data sẽ được tự động fill vào form**")
else:
    st.sidebar.info("ℹ️ Demo mode đã tắt")
    st.sidebar.markdown("**Form sẽ trống để nhập thủ công**")

# Hiển thị demo data nếu bật demo
if use_demo:
    demo_data = create_demo_data()
    
    st.markdown("### 📊 Demo Data Preview:")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Thông tin cơ bản:**")
        st.markdown(f"- Migration Type: {demo_data['migration_type']}")
        st.markdown(f"- Cloud Source: {demo_data['cloud_source']}")
        st.markdown(f"- Cloud Target: {demo_data['cloud_target']}")
        st.markdown(f"- Database: {demo_data['db_type']}")
        st.markdown(f"- Data Size: {demo_data['data_size_gb']} GB")
    
    with col2:
        st.markdown("**Thông tin chi tiết:**")
        st.markdown(f"- Data Type: {demo_data['data_type']}")
        st.markdown(f"- Change Rate: {demo_data['change_rate']}")
        st.markdown(f"- Network: {demo_data['network_connection']}")
        st.markdown(f"- Zero Downtime: {demo_data['zero_downtime_required']}")

# Gọi hàm collect_user_input với demo mode
st.markdown("---")
st.markdown("### 📝 Form Migration (với Demo Data):")

user_input = collect_user_input(use_demo=use_demo)

# Hiển thị kết quả nếu submit
if user_input.get('submit'):
    st.markdown("### ✅ Kết quả:")
    
    # Hiển thị system info
    system_info = build_system_info(user_input)
    st.text_area("System Information", system_info, height=300)
    
    # Hiển thị JSON
    if user_input.get('migration_type') == "Cloud ➜ Cloud":
        json_output = build_json_for_ai(user_input)
        st.markdown("### 🤖 JSON Output:")
        st.code(json_output, language="json")
    
    # Hiển thị các trường đã nhập
    st.markdown("### 📋 Các trường đã nhập:")
    for key, value in user_input.items():
        if key != 'submit' and value is not None:
            st.markdown(f"**{key}:** {value}")

st.markdown("---")
st.markdown("### 📝 Hướng dẫn:")
st.markdown("1. **Bật Demo Mode** để tự động fill data vào form")
st.markdown("2. **Tắt Demo Mode** để nhập thủ công")
st.markdown("3. **Submit form** để xem kết quả")
st.markdown("4. **JSON output** sẽ được tạo cho AI xử lý") 