import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from pubmed_fetcher.fetcher import fetch_pubmed_ids

def test_fetch_pubmed_ids():
    query = "covid-19 vaccine"
    ids = fetch_pubmed_ids(query, max_results=5)
    assert isinstance(ids, list)
    assert all(isinstance(i, str) for i in ids)
    assert len(ids) <= 5
