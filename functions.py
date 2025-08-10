
import wave
import streamlit as st
import os
import time
from pathlib import Path
from audio_recorder_streamlit import audio_recorder
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain.schema import SystemMessage
from langchain.chains import ConversationChain
from pydub import AudioSegment
import constants as ct

def is_audio_long_enough(audio_input_file_path, min_duration=0.1):
    """
    音声ファイルが指定秒数以上か判定。

    Args:
        audio_input_file_path (str): 音声入力ファイルのパス
        min_duration (float): 最小秒数

    Returns:
        bool: 指定秒数以上ならTrue
    """
    with wave.open(audio_input_file_path, 'rb') as wf:
        frames = wf.getnframes()
        rate = wf.getframerate()
        duration = frames / float(rate)
        return duration >= min_duration

def record_audio(audio_input_file_path):
    """
    Streamlitのaudio_recorder_streamlitで音声を録音し、ファイルに保存する。

    Args:
        audio_input_file_path (str): 保存先のファイルパス
    """
    audio = audio_recorder(
        text="発話開始",
        neutral_color="gray",
        recording_color="red",
        icon_name="microphone",
        icon_size="3x"
    )
    if audio is not None and len(audio) > 0:
        with open(audio_input_file_path, "wb") as f:
            f.write(audio)
    else:
        st.stop()

def transcribe_audio(audio_input_file_path):
    """
    音声入力ファイルから文字起こしテキストを取得。

    Args:
        audio_input_file_path (str): 音声入力ファイルのパス

    Returns:
        str: 文字起こし結果
    """
    if not is_audio_long_enough(audio_input_file_path):
        st.warning("録音が短すぎます。もう一度録音してください。")
        os.remove(audio_input_file_path)
        st.stop()
    with open(audio_input_file_path, 'rb') as audio_input_file:
        transcript = st.session_state.openai_obj.audio.transcriptions.create(
            model="whisper-1",
            file=audio_input_file,
            language="en"
        )
    os.remove(audio_input_file_path)
    return transcript

def save_to_wav(llm_response_audio, audio_output_file_path):
    """
    一旦mp3形式で音声ファイル作成後、wav形式に変換。

    Args:
        llm_response_audio (bytes): LLMからの回答の音声データ
        audio_output_file_path (str): 出力先のファイルパス
    """
    temp_audio_output_filename = f"{ct.AUDIO_OUTPUT_DIR}/temp_audio_output_{int(time.time())}.mp3"
    with open(temp_audio_output_filename, "wb") as temp_audio_output_file:
        temp_audio_output_file.write(llm_response_audio)
    audio_mp3 = AudioSegment.from_file(temp_audio_output_filename, format="mp3")
    audio_mp3.export(audio_output_file_path, format="wav")
    os.remove(temp_audio_output_filename)

def play_wav(audio_output_file_path, speed=1.0):
    """
    音声ファイルの読み上げ (Streamlit Cloud対応: st.audioのみ)。

    Args:
        audio_output_file_path (str): 音声ファイルのパス
        speed (float): 再生速度(未使用、将来拡張用)
    """
    with open(audio_output_file_path, "rb") as f:
        audio_bytes = f.read()
    st.audio(audio_bytes, format="audio/wav")
    os.remove(audio_output_file_path)

def create_chain(system_template):
    """
    LLMによる回答生成用のChain作成。

    Args:
        system_template (str): システムプロンプト

    Returns:
        ConversationChain: 会話チェーン
    """
    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content=system_template),
        MessagesPlaceholder(variable_name="history"),
        HumanMessagePromptTemplate.from_template("{input}")
    ])
    chain = ConversationChain(
        llm=st.session_state.llm,
        memory=st.session_state.memory,
        prompt=prompt
    )
    return chain

def create_problem_and_play_audio():
    """
    問題生成と音声ファイルの再生。

    Returns:
        tuple: (生成された問題文, LLM音声レスポンス)
    """
    problem = st.session_state.chain_create_problem.predict(input="")
    llm_response_audio = st.session_state.openai_obj.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=problem
    )
    audio_output_file_path = f"{ct.AUDIO_OUTPUT_DIR}/audio_output_{int(time.time())}.wav"
    save_to_wav(llm_response_audio.content, audio_output_file_path)
    play_wav(audio_output_file_path, st.session_state.speed)
    return problem, llm_response_audio

def create_evaluation():
    """
    ユーザー入力値の評価生成。

    Returns:
        str: 評価結果
    """
    llm_response_evaluation = st.session_state.chain_evaluation.predict(input="")
    return llm_response_evaluation

def save_to_wav(llm_response_audio, audio_output_file_path):
    """
    一旦mp3形式で音声ファイル作成後、wav形式に変換
    Args:
        llm_response_audio: LLMからの回答の音声データ
        audio_output_file_path: 出力先のファイルパス
    """

    temp_audio_output_filename = f"{ct.AUDIO_OUTPUT_DIR}/temp_audio_output_{int(time.time())}.mp3"
    with open(temp_audio_output_filename, "wb") as temp_audio_output_file:
        temp_audio_output_file.write(llm_response_audio)
    
    audio_mp3 = AudioSegment.from_file(temp_audio_output_filename, format="mp3")
    audio_mp3.export(audio_output_file_path, format="wav")

    # 音声出力用に一時的に作ったmp3ファイルを削除
    os.remove(temp_audio_output_filename)

def play_wav(audio_output_file_path, speed=1.0):
    """
    音声ファイルの読み上げ（Streamlit Cloud対応: st.audioのみ）
    Args:
        audio_output_file_path: 音声ファイルのパス
        speed: 再生速度（未使用、将来拡張用）
    """
    import streamlit as st
    import os
    with open(audio_output_file_path, "rb") as f:
        audio_bytes = f.read()
    st.audio(audio_bytes, format="audio/wav")
    os.remove(audio_output_file_path)

def create_chain(system_template):
    """
    LLMによる回答生成用のChain作成
    """

    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content=system_template),
        MessagesPlaceholder(variable_name="history"),
        HumanMessagePromptTemplate.from_template("{input}")
    ])
    chain = ConversationChain(
        llm=st.session_state.llm,
        memory=st.session_state.memory,
        prompt=prompt
    )

    return chain

def create_problem_and_play_audio():
    """
    問題生成と音声ファイルの再生
    Args:
        chain: 問題文生成用のChain
        speed: 再生速度（1.0が通常速度、0.5で半分の速さ、2.0で倍速など）
        openai_obj: OpenAIのオブジェクト
    """

    # 問題文を生成するChainを実行し、問題文を取得
    problem = st.session_state.chain_create_problem.predict(input="")

    # LLMからの回答を音声データに変換
    llm_response_audio = st.session_state.openai_obj.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=problem
    )

    # 音声ファイルの作成
    audio_output_file_path = f"{ct.AUDIO_OUTPUT_DIR}/audio_output_{int(time.time())}.wav"
    save_to_wav(llm_response_audio.content, audio_output_file_path)

    # 音声ファイルの読み上げ
    play_wav(audio_output_file_path, st.session_state.speed)

    return problem, llm_response_audio

def create_evaluation():
    """
    ユーザー入力値の評価生成
    """

    llm_response_evaluation = st.session_state.chain_evaluation.predict(input="")

    return llm_response_evaluation