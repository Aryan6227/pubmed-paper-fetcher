import argparse
from pubmed_fetcher.fetcher import fetch_pubmed_ids, fetch_pubmed_details, save_papers_to_csv

def main():
    parser = argparse.ArgumentParser(description="Fetch PubMed papers with non-academic authors.")
    parser.add_argument("query", help="PubMed query string")
    parser.add_argument("-f", "--file", help="CSV filename to save results")
    parser.add_argument("-d", "--debug", action="store_true", help="Print debug info")
    
    args = parser.parse_args()

    if args.debug:
        print("🔍 Querying PubMed with:", args.query)

    ids = fetch_pubmed_ids(args.query)
    if args.debug:
        print(f"📄 Found {len(ids)} PubMed IDs")

    papers = fetch_pubmed_details(ids)

    if args.file:
        save_papers_to_csv(papers, args.file)
    else:
        for paper in papers:
            print("📝 Title:", paper["Title"])
            print("📅 Date:", paper["PublicationDate"])
            print("👥 Non-Academic Authors:", paper["NonAcademicAuthors"])
            print("🏢 Company Affiliations:", paper["CompanyAffiliations"])
            print("📧 Email:", paper["CorrespondingEmail"])
            print("---")

    if not papers:
        print("⚠️ No results found for the given query.")
        return
