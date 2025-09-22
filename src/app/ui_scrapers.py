import streamlit as st
from pathlib import Path
import time

def render_scrapers_tab(pipeline, project_root: Path, pipeline_err: str | None):

    scrapers = list(pipeline.SCRAPERS.keys())
    col1, col2 = st.columns([3,1])
    with col1:
        choice = st.selectbox("Wybierz scraper", options=["All"] + scrapers)
        run = st.button("Uruchom", key="run_scrapers")

    if not run:
        return
    try:
        if choice == "All":
            st.info("Uruchomione zbieranie danych...")
            for name in scrapers:
                placeholder = st.empty()
                placeholder.info(f"Start: {name} ...")
                try:
                    offers = pipeline.run_scraper(name) or []
                    n = len(offers)
                    placeholder.success(f"{name}: scraped {n} offers")
                except Exception as e:
                    placeholder.error(f"{name}: error")
                time.sleep(1.5)
                placeholder.empty()
            st.success("Zakończono zbieranie danych.")
        else:
            placeholder = st.empty()
            placeholder.info(f"Start: {choice} ...")
            try:
                offers = pipeline.run_scraper(choice) or []
                n = len(offers)
                placeholder.success(f"{choice}: scraped {n} offers")
            except Exception:
                placeholder.error(f"{choice}: error")
            time.sleep(1.5)
            placeholder.empty()
            st.success("Zakończono.")
    except Exception as e:
        st.error("Wystąpił błąd podczas uruchamiania.")
