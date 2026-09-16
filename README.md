# 🛡️ WikiVerify Pro: The Intelligence Auditor for Global Knowledge

WikiVerify Pro is a professional-grade research tool designed to transform Wikipedia from a "wall of text" into a verifiable database of claims. By leveraging the **Wikimedia Enterprise Structured Contents dataset**, WikiVerify Pro allows users to audit the credibility of information, map the structure of complex topics, and compare knowledge reliability across different language editions.

## 🌟 Key Features

### 1. 🛡️ Credibility & Trust Auditing
Instead of manually searching for `[citation needed]` tags, WikiVerify Pro programmatically scans the dataset's credibility signals:
- **Trust Scoring**: Calculates an overall credibility percentage for any article.
- **Signal Detection**: Automatically identifies `referenceneed` (unsupported claims) and `referencerisk` (claims backed by low-quality sources).
- **Source Health**: Analyzes the diversity and volume of unique citations.

### 2. 🌍 Global Knowledge Audit (Cross-Language)
Knowledge varies by culture and language. WikiVerify Pro can audit a topic across multiple language editions (English and French):
- **Comparative Reliability**: Tells you which language edition provides a more reliable, better-sourced account of a topic.
- **Cross-Referencing**: Identifies when a claim is "unsupported" in one language but "verified" in another.

### 3. 🗺️ Visual Knowledge Mapping
Understand the architecture of a topic at a glance:
- **Structure Flowcharts**: Automatically converts the hierarchical section structure of an article into a **Mermaid.js** flowchart.
- **Visual Hierarchy**: Renders the map as an image (via GUI) to show how sub-topics branch from the main subject.

### 4. 📌 Intelligence Synthesis
Get the essence of a topic without the noise:
- **Key Point Extraction**: Extracts the core abstract and the lead sentences of every major section to create a "TL;DR" of the article.
- **AI-Ready**: Built-in support for LLM API keys to enable advanced AI-powered summarization.

---

## 🛠️ Technical Architecture

WikiVerify Pro uses a decoupled three-layer architecture for maximum performance:

- **The Engine (`engine.py`)**: Powered by **DuckDB**. It queries 40GB+ of Parquet files on-disk without loading them into RAM, enabling millisecond response times.
- **The TUI (`tui.py`)**: A high-performance terminal interface built with **Rich**, designed for power users and developers.
- **The GUI (`gui.py`)**: An interactive web dashboard built with **Streamlit**, featuring visual metrics, tabs, and rendered charts.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- [uv](https://github.com/astral-sh/uv) (recommended for lightning-fast package management)
- The **Wikimedia Enterprise Structured Contents** Parquet dataset (English and French editions)

### Installation
```bash
# Clone the repository
git clone https://github.com/your-repo/wikiverify-pro.git
cd wikiverify-pro

# Install dependencies using uv
uv pip install -r requirements.txt
```

### Running the Application

#### Option A: The TUI (Terminal User Interface)
Best for fast audits and command-line automation.
```bash
# Basic audit
uv run python src/interfaces/tui/tui.py

# Full Intelligence Audit (Flowcharts, Key Points, and Cross-Language)
uv run python src/interfaces/tui/tui.py --flowchart --key-points --cross-lang
```

#### Option B: The GUI (Web Dashboard)
Best for visual research and deep-dive analysis.
```bash
uv run streamlit run src/interfaces/gui/gui.py
```

---

## 📊 Data Configuration
When prompted (or in the GUI sidebar), provide the paths to your Parquet shards:
- **English Path**: `path/to/enwiki/data/*.parquet`
- **French Path**: `path/to/frwiki/data/*.parquet`

## 📜 Attribution & Licensing
This project utilizes data from the Wikimedia Enterprise initiative. All users are expected to conform to the **Wikimedia Attribution Framework**. Please ensure you provide proper credit to the Wikimedia community when using the outputs of this tool.

---
**Developed for the AI and Research Community to fight misinformation with evidence.**
