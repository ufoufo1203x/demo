import streamlit as st
import os
import google.generativeai as genai

# ページの設定
st.set_page_config(
    page_title="エコ☘️ アップサイクルジェネレーター",
    page_icon="♻️",
    layout="wide"
)

# カスタムCSSでデザインを強化
st.markdown("""
<style>
    .main-title {
        color: #2c3e50;
        font-size: 2.5em;
        text-align: center;
        margin-bottom: 30px;
        background: linear-gradient(to right, #3498db, #2ecc71);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #3498db;
        padding: 10px;
    }
    .stButton > button {
        background-color: #2ecc71;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #27ae60;
    }
    .sidebar .sidebar-content {
        background-color: #f0f4f7;
    }
</style>
""", unsafe_allow_html=True)

# Gemini APIキーの設定
def set_api_key(api_key):
    """APIキーを設定する関数"""
    try:
        genai.configure(api_key=api_key)
        st.session_state['api_key_valid'] = True
        st.success("APIキーが正常に設定されました！ 🎉")
    except Exception as e:
        st.error(f"APIキーの設定に失敗しました: {e}")
        st.session_state['api_key_valid'] = False

# サイドバーの設定
def sidebar():
    st.sidebar.title("🛠️ エコ設定")
    
    # APIキー入力
    st.sidebar.subheader("Gemini API設定")
    api_key = st.sidebar.text_input("APIキーを入力", type="password", 
                                    key="gemini_api_key_input")
    
    if st.sidebar.button("APIキー設定"):
        if api_key:
            set_api_key(api_key)
        else:
            st.sidebar.warning("APIキーを入力してください")
    
    # 追加情報
    st.sidebar.markdown("---")
    st.sidebar.info("""
    ♻️ このアプリは不要な物をアップサイクルするアイデアを提案します！
    🌍 環境に優しいソリューションを見つけましょう。
    """)

def generate_upcycle_ideas(item_name):
    """Gemini APIを使用してアップサイクル案を生成する"""
    prompt = f"""
    不要な商品の名前：{item_name}

    上記の商品に基づいて、10個のアップサイクル例を考えてください。それぞれの例について、具体的な方法と環境エコ度（CO2削減量を示す指数。高、中、低で評価）を示してください。

    出力形式：
    1. 方法：[具体的な方法]、エコ度：[エコ度]
    2. 方法：[具体的な方法]、エコ度：[エコ度]
    ...
    10. 方法：[具体的な方法]、エコ度：[エコ度]
    """

    try:
        # APIキーが設定されているか確認
        if not st.session_state.get('api_key_valid', False):
            return "⚠️ まずはサイドバーからGemini APIキーを設定してください"

        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"エラーが発生しました: {e}"

def main():
    # サイドバーの追加
    sidebar()

    # メインコンテンツ
    st.markdown("<h1 class='main-title'>♻️ エコ アップサイクルアイデアジェネレーター 🌍</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    ### 🔍 不要な商品をアップサイクルする素晴らしいアイデアを見つけよう！
    環境に優しく、クリエイティブな再利用方法を提案します。
    """)

    # 商品名入力
    item_name = st.text_input("🏷️ 不要な商品の名前を入力してください", 
                               placeholder="例: 古いジーンズ")

    if st.button("✨ アイデアを生成"):
        if item_name:
            with st.spinner("🔄 アイデア生成中..."):
                upcycle_ideas = generate_upcycle_ideas(item_name)
                st.markdown("### 🌿 アップサイクルアイデア:")
                st.write(upcycle_ideas)
        else:
            st.warning("🚨 商品名を入力してください")

# セッション状態の初期化
if 'api_key_valid' not in st.session_state:
    st.session_state['api_key_valid'] = False

# メイン関数の実行
if __name__ == "__main__":
    main()
