import streamlit as st

def render_sidebar():
    st.sidebar.header("📊 内部パラメータ")
    user_stress = st.sidebar.slider(
        "現在のストレス度", 
        0.0, 1.0, 0.3,
        help="高いほどリスク判定が厳しくなります"
    )

    st.sidebar.markdown("---")
    st.sidebar.write("### 状態解説")
    
    if user_stress > 0.7:
        st.sidebar.error("オーバーロード気味です。")
    elif user_stress > 0.4:
        st.sidebar.warning("少し疲れが溜まっています。")
    else:
        st.sidebar.success("安定した状態です。")
    
    return user_stress