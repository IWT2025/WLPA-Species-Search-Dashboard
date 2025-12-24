import pandas as pd
import streamlit as st

# Filenames in the repo
WLPA_FILE = "WLPA.xlsx"
SCHED4_FILE = "WLPA-SchIV.xlsx"

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

    Expected columns in WLPA-SchIV.xlsx:
        - 'Schedule'    (text like 'Schedule-IV')
        - 'I'           (Appendix I entries)
        - 'II_family'   (Appendix II family names or notes)
        - 'II_species'  (Appendix II species names or notes)
        - 'III'         (Appendix III entries)

    All non-empty cells in I / II_family / II_species / III are kept exactly,
    as 'ScientificNameOrText', with an Appendix column indicating I / II / III.
    """
    # Read sheet (default first sheet); change sheet_name if needed
    raw = pd.read_excel(SCHED4_FILE)

    # Ensure expected columns exist; rename if your headers differ
    col_map = {
        "Schedule": "Schedule",
        "I": "I",
        "II_family": "II_family",
        "II_species": "II_species",
        "III": "III",
    }
    raw = raw.rename(columns=col_map)

    # Fill missing columns if not present
    for col in ["Schedule", "I", "II_family", "II_species", "III"]:
        if col not in raw.columns:
            raw[col] = ""

    records = []

    def add_records_from_column(col_name, appendix_label):
        # For each non-empty cell in the given column, create a record
        for _, row in raw.iterrows():
            schedule_val = str(row.get("Schedule", "")).strip()
            text_val = row.get(col_name, None)

            if pd.isna(text_val):
                continue

            text_str = str(text_val).strip()
            if not text_str:
                continue

            records.append({
                "Schedule": schedule_val or "Schedule-IV",
                "Appendix": appendix_label,
                # Keep entire cell content as-is
                "ScientificNameOrText": text_str,
            })

    # Build records for Appendix I, II (two columns), III
    add_records_from_column("I", "I")
    add_records_from_column("II_family", "II")
    add_records_from_column("II_species", "II")
    add_records_from_column("III", "III")

    if not records:
        return pd.DataFrame(columns=["Schedule", "Appendix", "ScientificNameOrText"])

    df = pd.DataFrame(records)

    # Normalize whitespace
    for col in ["Schedule", "Appendix", "ScientificNameOrText"]:
        df[col] = df[col].astype(str).str.strip()

    return df


# ---------- STREAMLIT APP LAYOUT ----------

st.set_page_config(page_title="WLPA Species & Scheduled Specimens", layout="centered")

st.title("WLPA Species Finder")

st.markdown(
    "This app lets you search:\n"
    "- **WLPA Schedules I, II, III** by common or scientific name, and\n"
    "- **Scheduled specimens (Schedule IV)** by scientific/family names or notes."
)

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

if not common_q and not sci_q:
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

st.header("Scheduled Specimens (Schedule IV)")

sched4 = load_schedule_iv()

sched4_query = st.text_input(
    "Search by scientific name, family name or any text", ""
)

sched4_q = sched4_query.strip()

if not sched4_q:
else:
    mask4 = sched4["ScientificNameOrText"].str.contains(sched4_q, case=False, na=False)
    results4 = sched4[mask4].copy()

    if results4.empty:
        st.warning("No Scheduled Specimens found matching your query.")
    else:
        st.success(f"Found {len(results4)} Scheduled Specimen record(s).")
        display4 = results4.rename(columns={
            "Schedule": "Schedule",
            "Appendix": "Appendix",
            "ScientificNameOrText": "Scientific name / family / notes",
        })
        st.dataframe(
            display4[["Schedule", "Appendix", "Scientific name / family / notes"]]
            .reset_index(drop=True)
        )


