# app.py
import os
import tempfile

import streamlit as st

from src.pipeline import process_local_file, process_youtube_url


st.set_page_config(page_title="Convolens AI", layout="wide")

st.title("Convolens AI – Smart Audio/Video Analyzer")

st.write(
    "Convert audio, video, or YouTube links into transcripts, **smart summaries**, "
    "**key points**, and **smart improvements** using local AI models."
)


# --- Input section: title + upload + URL ---
st.subheader("Input")

col1, col2 = st.columns(2)

with col1:
    custom_title = st.text_input("Title (optional)", value="")

with col2:
    language = st.text_input("Language code (optional, e.g. 'en')", value="")

uploaded_file = st.file_uploader(
    "Upload audio/video file",
    type=["mp3", "wav", "m4a", "mp4", "mov", "mkv"],
)

url_input = st.text_input("Or paste YouTube URL")


analyze_clicked = st.button("Analyze")


# --- Processing ---
if analyze_clicked:
    if not uploaded_file and not url_input.strip():
        st.error("Please upload a file or provide a YouTube URL.")
    else:
        with st.spinner("Analyzing, please wait..."):
            temp_path = None
            result = None

            try:
                if uploaded_file:
                    # Save uploaded file to temp path
                    with tempfile.NamedTemporaryFile(
                        delete=False, suffix=uploaded_file.name
                    ) as tmp:
                        tmp.write(uploaded_file.read())
                        temp_path = tmp.name

                    result = process_local_file(temp_path, language=language or None)

                elif url_input.strip():
                    result = process_youtube_url(url_input.strip(), language=language or None)

                # Only override title if result exists
                if result and custom_title.strip():
                    result["title"] = custom_title.strip()

            except Exception as e:
                st.error(f"Error during processing: {e}")
                result = None  # make sure we don't use a bad result

            finally:
                if temp_path and os.path.exists(temp_path):
                    os.remove(temp_path)

        # --- Output section ---
        if result:
            st.subheader("Smart Summary Output")

            st.markdown(f"### Title\n{result.get('title', '')}")

            st.markdown("### Smart Summary")
            st.write(result.get("smart_summary", ""))

            st.markdown("### Key Points")
            key_points = result.get("key_points", [])
            if key_points:
                for point in key_points:
                    st.markdown(f"- {point}")
            else:
                st.write("No key points generated.")

            st.markdown("### Smart Improvements")
            improvements = result.get("smart_improvements", [])
            if improvements:
                for imp in improvements:
                    st.markdown(f"- {imp}")
            else:
                st.write("No improvements generated.")

            st.markdown("### Full Transcript")
            st.text_area("Transcript", result.get("transcript", ""), height=250)
