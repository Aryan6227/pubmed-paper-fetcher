import requests
import pandas as pd
from xml.etree import ElementTree as ET
from typing import List, Dict
from pubmed_fetcher.utils import is_academic_affiliation, extract_email

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

def fetch_pubmed_ids(query: str, max_results: int = 20) -> List[str]:
    """
    Fetch PubMed IDs using a search query.
    """
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": max_results
    }
    try:
        response = requests.get(f"{BASE_URL}/esearch.fcgi", params=params, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ Error fetching PubMed IDs: {e}")
        return []

    data = response.json()
    return data.get("esearchresult", {}).get("idlist", [])

def fetch_pubmed_details(id_list: List[str]) -> List[Dict]:
    """
    Fetch detailed data for given PubMed IDs.
    """
    if not id_list:
        return []

    ids = ",".join(id_list)
    params = {
        "db": "pubmed",
        "id": ids,
        "retmode": "xml"
    }

    try:
        response = requests.get(f"{BASE_URL}/efetch.fcgi", params=params, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ Error fetching PubMed details: {e}")
        return []
    
    root = ET.fromstring(response.text)
    articles = []

    for article in root.findall(".//PubmedArticle"):
        pubmed_id = article.findtext(".//PMID")
        title = article.findtext(".//ArticleTitle")
        pub_date = article.findtext(".//PubDate/Year") or "Unknown"
        authors = []

        non_academic_authors = []
        company_affiliations = set()
        corresponding_email = None

        for author in article.findall(".//Author"):
            name = f"{author.findtext('ForeName', '')} {author.findtext('LastName', '')}".strip()
            affiliation = author.findtext(".//Affiliation", "") or ""
            
            if not is_academic_affiliation(affiliation):
                non_academic_authors.append(name)
                company_affiliations.add(affiliation)

            email = extract_email(affiliation)
            if email and not corresponding_email:
                corresponding_email = email  # First valid email found

        # Add to articles:
        articles.append({
            "PubmedID": pubmed_id,
            "Title": title,
            "PublicationDate": pub_date,
            "NonAcademicAuthors": non_academic_authors,
            "CompanyAffiliations": list(company_affiliations),
            "CorrespondingEmail": corresponding_email
        })

    return articles

def save_papers_to_csv(papers: List[Dict], filename: str) -> None:
    """
    Save the list of filtered papers to a CSV file.
    """
    df = pd.DataFrame([{
        "PubmedID": paper["PubmedID"],
        "Title": paper["Title"],
        "Publication Date": paper["PublicationDate"],
        "Non-academic Author(s)": ", ".join(paper["NonAcademicAuthors"]),
        "Company Affiliation(s)": ", ".join(paper["CompanyAffiliations"]),
        "Corresponding Author Email": paper["CorrespondingEmail"] or ""
    } for paper in papers])

    df.to_csv(filename, index=False)
    print(f"✅ Results saved to {filename}")