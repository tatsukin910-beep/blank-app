import streamlit as st
import random
import time

class CognitiveOS:
    def __init__(self, stress=0.3):
        self.stress = stress
        self.completion = 0.0
        self.loops = 0

    def process(self, event):
        self.completion = 0.0
        self.loops = 0
        logs = []

        while self.completion < 0.5:
            self.loops += 1
            risk = self.calc_risk(event)

            if risk < 0.3:
                self.completion += 0.3
            elif risk > 0.6:
                self.completion *= 0.5

            logs.append({
                "loop": self.loops,
                "risk": round(risk, 3),
                "completion": round(self.completion, 3)
            })

            if risk > 0.85 or self.loops >= 3:
                return "⚠️ EMERGENCY → 今は決めない", logs

        return "✅ OK → ソフト判断で進む", logs

    def calc_risk(self, event):
        trigger_words = ["気持ち", "返信", "本音", "不安", "どうしよう"]
        base = 0.65 if any(x in event for x in trigger_words) else 0.3
        risk = base * (1 + self.stress * 0.6)
        risk *= (1 + self.loops * 0.1)
        return min(1.0, risk + random.uniform(-0.05, 0.05))

def main():
    st.set_page_config(page_title="Cognitive OS v4", page_icon="🧠", layout="centered")
    st.title("🧠 Cognitive OS v4")
    st.markdown("---")

    st.sidebar.header("📊 内部パラメータ")
    user_stress = st.sidebar.slider("現在のストレス度", 0.0, 1.0, 0.3, 
                                    help="高いほどリスク判定が厳しくなります")

    st.sidebar.markdown("---")
    st.sidebar.write("### 状態解説")
    if user_stress > 0.7:
        st.sidebar.error("オーバーロード気味です。")
    elif user_stress > 0.4:
        st.sidebar.warning("少し疲れが溜まっています。")
    else:
        st.sidebar.success("安定した状態です。")

    event = st.text_input("何が起きていますか？（イベント入力）", 
                          placeholder="例：返信が来ない、自分の気持ちがわからない")

    if st.button("▶ 思考プロセス実行", use_container_width=True):
        if not event:
            st.info("何か入力してください。")
            return

        os = CognitiveOS(stress=user_stress)

        with st.status("思考プロセスのシミュレーション中...", expanded=True) as status:
            result, logs = os.process(event)
            time.sleep(0.8)

            for log in logs:
                st.write(f"Loop {log['loop']}: リスク度 {log['risk']} | 納得度 {log['completion']}")

            status.update(label="シミュレーション完了", state="complete", expanded=False)

        st.subheader("💡 OSの最終判断")
        if "EMERGENCY" in result:
            st.error(result)
            st.warning("🧠 **OSからのアドバイス:** 思考がループしています。今はこれ以上考えても解決しません。スマホを置いて、別のことをしてください。")
        else:
            st.success(result)
            st.info("🧠 **OSからのアドバイス:** 今の状態なら、直感に従って軽く決めてしまっても大丈夫そうです。")

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
