# 🧪 PubMed Paper Fetcher

A Python CLI tool to fetch PubMed research papers that include at least one author affiliated with a **pharmaceutical or biotech** company.

---

## 🚀 Features

- Accepts full PubMed query syntax
- Fetches metadata using NCBI Entrez API
- Filters authors with **non-academic affiliations**
- Extracts **company affiliations** and **corresponding author email**
- Saves results to CSV
- Debug/log mode for easy tracing

---

## 📦 Installation & Setup

### 1. Install Requirements

```bash
# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Clone the repository
git clone https://github.com/your-username/pubmed-paper-fetcher.git
cd pubmed-paper-fetcher

# Install dependencies
poetry install

```

### 2. Run the CLI Tool

```bash
poetry run get-papers-list "covid-19 vaccine" -f output.csv -
```

**🔧 Arguments:**

- **query** → The PubMed search string (required)

- **-f**, **--file** → CSV filename (optional; prints to console if omitted)

- **-d**, **--debug** → Print extra debug info

---

## 🧠 Heuristics for Non-Academic Detection

- We identify non-academic authors by checking if their affiliations do not contain academic keywords like:

**"university", "hospital", "institute", "department", etc.**

- You can tweak this list in utils.py.

---

## 🗂 Output Columns

- **Field** - Description
- **PubmedID** - Unique PubMed article ID
- **Title** - Title of the paper
- **Publication Date** - Year of publication
- **Non-academic Author(s)** - Names of non-academic authors
- **Company Affiliation(s)** - Company or organization names
- **Corresponding Author Email** - Email of first matched author

---

## 🧪 Testing

Basic unit tests are inside tests/. Run:

```bash
poetry run pytest
```

---

## 🔍 Tools Used

- **NCBI Entrez API**

- **Poetry** for dependency and CLI packaging

- **Requests** for API calls

- **Pandas** for CSV creation

---

**Thank You**

---