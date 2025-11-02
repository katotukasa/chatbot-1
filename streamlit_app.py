import os
import sys
from google import genai
from google.genai import types

# Streamlit環境で使用する場合、st.secrets から読み込むためにインポート
try:
    import streamlit as st
except ImportError:
    # Streamlitがインストールされていない場合、ダミーのstを作成
    class DummyStreamlit:
        def get(self, key, default=None):
            return default
    st = DummyStreamlit()

# ----------------------------------------------------
# 1. APIキーの設定とクライアントの初期化
# ----------------------------------------------------

# ① Streamlit Secretsからキーを読み込む (Streamlit Cloudでの推奨方法)
GEMINI_API_KEY = st.get("GEMINI_API_KEY") 

# ② Streamlit Secretsになければ、OSの環境変数から読み込む (ローカル実行での推奨方法)
if not GEMINI_API_KEY:
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# キーが存在しない場合のエラーチェック
if not GEMINI_API_KEY:
    print("--- ⚠️ エラー ---")
    print("APIキーが設定されていません。")
    print("Streamlit Secrets または 環境変数 'GEMINI_API_KEY' にキーを設定してください。")
    # Streamlit環境でなければ終了
    if 'streamlit' not in sys.modules:
         sys.exit(1)
    # Streamlit環境であればエラーメッセージを表示して処理を中断
    else:
        st.error("APIキーが設定されていません。`GEMINI_API_KEY`をSecretsまたは環境変数に設定してください。")
        st.stop()
        
try:
    # 取得したキーを使ってクライアントを初期化
    # genai.Client() は、引数がなければ環境変数 'GEMINI_API_KEY' を自動で探す
    # ただし、今回は明示的にキーを渡すことで、読み込み元(Secrets or os.environ)を明確にする
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    # ローカル実行の場合のみ成功メッセージを表示
    if 'streamlit' not in sys.modules:
        print("クライアントの初期化に成功しました。")

except Exception as e:
    error_message = f"致命的なエラー: クライアントの初期化に失敗しました: {e}"
    if 'streamlit' in sys.modules:
        st.error(error_message)
        st.stop()
    else:
        print(f"--- 致命的なエラー ---")
        print(error_message)
        sys.exit(1)


# ----------------------------------------------------
# 2. プロンプトとモデルの指定
# ----------------------------------------------------
# 使用するモデル名 (例: gemini-2.5-flash は高速で費用対効果が高い)
model_name = 'gemini-2.5-flash'

# 生成させたいテキストのプロンプト
prompt_text = "PythonでWebサーバーを構築する最も簡単な方法を、具体的なコードと合わせて教えてください。"


# ----------------------------------------------------
# 3. APIの呼び出しと結果の表示
# ----------------------------------------------------

# ローカル実行時の表示
if 'streamlit' not in sys.modules:
    print("\n" + "=" * 50)
    print(f"プロンプト: {prompt_text}")
    print(f"モデル: {model_name}")
    print("=" * 50)

try:
    # テキスト生成をリクエスト
    response = client.models.generate_content(
        model=model_name,
        contents=prompt_text,
    )

    # 応答の表示
    if 'streamlit' in sys.modules:
        # Streamlit環境での表示
        st.header("🤖 Gemini の応答")
        st.code(prompt_text, language='text')
        st.markdown(response.text)
    else:
        # ローカル環境での表示
        print("\n--- 🤖 Geminiの応答 ---")
        print(response.text)
        print("-------------------------")

except Exception as e:
    error_message = f"API呼び出し中にエラーが発生しました: {e}"
    if 'streamlit' in sys.modules:
        st.error(error_message)
    else:
        print(f"\n--- API呼び出し中にエラーが発生しました ---")
        print(f"エラー内容: {e}")

# ----------------------------------------------------
