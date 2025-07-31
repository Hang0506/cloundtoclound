import streamlit as st
from openai import OpenAI
from migration_utils import collect_user_input, build_system_info, build_prompts
from styles import inject_custom_css
from render_results import render_migration_sections, render_download_button

# Cấu hình giao diện
st.set_page_config(page_title="SkyBridge AI - Cloud & Multi-Cloud Migration Planner", layout="wide")

# Set API key từ secrets - with fallback for demo mode
try:
    client = OpenAI(api_key=st.secrets["openai_api_key"])
    DEMO_MODE = False
except:
    client = None
    DEMO_MODE = True
    st.markdown(
        '<div role="alert" aria-live="assertive" style="color: #842029; background: #f8d7da; padding: 8px; border-radius: 4px; font-weight:600;">⚠️ Demo Mode: Using sample migration plan (no OpenAI API key configured)</div>',
        unsafe_allow_html=True
    )

# Header
st.markdown(
    """
    <h1 class="big-title" tabindex="0">🌉 SkyBridge AI – Tư Vấn Chuyển Đổi CSDL Lên Cloud & Multi-Cloud</h1>
    <p class="sub-desc" tabindex="0">Trợ lý AI chuyên sâu giúp bạn thiết kế kế hoạch migration từ On-premise lên Cloud hoặc giữa các Cloud chỉ trong vài phút.</p>
    """,
    unsafe_allow_html=True
)

st.divider()

# 📥 Nhập thông tin
st.markdown(
    '<h2 class="section-title" tabindex="0">📥 Nhập thông tin hệ thống và loại migration:</h2>',
    unsafe_allow_html=True
)


# --- Main Logic: Use Refactored Functions ---
inject_custom_css(st)
user_input = collect_user_input()

if user_input["submit"]:
    system_info = build_system_info(user_input)
    prompts = build_prompts(system_info, migration_type=user_input["migration_type"])

    with st.spinner("🤖 Đang tạo các phần của kế hoạch migration..."):

        def call_openai(section_prompt):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": section_prompt}],
                    temperature=0.4,
                    max_tokens=2500
                )
                return response.choices[0].message.content
            except Exception as e:
                return f"❌ API Error: {str(e)}"

        sections = {}
        for key, prompt_text in prompts.items():
            # Debug: Hiển thị prompt_text trước khi gọi OpenAI
            st.write(f"🔍 Debug - Prompt cho {key}:")
            st.code(prompt_text, language="text")
            st.write("---")
            
            #sections[key] = call_openai(prompt_text)

        st.success("✅ Đã tạo xong kế hoạch migration")
        render_migration_sections(st, sections)
        render_download_button(st, sections)
