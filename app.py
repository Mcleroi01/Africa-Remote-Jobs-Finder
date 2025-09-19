import streamlit as st
import pandas as pd
from backend.aggregate import search_all, available_sources

st.set_page_config(page_title="Africa Remote Jobs Finder", page_icon="🌍", layout="wide")

st.title("🌍 Africa Remote Jobs Finder")
st.caption("Find legit remote jobs open to candidates in Africa across multiple sites.")

with st.sidebar:
    st.header("Search")
    query = st.text_input("Keyword (e.g., Laravel, Flutter, React, Fullstack)", value="React")
    source_options = available_sources()
    selected_sources = st.multiselect(
        "Sources",
        options=source_options,
        default=source_options,
        help="Choose which job boards to query"
    )
    stacks = st.multiselect(
        "Filter by stack (optional)",
        ["Python", "Django", "Flask", "FastAPI", "JavaScript", "TypeScript", "React", "Next.js", "Vue", "Nuxt",
         "Node", "Express", "Java", "Spring", "Kotlin", "Swift", "Flutter", "Dart", "Laravel", "PHP", "Ruby", "Rails",
         "Go", "Rust", "AWS", "GCP", "Azure", "Postgres", "MySQL", "MongoDB", "Docker", "Kubernetes",
         "Frontend", "Backend", "Fullstack"],
    )
    run = st.button("Search", use_container_width=True)

@st.cache_data(ttl=300, show_spinner=False)
def cached_search(q: str, sources: tuple[str, ...]):
    return search_all(q, list(sources))

if run and query.strip():
    with st.spinner("Searching jobs across multiple sources..."):
        jobs = cached_search(query.strip(), tuple(selected_sources))
        # Apply optional stack filters
        if stacks:
            selected = set(s.lower() for s in stacks)
            jobs = [j for j in jobs if selected.intersection({s.lower() for s in j.skills})]

    if not jobs:
        st.info("No matching remote jobs found that are clearly open to Africa. Try another keyword or fewer filters.")
    else:
        df = pd.DataFrame([{
            "Title": j.title,
            "Company": j.company,
            "Key Skills": ", ".join(j.skills),
            "Source": j.source,
            "Location Hint": j.location_hint or "",
            "Apply Link": j.url,
        } for j in jobs])

        st.success(f"Found {len(df)} jobs")
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Apply Link": st.column_config.LinkColumn("Apply Link")
            }
        )

        with st.expander("Show raw results"):
            st.json([j.to_dict() for j in jobs])
else:
    st.empty()

st.markdown("---")
st.caption("Results are ephemeral and fetched in real time. Sources include RemoteOK, WeWorkRemotely, Remotive, Remote.co, Jobicy, and selected AI companies (Greenhouse).")
