import streamlit as st
import sys
from pathlib import Path

APP_PATH = Path(__file__).resolve().parent
PROJECT_ROOT = None
for p in (APP_PATH, *APP_PATH.parents):
    if (p / "src").exists():
        PROJECT_ROOT = p
        break

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

st.set_page_config(page_title="Job Station", layout="wide")
st.title("Job Station")

from app.pipeline_loader import get_scrape_pipeline
from app.ui_scrapers import render_scrapers_tab

pipeline, pipeline_err = get_scrape_pipeline(PROJECT_ROOT)

tabs = st.tabs(["Data", "DB", "RAG"])

with tabs[0]:
    st.header("Data")
    st.markdown("Zbieraj dane")
    render_scrapers_tab(pipeline, PROJECT_ROOT, pipeline_err)

with tabs[1]:
    st.header("DB")
    st.write("Placeholder")
    if st.button("Sprawdź Qdrant"):
        st.info("Placeholder")

with tabs[2]:
    st.header("RAG")
    st.write("Placeholder: narzędzia RAG pojawią się tutaj.")
    if st.button("RAG"):
        st.info("Placeholder")
