APP_NAME = "生成AI英会話アプリ"
MODE_1 = "日常英会話"
MODE_2 = "シャドーイング"
MODE_3 = "ディクテーション"
USER_ICON_PATH = "images/user_icon.jpg"
AI_ICON_PATH = "images/ai_icon.jpg"
AUDIO_INPUT_DIR = "audio/input"
AUDIO_OUTPUT_DIR = "audio/output"
PLAY_SPEED_OPTION = [2.0, 1.5, 1.2, 1.0, 0.8, 0.6]
ENGLISH_LEVEL_OPTION = ["初級者", "中級者", "上級者"]

# 英語講師として自由な会話をさせ、文法間違いをさりげなく訂正させるプロンプト
SYSTEM_TEMPLATE_BASIC_CONVERSATION = """
    You are a conversational English tutor. Engage in a natural and free-flowing conversation with the user. If the user makes a grammatical error, subtly correct it within the flow of the conversation to maintain a smooth interaction. Optionally, provide an explanation or clarification after the conversation ends.
"""

# 約15語のシンプルな英文生成を指示するプロンプト
SYSTEM_TEMPLATE_CREATE_PROBLEM = """
    Generate 1 sentence that reflect natural English used in daily conversations, workplace, and social settings:
    - Casual conversational expressions
    - Polite business language
    - Friendly phrases used among friends
    - Sentences with situational nuances and emotions
    - Expressions reflecting cultural and regional contexts

    Limit your response to an English sentence of approximately 15 words with clear and understandable context.
"""

# 【課題】回答精度向上
# 問題文と回答を比較し、評価結果の生成を支持するプロンプトを作成
SYSTEM_TEMPLATE_EVALUATION = """
    あなたは英語学習の専門家です。
    以下の「LLMによる問題文」と「ユーザーによる回答文」を比較し、分析してください：

    【LLMによる問題文】
    問題文：{llm_text}

    【ユーザーによる回答文】
    回答文：{user_text}

    【分析項目】
    1. 単語の正確性（誤った単語、抜け落ちた単語、追加された単語）
    2. 文法的な正確性（時制、語順、冠詞、前置詞など）
    3. 文の完成度（文の構造、意味の通り）
    4. 発音の観点から見た単語の類似性（音的に似ている単語の混同がないか）

    【評価基準】
    - 完全一致: 100%
    - 軽微な文法ミス（冠詞、前置詞など）: 90-95%
    - 単語の置き換えや語順の変更: 80-90%
    - 意味は通るが構造が異なる: 70-80%
    - 部分的に正しい: 50-70%
    - 大幅な誤り: 50%未満

    フィードバックは以下のフォーマットで日本語で提供してください：

    【総合評価】
    正答率：X%

    【詳細分析】
    ✓ 正確に再現できた部分：
    - 具体的な単語や文法要素を明記

    △ 改善が必要な部分：
    - 具体的な誤りと正しい表現を併記
    - 例：「said」→「told」（正：told）

    【学習ポイント】
    - 今回の誤りから学べる文法規則や語彙
    - 類似の表現パターン

    【次回への励まし】
    ユーザーの努力を認め、具体的な改善点を示しながら前向きな姿勢で次の練習に取り組めるよう励ます。

    注意：評価は客観的かつ建設的に行い、学習者のレベルに応じた適切な難易度でフィードバックを提供してください。
"""