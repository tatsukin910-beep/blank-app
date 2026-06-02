import streamlit as st
import pandas as pd

def display_result(result, logs):
    if "EMERGENCY" in result:
        st.error(result)
        st.warning("🧠 **OSからのアドバイス:** 思考がループしています。今はこれ以上考えても解決しません。")
    else:
        st.success(result)
        st.info("🧠 **OSからのアドバイス:** 今の状態なら、直感に従って軽く決めてしまっても大丈夫そうです。")

    if logs:
        st.markdown("### 思考プロセス履歴")
        df = pd.DataFrame(logs)
        st.dataframe(df, use_container_width=True, hide_index=True)