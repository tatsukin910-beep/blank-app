import streamlit as st
import time
from cognitive_os.core import CognitiveOS
from components.sidebar import render_sidebar
from components.results import display_result

def main():
    st.set_page_config(
        page_title="Cognitive OS v4", 
        page_icon="🧠", 
        layout="centered"
    )
    
    st.title("🧠 Cognitive OS v4")
    st.markdown("---")

    user_stress = render_sidebar()

    event = st.text_input(
        "何が起きていますか？（イベント入力）", 
        placeholder="例：返信が来ない、自分の気持ちがわからない"
    )

    if st.button("▶ 思考プロセス実行", use_container_width=True):
        if not event:
            st.info("何か入力してください。")
            st.stop()

        os = CognitiveOS(stress=user_stress)

        with st.status("思考プロセスのシミュレーション中...", expanded=True) as status:
            result, logs = os.process(event)
            time.sleep(0.8)
            status.update(label="完了！", state="complete")

        display_result(result, logs)

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🛑 Panic Button", use_container_width=True):
            st.toast("強制停止しました")
            st.error("🚨 今は考えなくていい。深呼吸して。")
    with col2:
        if st.button("🔄 Reset", use_container_width=True):
            st.rerun()

if __name__ == "__main__":
    main()