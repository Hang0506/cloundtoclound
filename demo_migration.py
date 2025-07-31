import streamlit as st
from migration_utils import create_demo_data, build_json_for_ai, build_system_info, show_demo_migration

st.set_page_config(
    page_title="Demo Migration JSON",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 Demo: Cloud-to-Cloud Migration JSON")

# Tab để chọn chế độ
tab1, tab2 = st.tabs(["📊 Demo Data", "🤖 JSON Processing"])

with tab1:
    st.markdown("## 📊 Demo Data Overview")
    
    demo_data, json_output = show_demo_migration()

with tab2:
    st.markdown("## 🤖 JSON Processing Demo")
    
    # Tạo demo data
    demo_data = create_demo_data()
    
    # Hiển thị JSON được xử lý
    st.markdown("### JSON Output cho AI:")
    json_output = build_json_for_ai(demo_data)
    st.code(json_output, language="json")
    
    # Hiển thị thông tin được xử lý
    st.markdown("### System Info được tạo:")
    system_info = build_system_info(demo_data)
    st.text_area("System Information", system_info, height=400)
    
    # Hiển thị các trường được xử lý
    st.markdown("### Các trường được xử lý:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Mapping tự động:**")
        st.markdown("- Downtime: '30 phút' → 30 minutes")
        st.markdown("- Change Rate: 'Trung bình' → 'Medium'")
        st.markdown("- Network: 'VPN' → 'VPN'")
        st.markdown("- Partitioning: 'Có phân vùng' → true")
        st.markdown("- Boolean: 'Có' → true, 'Không' → false")
    
    with col2:
        st.markdown("**Logic thông minh:**")
        st.markdown("- Critical Level: High (zero downtime + HA)")
        st.markdown("- Security Policies: AES256 + IAM (detected)")
        st.markdown("- External Integrations: Parsed from text")
        st.markdown("- Source/Target Services: Extracted")
    
    # Hiển thị JSON parsed
    st.markdown("### JSON Parsed Fields:")
    import json
    parsed_json = json.loads(json_output)
    
    for key, value in parsed_json.items():
        if isinstance(value, list):
            st.markdown(f"**{key}:** {', '.join(map(str, value))}")
        elif isinstance(value, bool):
            st.markdown(f"**{key}:** {'✅' if value else '❌'}")
        else:
            st.markdown(f"**{key}:** {value}")

st.markdown("---")
st.markdown("### 📝 Ghi chú:")
st.markdown("- Demo này sử dụng dữ liệu mẫu từ một dự án migration thực tế")
st.markdown("- JSON output được chuẩn hóa để AI có thể xử lý dễ dàng")
st.markdown("- Tất cả các trường được mapping tự động từ text sang format phù hợp")
st.markdown("- Critical level được tính toán dựa trên các yếu tố quan trọng") 