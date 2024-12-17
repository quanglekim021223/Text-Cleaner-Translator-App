import streamlit as st
import re
from googletrans import Translator

# Text cleaning function
def clean_paragraph(text):
    """
    Cleans text by removing unnecessary line breaks and joining sentences properly.
    """
    text = re.sub(r'\n(?=\w)', ' ', text)
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s+([,.!?])', r'\1', text)
    return text.strip()

# Sentence splitting function
def split_sentences(text):
    """
    Splits text into sentences using regex.
    """
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return sentences

# Translate function
def translate_text(sentences, target_language):
    """
    Translates a list of sentences to the target language.
    """
    translator = Translator()
    translated_sentences = []
    for sentence in sentences:
        try:
            translated = translator.translate(sentence, dest=target_language)
            translated_sentences.append(translated.text)
        except Exception:
            translated_sentences.append("[Translation Error]")
    return translated_sentences

# Streamlit app layout
st.set_page_config(page_title="Text Cleaner & Translator", layout="wide")
st.title("📝 Text Cleaner & Translator App")

# Input section
col1, col2 = st.columns(2)
with col1:
    st.header("Input Text")
    user_input = st.text_area(
        "Paste your text here:",
        height=300,
        placeholder="Enter your text..."
    )

    # Checkbox to allow changing the target language
    change_language = st.checkbox("Change target language from Vietnamese")

    # Language code to full name mapping
    language_codes = {
        "None": "None",
        "en": "English",
        "es": "Spanish",
        "fr": "French",
        "de": "German",
        "zh-cn": "Chinese",
        "ja": "Japanese",
        "vi": "Vietnamese"
    }

    if change_language:
        target_lang = st.selectbox(
            "Choose a target language:",
            list(language_codes.values()),
            format_func=lambda x: x if x != "None" else "None",
            index=6  # Default to Vietnamese
        )
    else:
        target_lang = "Vietnamese"

    # Retrieve the selected language code
    target_code = next((code for code, name in language_codes.items() if name == target_lang), "vi")

# Output section
if user_input:
    cleaned_text = clean_paragraph(user_input)
    sentences = split_sentences(cleaned_text)

    # Translation
    if target_lang != "None":
        translated_sentences = translate_text(sentences, target_code)
    else:
        translated_sentences = []

    with col2:
        st.header("Cleaned Text & Translated Text")

        # Display sentences side-by-side with hover effects
        st.markdown("""
        <style>
        .sentence-box {
            padding: 10px;
            margin-bottom: 5px;
            border-radius: 5px;
            transition: background-color 0.3s ease;
        }
        .sentence-box:hover {
            background-color: #94908c;
        }
        .highlight {
            background-color: #94908c;
            transition: background-color 0.3s ease;
        }
        </style>
        """, unsafe_allow_html=True)

        # Render sentences dynamically with hover interaction
        for i, sentence in enumerate(sentences):
            translated_sentence = translated_sentences[i] if translated_sentences else ""
            st.markdown(
                f"""
                <div class="sentence-box" onmouseover="this.classList.add('highlight')" onmouseout="this.classList.remove('highlight')">
                    <b>Cleaned:</b> {sentence}<br>
                    <b>Translated:</b> {translated_sentence}
                </div>
                """,
                unsafe_allow_html=True
            )
else:
    st.info("Enter text to clean and translate.")