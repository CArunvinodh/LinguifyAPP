import streamlit as st
from transformer.app import AcademicTextHumanizer, NLP_GLOBAL, download_nltk_resources
from nltk.tokenize import word_tokenize


def main():
    # Download NLTK resources if needed
    download_nltk_resources()

    # --- Streamlit Page Config ---
    st.set_page_config(
        page_title="Linguify — Academic Text Refiner",
        page_icon="🪶",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # --- Custom CSS for Branding & Modern UI ---
    st.markdown(
        """
        <style>
        /* Global */
        body {
            background-color: #f8fafc;
            font-family: "Inter", sans-serif;
        }

        /* Header Gradient */
        .main-header {
            text-align: center;
            padding: 1.8rem;
            border-radius: 16px;
            background: linear-gradient(90deg, #0072ff, #00c6ff);
            color: white;
            margin-bottom: 2rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }

        .main-header h1 {
            margin: 0;
            font-size: 2.4em;
            font-weight: 800;
            letter-spacing: 1px;
            background: linear-gradient(90deg, #ffffff, #dff5ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .main-header p {
            font-size: 1.1em;
            margin-top: 0.4em;
            opacity: 0.9;
        }

        /* Card Styling */
        .stTextArea, .stFileUploader, .stButton > button {
            border-radius: 10px !important;
        }

        /* Branded Button */
        .stButton > button {
            background: linear-gradient(90deg, #0072ff, #00c6ff);
            color: white;
            border: none;
            font-size: 1em;
            padding: 0.6em 1.4em;
            border-radius: 12px;
            transition: all 0.3s ease;
            font-weight: 600;
        }

        .stButton > button:hover {
            transform: scale(1.05);
            background: linear-gradient(90deg, #00c6ff, #0072ff);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }

        /* Info Bar */
        .info-bar {
            background: #eef3fa;
            border-left: 5px solid #0072ff;
            padding: 0.8em 1.2em;
            border-radius: 10px;
            margin-top: 1.2em;
            font-size: 0.95em;
        }

        /* Output Box */
        .output-box {
            background: #ffffff;
            border: 1px solid #e0e6ed;
            padding: 1.2em;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }

        /* Streamlit Tab Bar (Top Navbar Title) */
        header[data-testid="stHeader"] {
            background: linear-gradient(90deg, #0072ff, #00c6ff);
            height: 55px;
        }

        header[data-testid="stHeader"] div {
            color: white !important;
            font-weight: 700;
            font-size: 1rem;
        }

        /* App Title Bar Gradient Text */
        .title-gradient {
            text-align: center;
            font-size: 2.5em;
            font-weight: 800;
            background: linear-gradient(90deg, #0072ff, #00c6ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: 1.2px;
            margin-bottom: 0.3em;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    # --- HEADER ---
    st.markdown(
        """
        <div class="main-header">
            <h1>Linguify 🪶</h1>
            <p>Refine and Humanize AI-generated content into polished academic writing</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --- SIDEBAR ---
    st.sidebar.title("⚙️ Linguify Options")
    st.sidebar.markdown("Customize your refinement settings:")
    use_passive = st.sidebar.checkbox("Convert sentences to Passive Voice", value=False)
    use_synonyms = st.sidebar.checkbox("Replace with Formal Synonyms", value=False)

    st.sidebar.markdown("---")
    uploaded_file = st.sidebar.file_uploader("📂 Upload a .txt File", type=["txt"])
    st.sidebar.caption("You can also paste text directly below.")

    # --- MAIN INPUT AREA ---
    st.markdown("<h2 class='title-gradient'>📝 Input Text</h2>", unsafe_allow_html=True)
    user_text = st.text_area(
        "Enter or paste your text here:",
        height=220,
        placeholder="Type or paste your text here to refine...",
    )

    if uploaded_file is not None:
        file_text = uploaded_file.read().decode("utf-8", errors="ignore")
        user_text = file_text

    # --- PROCESS BUTTON ---
    if st.button("✨ Refine with Linguify"):
        if not user_text.strip():
            st.warning("⚠️ Please enter or upload text to begin refinement.")
        else:
            with st.spinner("🚀 Linguify is refining your text..."):
                input_word_count = len(word_tokenize(user_text, language='english', preserve_line=True))
                doc_input = NLP_GLOBAL(user_text)
                input_sentence_count = len(list(doc_input.sents))

                humanizer = AcademicTextHumanizer(
                    p_passive=0.3,
                    p_synonym_replacement=0.3,
                    p_academic_transition=0.4
                )
                transformed = humanizer.humanize_text(
                    user_text,
                    use_passive=use_passive,
                    use_synonyms=use_synonyms
                )

                output_word_count = len(word_tokenize(transformed, language='english', preserve_line=True))
                doc_output = NLP_GLOBAL(transformed)
                output_sentence_count = len(list(doc_output.sents))

            # --- OUTPUT DISPLAY ---
            st.markdown("<h2 class='title-gradient'>🎓 Refined Output</h2>", unsafe_allow_html=True)
            st.markdown(f"<div class='output-box'>{transformed}</div>", unsafe_allow_html=True)

            st.markdown(
                f"""
                <div class='info-bar'>
                <b>Input Words:</b> {input_word_count} | 
                <b>Sentences:</b> {input_sentence_count} |
                <b>Output Words:</b> {output_word_count} | 
                <b>Sentences:</b> {output_sentence_count}
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("---")
    st.caption("🪶 Linguify — Academic Text Refiner | Crafted with care by Arunsystems")


if __name__ == "__main__":
    main()
