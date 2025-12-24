import requests
import pandas as pd
import streamlit as st

EXCEL_FILE = "WLPA.xlsx"

# ---------- WLPA SCHEDULES I–III FROM EXCEL ----------

@st.cache_data
def load_wlpa_schedules_1_3():
    # Schedule I
    s1 = pd.read_excel(EXCEL_FILE, sheet_name="Schedule-I")
    s1 = s1.rename(columns={
        "Schedule": "Schedule",
        "Common Name": "CommonName",
        "Scientific Name": "ScientificName"
    })
    s1["Appendix"] = ""
    s1 = s1[["Schedule", "Appendix", "CommonName", "ScientificName"]]

    # Schedule II
    s2 = pd.read_excel(EXCEL_FILE, sheet_name="Schedule-II")
    s2 = s2.rename(columns={
        "Schedule": "Schedule",
        "Common Name": "CommonName",
        "Scientific Name": "ScientificName"
    })
    s2["Appendix"] = ""
    s2 = s2[["Schedule", "Appendix", "CommonName", "ScientificName"]]

    # Schedule III
    s3 = pd.read_excel(EXCEL_FILE, sheet_name="Schedule-III")
    s3 = s3.rename(columns={
        "schedule": "Schedule",
        "Common Name": "CommonName",
        "Scintific Name": "ScientificName"
    })
    s3["Appendix"] = ""
    s3 = s3[["Schedule", "Appendix", "CommonName", "ScientificName"]]

    all_1_3 = pd.concat([s1, s2, s3], ignore_index=True)
    for col in ["CommonName", "ScientificName"]:
        all_1_3[col] = all_1_3[col].astype(str).str.strip()
    return all_1_3


# ---------- SCHEDULE IV FROM CITES API ----------

@st.cache_data
def load_schedule_4_from_cites():
    """
    Uses your CITES Species+ API token (stored in Streamlit secrets)
    to fetch species in CITES Appendices I, II, III and treat them as WLPA Schedule IV.
    Tries to use English common names when available.
    """
    api_token = st.secrets["CITES_API_TOKEN"]  # set this in Streamlit Secrets

    headers = {"X-Authentication-Token": api_token}
    base_url = "https://api.speciesplus.net/api/v1/taxon_concepts"

    all_rows = []

    # Loop over CITES Appendices I, II, III
    for appendix in ["I", "II", "III"]:
        page = 1
        while True:
            params = {
                "page": page,
                "per_page": 500,
                "cites_appendix": appendix,
            }
            response = requests.get(base_url, headers=headers, params=params)

            # Stop if any error from API
            if response.status_code != 200:
                break

            data = response.json()
            results = data.get("taxon_concepts", [])

            # No more results → stop paging this appendix
            if not results:
                break

            for item in results:
                sci_name = item.get("full_name", "")

                # Try to get an English common name if present
                common_name = ""
                # Some responses include `english_common_name`
                if "english_common_name" in item and item["english_common_name"]:
                    common_name = item["english_common_name"]
                # Some include a list `common_names` with language info
                elif "common_names" in item and item["common_names"]:
                    for cn in item["common_names"]:
                        if isinstance(cn, dict):
                            lang = cn.get("language", "")
                            name_val = cn.get("name") or cn.get("full_name") or ""
                            if lang and isinstance(lang, str) and lang.lower().startswith("en"):
                                common_name = name_val
                                break
                    # If still empty, just pick first name
                    if not common_name:
                        cn0 = item["common_names"][0]
                        if isinstance(cn0, dict):
                            common_name = cn0.get("name") or cn0.get("full_name") or ""

                all_rows.append({
                    "Schedule": "Schedule-IV",
                    "Appendix": appendix,
                    "CommonName": common_name or "",
                    "ScientificName": sci_name or ""
                })

            page += 1

    if not all_rows:
        return pd.DataFrame(columns=["Schedule", "Appendix", "CommonName", "ScientificName"])

    df = pd.DataFrame(all_rows)
    for col in ["CommonName", "ScientificName"]:
        df[col] = df[col].astype(str).str.strip()
    return df


# ---------- COMBINE ALL SCHEDULES ----------

@st.cache_data
def load_all_data():
    """
    Combine WLPA Schedules I–III (from Excel) with Schedule IV (from CITES API).
    """
    wlpa_1_3 = load_wlpa_schedules_1_3()
    sched_4 = load_schedule_4_from_cites()
    all_data = pd.concat([wlpa_1_3, sched_4], ignore_index=True)
    for col in ["CommonName", "ScientificName"]:
        all_data[col] = all_data[col].astype(str).str.strip()
    return all_data


# ---------- STREAMLIT UI ----------

st.set_page_config(page_title="WLPA + CITES Species Finder", layout="centered")

st.title("WLPA + CITES Species Finder")
st.write(
    "Search by common name or scientific name to see the WLPA Schedule "
    "and CITES Appendix (for Schedule IV species)."
)

data = load_all_data()

common_input = st.text_input("Common name (exact or partial match)", "")
sci_input = st.text_input("Scientific name (exact or partial match)", "")

common_query = common_input.strip()
sci_query = sci_input.strip()

if not common_query and not sci_query:
    st.info("Enter a common name or scientific name to search.")
else:
    mask = pd.Series([True] * len(data))

    if sci_query:
        mask &= data["ScientificName"].str.contains(sci_query, case=False, na=False)
    if common_query:
        mask &= data["CommonName"].str.contains(common_query, case=False, na=False)

    results = data[mask].copy()

    if results.empty:
        st.warning("No species found matching your query.")
    else:
        st.success(f"Found {len(results)} matching record(s).")
        display = results.rename(columns={
            "Schedule": "Schedule",
            "Appendix": "Appendix",
            "CommonName": "Common name",
            "ScientificName": "Scientific name"
        })
        st.dataframe(
            display[["Schedule", "Appendix", "Common name", "Scientific name"]].reset_index(drop=True)
        )
