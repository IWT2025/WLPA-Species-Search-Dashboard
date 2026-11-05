# WLPA Species Lookup

**Live app:** https://wlpa-species-search.streamlit.app/

A searchable reference to the species protected under the **Wild Life
(Protection) Act, 1972 — Schedules I to IV, as on 5 June 2025** — with their
CITES Appendix and IUCN Red List status. Built and maintained by the
**[Wildlife Trust of India](https://www.wti.org.in/)** for enforcement officers,
researchers and anyone who needs to know quickly whether, and how, a species is
protected in India.

> **Disclaimer.** This app is meant for **quick reference only**. We have taken
> every care to reproduce the Act faithfully: each species, its Schedule, Part,
> serial number and the way it is listed. Even so, errors can remain, and the
> app is not a substitute for the law. **Always refer to the authoritative text
> of the Wild Life (Protection) Act, 1972**, as notified by the Government of
> India, before relying on any entry for legal, enforcement or official
> purposes. The Wildlife Trust of India accepts no liability for decisions taken
> on the basis of this app.

---

## Why this exists

The Schedules of the Act list more than 3,500 entries across mammals, birds,
reptiles, amphibians, fish, invertebrates and plants, together with the CITES
species brought in by the 2022 amendment (Schedule IV). The official text is
long, hard to search, and — as we found — carries printing errors that make
some species hard to find.

While building this tool we read every entry of the official text against the
printed page and found **128 errors** in the Schedules as published: misspelt
scientific names (*Copra falconeri* for *Capra falconeri*), words run together
or split, misplaced columns, a missing class heading and missing or wrong
serial numbers. Each was checked on the page and signed off by the Wildlife
Trust of India.

**The full list is published here:
[Errata in the Schedules to the Wild Life (Protection) Act, 1972](errata/WLPA_Schedules_errata.pdf)**
(PDF, 7 pages). Page by page, it gives the location of each error, the text as
printed and the proposed correction, with the nature of each error.

## How it was built

1. **Source.** The text of Schedules I–IV was extracted from India Code's
   consolidated Wild Life (Protection) Act, 1972, **as on 5 June 2025** — the
   only source of the species lists.
2. **Errors found.** Every name was compared with the rendered page, with an
   earlier copy of the Schedules, and with taxonomic references (GBIF, the
   IUCN Red List, CITES Species+). Suspected errors went into a correction
   ledger, never into the Act's text itself.
3. **Human review.** Each proposed correction was checked against the printed
   page by the Wildlife Trust of India and accepted or rejected. Names that
   follow Indian usage, including that of the Zoological Survey of India, were
   kept as printed even where other authorities use a different name.
4. **Enrichment.** Each entry was linked to its CITES Appendix (from the Act's
   own Schedule IV and CITES Species+), its IUCN Red List category, its
   taxonomy, and its common and local names.
5. **Safety checks.** Where the Act protects a whole family or genus "except
   those listed in Schedule I", the species of that group were listed out and
   the Schedule I species carved out, and an audit confirms that no Schedule I
   species is shown at a lower level of protection.
6. **The app.** Everything is packed into one self-contained page,
   `WLPA_species_reference.html`, which this repository serves online and which
   also works offline once saved.

In the app, the **Act's printed text is always shown**. Where we have corrected
it, the correction is shown alongside, and the entry can be found under both
spellings.

## Please use it sensibly

- **It is a quick reference, not the law.** The legal text is the Act as
  notified in the Gazette of India and its amendments. Before relying on an
  entry in a prosecution, a seizure, a permit or any legal document, confirm it
  against the official text.
- **Corrections are ours.** Where this app corrects a misprint, the official
  text still reads as printed until it is corrected officially. Quote the Act as
  printed and note the correction, rather than quoting the correction as the Act.
- **Status changes.** CITES and IUCN listings change over time and the Act can
  be amended. The app reflects the Act as on 5 June 2025; check the date before
  relying on it.
- **Do not alter and redistribute it as an official list.** If you find an
  error, tell us (below) rather than circulating a modified copy.

## Using and citing this work

You are welcome to use the app and its data for conservation, enforcement,
research and education. **Please credit the Wildlife Trust of India** whenever
you use, reproduce or build on it:

> Wildlife Trust of India (2026). *WLPA Species Lookup: Schedules I–IV of the
> Wild Life (Protection) Act, 1972, as on 5 June 2025.*
> https://wlpa-species-search.streamlit.app/

GitHub's **"Cite this repository"** button (from `CITATION.cff`) gives the same
citation in other formats.

Data drawn from third parties remains subject to their own terms, in
particular the [IUCN Red List terms of use](https://www.iucnredlist.org/terms/terms-of-use)
and [CITES Species+](https://speciesplus.net/). The Act itself is published by
the Government of India on [India Code](https://indiacode.gov.in/).

## Reporting an error

If you find an entry that looks wrong, please open an
[issue](https://github.com/IWT2025/WLPA-Species-Search-Dashboard/issues) with
the species, the Schedule and serial number, and what you believe is correct
(with a source if you have one), or write to the Wildlife Trust of India.

## What is in this repository

| File | What it is |
|---|---|
| `WLPA_species_reference.html` | The whole app: one self-contained page. Generated by WTI's build pipeline; not edited by hand |
| `WLPA-App.py` (and `app.py`, the same file) | Shows that page on Streamlit |
| `errata/WLPA_Schedules_errata.pdf` | The 128 errors found in the Schedules as published, page by page |
| `CITATION.cff` | How to cite this work |
| `legacy/` | The earlier Excel-based version of the app (2025), kept for reference |

To update the app, replace `WLPA_species_reference.html` with the newly built
page and push; Streamlit redeploys on its own.

---

© Wildlife Trust of India.
