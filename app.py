# app.py

import os
import requests
import streamlit as st

# Fetch API key securely
SERP_API_KEY = os.getenv("SERPAPI_KEY")

# List of Infosys competitors
competitors = [
    "TCS", "Wipro", "HCLTech", "Accenture", "Capgemini", "Cognizant",
    "IBM", "Tech Mahindra", "DXC Technology"
]

def search_with_serpapi(query):
    url = "https://serpapi.com/search.json"
    params = {
        "engine": "google",
        "q": query,
        "api_key": SERP_API_KEY,
        "num": 5
    }
    response = requests.get(url, params=params)
    data = response.json()
    results = []
    if "organic_results" in data:
        for item in data["organic_results"]:
            results.append({
                "title": item.get("title", ""),
                "link": item.get("link", ""),
                "snippet": item.get("snippet", "")
            })
    return results

# Streamlit app starts
st.set_page_config(page_title="Virgin Media Collaboration Finder", layout="wide")
st.title("🔎 Virgin Media Collaboration Finder")

if st.button("Run Research"):
    collaborations = {}
    progress_bar = st.progress(0)

    for idx, competitor in enumerate(competitors):
        query = f"Virgin Media {competitor} partnership OR case study OR collaboration"
        st.write(f"🔍 Searching for: **{competitor}**...")
        try:
            results = search_with_serpapi(query)
            collaborations[competitor] = results
        except Exception as e:
            st.error(f"Error fetching results for {competitor}: {e}")
        progress_bar.progress((idx + 1) / len(competitors))

    st.success("✅ Research Complete!")

    if collaborations:
        for competitor, results in collaborations.items():
            if results:
                st.subheader(f"Competitor: {competitor}")
                for result in results:
                    st.markdown(f"**Title**: {result['title']}")
                    st.markdown(f"**Snippet**: {result['snippet']}")
                    st.markdown(f"[🔗 View Link]({result['link']})")
                    st.markdown("---")
else:
    st.info("👆 Click the 'Run Research' button to start finding collaborations!")

