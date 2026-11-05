import pandas as pd
import streamlit as st

# Filenames in the repo
WLPA_FILE = "WLPA.xlsx"
SCHED4_FILE = "WLPA-SchIV.xlsx"

# ---------- STREAMLIT APP LAYOUT ----------

st.set_page_config(page_title="WLPA Species & Scheduled Specimens (Exotics)", layout="centered")

# =======================  RESPONSIVE FONT & COLOR SETTINGS  =======================
st.markdown(
    """
    <style>
    /* Default (desktop-ish) base styles */
    html, body {
        font-family: Arial, sans-serif;
        font-size: 16px;
    }

    /* Light mode defaults */
    body {
        background-color: #ffffff;
        color: #111111;
    }

    /* Dark mode override when OS/browser prefers dark */
    @media (prefers-color-scheme: dark) {
        body {
            background-color: #000000;
            color: #f5f5f5;
        }

        h1, h2, h3 {
            color: #f5f5f5;
        }

        .stMarkdown p,
        .stTextInput label,
        .stTextInput input,
        .stDataFrame div {
            color: #f5f5f5;
        }
    }

    /* PAGE TITLE (st.title -> h1) */
    h1 {
        font-size: 22px;
        font-weight: 600;
        text-align: center;
    }

    /* SECTION HEADERS (st.header -> h2) */
    h2 {
        font-size: 20px;
        font-weight: 600;
    }

    /* SUBHEADERS (st.subheader -> h3, if used) */
    h3 {
        font-size: 18px;
        font-weight: 500;
    }

    /* NORMAL TEXT (st.markdown paragraphs) */
    .stMarkdown p {
        font-size: 14px;
    }

    /* TEXT INPUT LABELS */
    .stTextInput label {
        font-size: 13px;
    }

    /* TEXT INSIDE TEXT INPUT BOX */
    .stTextInput input {
        font-size: 13px;
    }

    /* TABLE TEXT */
    .stDataFrame div {
        font-size: 13px;
    }

    .stAlert {
        font-size: 13px;
    }

    /* --------- MOBILE / SMALL SCREEN ADJUSTMENTS --------- */
    @media (max-width: 768px) {
        html, body {
            font-size: 14px;
        }

        h1 {
            font-size: 20px;
        }

        h2 {
            font-size: 18px;
        }

        h3 {
            font-size: 16px;
        }

        .stMarkdown p {
            font-size: 13px;
        }

        .stTextInput label {
            font-size: 12px;
        }

        .stTextInput input {
            font-size: 12px;
        }

        .stDataFrame div {
            font-size: 12px;
        }

        .stAlert {
            font-size: 12px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)
# =======================  END RESPONSIVE SETTINGS  =======================

st.title("The Wild Life (Protection) Act, 1972 - Scheduled Species Finder")

st.markdown(
    "This app lets you search:\n"
    "- **WLPA Schedules I, II, III** by common or scientific name, and\n"
    "- **Scheduled specimens (Schedule IV)** by scientific names. Scheduled specimens are commonly called exotic species."
)

# ---------- LOAD WLPA SCHEDULES I–III (GENERAL SPECIES SEARCH) ----------

@st.cache_data
def load_wlpa_1_3():
    """
    Load Schedules I, II, III from WLPA.xlsx.
    Shows only Schedule, CommonName, ScientificName.
    """
    # Schedule I
    s1 = pd.read_excel(WLPA_FILE, sheet_name="Schedule-I")
    s1 = s1.rename(columns={
        "Schedule": "Schedule",
        "Common Name": "CommonName",
        "Scientific Name": "ScientificName",
    })
    s1 = s1[["Schedule", "CommonName", "ScientificName"]]

    # Schedule II
    s2 = pd.read_excel(WLPA_FILE, sheet_name="Schedule-II")
    s2 = s2.rename(columns={
        "Schedule": "Schedule",
        "Common Name": "CommonName",
        "Scientific Name": "ScientificName",
    })
    s2 = s2[["Schedule", "CommonName", "ScientificName"]]

    # Schedule III
    s3 = pd.read_excel(WLPA_FILE, sheet_name="Schedule-III")
    s3 = s3.rename(columns={
        "schedule": "Schedule",
        "Common Name": "CommonName",
        "Scintific Name": "ScientificName",
    })
    s3 = s3[["Schedule", "CommonName", "ScientificName"]]

    df = pd.concat([s1, s2, s3], ignore_index=True)

    for col in ["CommonName", "ScientificName"]:
        df[col] = df[col].astype(str).str.strip()

    return df


# ---------- LOAD WLPA SCHEDULE IV (SCHEDULED SPECIMENS) ----------

@st.cache_data
def load_schedule_iv():
    """
    Load Schedule IV (Scheduled Specimens) from WLPA-SchIV.xlsx.

    Structure of WLPA-SchIV.xlsx:
        - Sheet 'I'   : one column with species text for Appendix I
        - Sheet 'II'  : one column with species text for Appendix II
        - Sheet 'III' : one column with species text for Appendix III

    All non-empty cells in each sheet's single column are kept exactly,
    as 'ScientificNameOrText', with an Appendix column indicating I / II / III.
    """
    records = []

    # Helper to read a sheet with a single species column
    def read_appendix_sheet(sheet_name: str, appendix_label: str):
        try:
            df = pd.read_excel(SCHED4_FILE, sheet_name=sheet_name)
        except Exception:
            return

        if df.empty:
            return

        # Assume the first column contains the species / text
        first_col = df.columns[0]

        for _, row in df.iterrows():
            text_val = row.get(first_col, None)

            if pd.isna(text_val):
                continue

            text_str = str(text_val).strip()
            if not text_str:
                continue

            records.append({
                "Schedule": "Schedule-IV",
                "Appendix": appendix_label,
                "ScientificNameOrText": text_str,
            })

    # Read sheets I, II, III
    read_appendix_sheet("I", "I")
    read_appendix_sheet("II", "II")
    read_appendix_sheet("III", "III")

    if not records:
        return pd.DataFrame(columns=["Schedule", "Appendix", "ScientificNameOrText"])

    df = pd.DataFrame(records)
    for col in ["Schedule", "Appendix", "ScientificNameOrText"]:
        df[col] = df[col].astype(str).str.strip()

    return df


# ---------- SECTION 1: SCHEDULE I–III SEARCH ----------

st.header("Species in Schedules I–III")

wlpa_1_3 = load_wlpa_1_3()

col1, col2 = st.columns(2)
with col1:
    common_query = st.text_input(
        "Common name (exact or partial match)", ""
    )
with col2:
    sci_query = st.text_input(
        "Scientific name (exact or partial match)", ""
    )

common_q = common_query.strip()
sci_q = sci_query.strip()

# Only run search when at least one input has text
if common_q or sci_q:
    mask = pd.Series([True] * len(wlpa_1_3))

    if sci_q:
        mask &= wlpa_1_3["ScientificName"].str.contains(sci_q, case=False, na=False)
    if common_q:
        mask &= wlpa_1_3["CommonName"].str.contains(common_q, case=False, na=False)

    results = wlpa_1_3[mask].copy()

    if results.empty:
        st.warning("No species found in Schedules I–III matching your query.")
    else:
        st.success(f"Found {len(results)} species in Schedules I–III.")
        display = results.rename(columns={
            "Schedule": "Schedule",
            "CommonName": "Common name",
            "ScientificName": "Scientific name",
        })
        st.dataframe(
            display[["Schedule", "Common name", "Scientific name"]].reset_index(drop=True)
        )

# ---------- SECTION 2: SCHEDULED SPECIMENS (SCHEDULE IV) ----------

st.header("Scheduled Specimens (Schedule IV) - Exotics")

sched4 = load_schedule_iv()

sched4_query = st.text_input(
    "Search ONLY by scientific name", ""
)

sched4_q = sched4_query.strip()

# Only run search when there is text
if sched4_q:
    mask4 = sched4["ScientificNameOrText"].str.contains(sched4_q, case=False, na=False)
    results4 = sched4[mask4].copy()

    if results4.empty:
        st.warning("No Scheduled Specimens found matching your query.")
    else:
        st.success(f"Found {len(results4)} Scheduled Specimen record(s).")
        display4 = results4.rename(columns={
            "Schedule": "Schedule",
            "Appendix": "Appendix",
            "ScientificNameOrText": "Scientific name / family",
        })
        st.dataframe(
            display4[["Schedule", "Appendix", "Scientific name / family"]]
            .reset_index(drop=True)
        )

