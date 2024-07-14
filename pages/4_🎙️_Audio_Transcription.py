# %% Libraries

import streamlit as st
import datetime
import io
import os
import whisper
import numpy as np
from audiorecorder import audiorecorder

# %% Parameters for Streamlit

# Set the page configuration for Streamlit
st.set_page_config(page_title = "Audio Transcription", page_icon = "🎙️", layout = "wide")
st.title("🎙️ Audio Transcription")
st.sidebar.image("./images/logo.png")

# %% Functions

def load_whisper_model(model_option: str) -> whisper.Whisper:

    """
    Load the Whisper model.

    Args:
        model_option (str): The name of the Whisper model to load.

    Returns:
        whisper.Whisper: The loaded Whisper model.
    """

    return whisper.load_model(model_option, in_memory = True)

def record_audio() -> audiorecorder:

    """
    Record audio using the audiorecorder.

    Returns:
        audiorecorder: The recorded audio.
    """

    return audiorecorder("Click to record", "Click to stop recording")

def transcribe_file(model: whisper.Whisper, file: str) -> str:

    """
    Transcribe an audio file using the Whisper model.

    Args:
        model (whisper.Whisper): The Whisper model to use for transcription.
        file (str): The path to the audio file.

    Returns:
        str: The transcribed text, or None if an error occurred.
    """

    try:

        with st.spinner("Transcribing audio..."):

            result = model.transcribe(file, fp16 = False)

        transcription_text = result['text']
        st.write(f"Transcription: {transcription_text}")
        st.success("Transcription completed!")

        return transcription_text

    except Exception as e:

        st.error(f"Error transcribing audio: {str(e)}")

        return None

def save_markdown(text: str, filename: str) -> None:

    """
    Save the transcribed text as a markdown file.

    Args:
        text (str): The text to save.
        filename (str): The name of the file to save.
    """

    # Ensure the directory exists
    os.makedirs(os.path.dirname(filename), exist_ok = True)

    try:

        with open(filename, 'w', encoding = 'utf-8') as f:

            f.write(text)

        st.success(f"Transcription saved as markdown to {filename}")

    except IOError as e:

        st.error(f"IOError: {str(e)}. Please check the file path and permissions.")

    except Exception as e:

        st.error(f"Unexpected error: {str(e)}")

@st.cache_resource
def get_model(option: str) -> whisper.Whisper:

    """
    Get the Whisper model, using caching to avoid reloading.

    Args:
        option (str): The name of the Whisper model to load.
    
    Returns:
        whisper.Whisper: The loaded Whisper model.
    """
    
    return load_whisper_model(option)

def main() -> None:

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Model Configuration")

        # Model selection
        model_option = st.selectbox("Select Whisper model",
                                    ("tiny", "base", "small", "medium", "large"),
                                    index=2)

        model = get_model(model_option)
        
        st.subheader("File Configuration")

        # Transcription type selection
        transcription_type = st.selectbox("Select transcription type",
                                          ("File", "Microphone"))

        if transcription_type == "File":

            filepath = st.text_input("Enter audio file path:")

            if filepath and st.button("Transcribe"):

                transcription_text = transcribe_file(model, filepath)

                if transcription_text:

                    st.session_state.transcription_text = transcription_text

        else:

            audio = record_audio()

            if len(audio) > 0:

                st.audio(audio.export().read())

                # Convert audio to the format expected by Whisper
                audio_buffer = io.BytesIO()
                audio.export(audio_buffer, format="wav", parameters=["-ar", str(16000)])
                file = np.frombuffer(audio_buffer.getvalue()[44:], dtype=np.int16).astype(np.float32) / 32768.0

                if st.button("Transcribe"):

                    transcription_text = transcribe_file(model, file)

                    if transcription_text:

                        st.session_state.transcription_text = transcription_text

    with col2:

        st.subheader("Save Transcription")
        
        save_path = st.text_input("Enter the path to save the markdown file:", value = f"./transcriptions/transcription_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md")

        if 'transcription_text' in st.session_state and st.button("Save as Markdown"):

            save_markdown(st.session_state.transcription_text, save_path)

# %% Main

if __name__ == '__main__':

    main()
