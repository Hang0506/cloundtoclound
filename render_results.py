def render_migration_sections(st, sections):
    title_map = [
        ("📌 Tổng Quan & Chiến Lược Migration", sections["overview"]),
        ("🪜 Các Bước Migration Chi Tiết", sections["steps"]),
        ("⏳ Tính Toán Thời Gian Truyền Tải", sections["time_estimation"]),
        ("🔐 Bảo Mật & Tuân Thủ", sections["security"]),
        ("✅ Xác Minh & Kiểm Tra Dữ Liệu", sections["validation"]),
        ("🚀 Gợi Ý Cải Tiến Tương Lai", sections["improvement"])
    ]
    for title, content in title_map:
        st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
        st.markdown(f'''
        <div style="max-height: 500px; overflow-y: auto; padding: 15px; border: 1px solid #ccc; background-color: #fefefe; font-size: 15px; line-height: 1.6;">
        {content}
        </div>
        ''', unsafe_allow_html=True)

def render_download_button(st, sections):
    full_plan = "\n\n".join([f"### {title}\n{content}" for title, content in sections.items()])
    st.download_button(
        label="📥 Tải xuống bản kế hoạch tổng hợp (.txt)",
        data=full_plan,
        file_name="SkyBridge_AI_Migration_FullPlan.txt",
        mime="text/plain",
        help="Tải về toàn bộ kế hoạch migration dưới dạng file văn bản. (aria-label: Download full migration plan as text file)",
        key="download_full_plan"
    ) 