def inject_custom_css(st):
    st.markdown("""
    <style>
    .big-title {
        font-size: 40px;
        font-weight: 800;
        color: #1a1a1a; /* Đen đậm, tốt cho contrast */
        margin-bottom: 10px;
        background: #fff;
    }
    .big-title:focus, .section-title:focus, .sub-desc:focus {
        outline: 2px solid #00529b;
        outline-offset: 2px;
    }
    .sub-desc {
        font-size: 18px;
        color: #222; /* Đậm hơn để dễ đọc */
        background: #fff;
    }
    .section-title {
        font-size: 22px;
        font-weight: 600;
        color: #00529b; /* Xanh đậm, contrast tốt */
        margin-top: 30px;
        background: #fff;
    }
    </style>
    """, unsafe_allow_html=True) 