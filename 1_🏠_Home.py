# %% Libraries

import streamlit as st

# %% Parameters for Streamlit

# Set the page configuration for Streamlit
st.set_page_config(page_title="Home", page_icon="🏠", layout="wide")
st.title("🏠 Welcome to Your Document Management Tool")
st.sidebar.image("./images/logo.png")

# %% Functions

def text_home() -> None:

    """
    Display the home page content with an overview of the application's features.
    """

    # Project Overview
    st.markdown("# Overview")
    st.markdown("""
    Welcome to our document management application, designed to simplify and enhance how you handle documents. 
    Our app offers a suite of tools to help you edit metadata, convert files, transcribe audio, and more, 
    all within a user-friendly interface.
    """)

    col1, col2 = st.columns(2)

    with col1:

        # Metadata Section
        st.markdown("# 📑 Metadata Editing")
        st.markdown("""
        Use the **Metadata** page to easily modify document metadata and add custom cover pages. 
        This feature ensures your documents are well-organized and present a professional appearance, 
        with all the necessary information right where it needs to be.
        """)

        # PDF to Markdown Section
        st.markdown("# 📄 PDF to Markdown Conversion")
        st.markdown("""
        The **PDF to Markdown** page allows you to convert PDF files into Markdown format, 
        making content extraction and editing a breeze. 
        It's an essential tool for anyone who works with static documents but needs the flexibility of Markdown.
        """)

        # Audio Transcription Section
        st.markdown("# 🎙️ Audio Transcription")
        st.markdown("""
        Our **Audio Transcription** feature lets you transcribe audio files directly within the app. 
        Whether you're converting YouTube videos, recorded lectures, or other audio content, 
        this tool makes it simple to generate text transcripts for further analysis or documentation.
        """)

    with col2:
            
        # Pomodoro Timer Section
        st.markdown("# ⏲️ Pomodoro Timer")
        st.markdown("""
        Stay productive with our **Pomodoro Timer**. This feature helps you manage your time effectively, 
        breaking your work into intervals with short breaks to boost focus and prevent burnout.
        """)

        # Stats Section
        st.markdown("# 📊 Stats and Insights")
        st.markdown("""
        The **Stats** page offers insights and statistics to track your productivity and document management activities. 
        Analyze your work patterns and improve your efficiency with data-driven insights.
        """)

def main() -> None:

    """
    Main entry point of the application.
    """
    
    text_home()

# %% Main

if __name__ == '__main__':
    
    main()
