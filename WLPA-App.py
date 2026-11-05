"""
WLPA Species Reference, served on Streamlit.

The app is a single self-contained page, WLPA_species_reference.html, built
in the wlpa-db project (python rebuild.py) from the Wild Life (Protection)
Act, 1972 as on 5 June 2025 (India Code). To update the site, replace that
file with the newly built one and push; Streamlit redeploys on its own.

The earlier Excel-based app is kept in legacy/.
"""
import pathlib

import streamlit as st

st.set_page_config(page_title="WLPA Species Reference", page_icon="🐾",
                   layout="wide", initial_sidebar_state="collapsed")

# The page is a full-screen app with its Search / Browse / About bar pinned
# to the bottom of the window. Inside a fixed-height frame that bar ends up
# below the screen, so the frame is pinned to the browser window instead:
# exactly one screen tall, with the page scrolling inside it.
st.markdown("""
<style>
  header[data-testid="stHeader"], footer {display: none !important;}
  .block-container {padding: 0 !important; max-width: 100% !important;}
  iframe {position: fixed !important; inset: 0 !important;
          width: 100vw !important; height: 100vh !important;
          height: 100dvh !important; border: 0 !important; z-index: 999;}
  html, body {overflow: hidden !important;}
</style>""", unsafe_allow_html=True)

HTML = pathlib.Path(__file__).with_name("WLPA_species_reference.html")
if hasattr(st, "iframe"):                       # Streamlit 1.5x and later
    st.iframe(HTML, height=1400)
else:                                           # older Streamlit
    import streamlit.components.v1 as components
    components.html(HTML.read_text(encoding="utf-8"), height=1400,
                    scrolling=True)
