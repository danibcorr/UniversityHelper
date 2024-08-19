# 🏫 University Helper

## 📝 Overview

University Helper is a comprehensive toolset designed to assist students, educators, and researchers in managing and processing various types of academic data. This repository contains several scripts, each dedicated to a specific task, from metadata management to audio transcription and beyond. 

### Features

- **Metadata Management (`2_📝_Metadata.py`)**: Randomly modify the metadata of selected files and create a customized cover page featuring the subject or degree name. This helps in organizing documents systematically.
- **PDF to Markdown Conversion (`3_📄_PDF_to_Markdown.py`)**: Seamlessly convert PDF documents into Markdown format for easier editing and content management.
- **Audio Transcription (`4_🎙️_Audio_Transcription.py`)**: Convert audio files into text transcriptions or record audio from the microphone and transcribe it automatically.
- **Pomodoro Timer (`5_🍅_Pomodoro.py`)**: Boost productivity using the Pomodoro technique, which breaks down work into intervals with short breaks.
- **Grade Statistics (`6_📊_Stats.py`)**: Retrieve and analyze grade statistics to gain insights into academic performance.

## 💻 Installation

To use the University Helper, you'll need to set up the project locally. Follow these steps to get started:

1. **Clone the Repository:**

   ```bash
   git clone [repository-url]
   ```

2. **Install Dependencies:**

   Use `pip` to install the required dependencies listed in the `requirements.txt` file:

   ```bash
   pip install -r requirements.txt
   ```

3. **Install Tesseract OCR (for OCR functionality):**

   University Helper uses Tesseract for Optical Character Recognition (OCR) to process text from images and PDFs. Follow the instructions at the following links to install Tesseract:

   - [pytesseract GitHub Repository](https://github.com/h/pytesseract)
   - [Tesseract OCR GitHub Repository](https://github.com/tesseract-ocr/tesseract)

## 🚀 Usage

To launch the University Helper, start the main Streamlit script:

```bash
streamlit run 1_🏠_Home.py
```

This will open the application in your web browser, where you can access all the available tools and features.

## 🤝 Contribution

We welcome contributions from the community! If you'd like to contribute, please fork the repository, create a new branch for your feature or bug fix, and submit a pull request. Here are a few ways you can contribute:

- **Report Bugs:** Found a bug? Create an issue describing the problem.
- **Add Features:** Have an idea for a new feature? Implement it and submit a pull request.
- **Improve Documentation:** Help us improve our README or other documentation files.

Let's work together to make University Helper even better!