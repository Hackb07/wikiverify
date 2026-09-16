import duckdb
import json
import re
import base64
from typing import Dict, Any, List, Optional

class WikiVerifyEngine:
    def __init__(self, data_path: str):
        """
        Initialize the engine with the path to the Parquet files.
        data_path: Path to the directory containing the .parquet files (e.g., '/data/enwiki/*.parquet')
        """
        self.conn = duckdb.connect(database=':memory:')
        self.data_path = data_path

    def search_article(self, topic: str, path_override: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Search for an article by name and return its structured data."""
        target_path = path_override if path_override else self.data_path
        query = f"""
            SELECT * FROM '{target_path}'
            WHERE name ILIKE ?
            LIMIT 1
        """
        result = self.conn.execute(query, [f"%{topic}%"]).fetchone()

        if not result:
            return None

        cols = self.conn.execute(f"DESCRIBE SELECT * FROM '{target_path}'").fetchall()
        col_names = [col[0] for col in cols]
        return dict(zip(col_names, result))

    def analyze_credibility(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the structured data to produce a credibility report."""
        sections_json = article.get('sections', '[]')
        try:
            sections = json.loads(sections_json)
        except json.JSONDecodeError:
            sections = []

        references_json = article.get('references', '[]')
        try:
            references = json.loads(references_json) if isinstance(references_json, str) else references_json
        except json.JSONDecodeError:
            references = []

        all_text = json.dumps(sections)
        ref_needed_count = all_text.count('referenceneed')
        ref_risk_count = all_text.count('referencerisk')

        total_sections = len(sections)
        unique_sources = len(set([r.get('identifier') for r in references if r.get('identifier')]))

        score = 100
        score -= (ref_needed_count * 5)
        score -= (ref_risk_count * 2)
        score = max(0, min(100, score))

        return {
            "overall_score": score,
            "verified_sections": total_sections - ref_needed_count - ref_risk_count,
            "risk_areas": ref_risk_count,
            "unsupported_claims": ref_needed_count,
            "source_count": unique_sources,
            "diversity": "High" if unique_sources > 50 else "Medium" if unique_sources > 20 else "Low",
            "name": article.get('name', 'Unknown'),
            "url": article.get('url', 'N/A')
        }

    def cross_language_audit(self, topic: str, fr_path: str) -> Dict[str, Any]:
        """Compare credibility of a topic between English and French Wikipedia."""
        en_article = self.search_article(topic)
        fr_article = self.search_article(topic, path_override=fr_path)

        en_report = self.analyze_credibility(en_article) if en_article else None
        fr_report = self.analyze_credibility(fr_article) if fr_article else None

        return {
            "en": en_report,
            "fr": fr_report,
            "comparison": "French is more reliable" if (fr_report and en_report and fr_report['overall_score'] > en_report['overall_score'])
                           else "English is more reliable" if (fr_report and en_report and en_report['overall_score'] > fr_report['overall_score'])
                           else "Similar reliability" if (fr_report and en_report) else "Missing data in one or more languages"
        }

    def generate_flowchart(self, article: Dict[str, Any]) -> str:
        """Generates a Mermaid.js flowchart string representing the article structure."""
        sections_json = article.get('sections', '[]')
        try:
            sections = json.loads(sections_json)
        except json.JSONDecodeError:
            return "No sections found to map."

        if not sections:
            return "No sections found to map."

        root = article.get('name', 'Article')
        mermaid = f"graph TD\n  Root({root})\n"

        for i, section in enumerate(sections):
            title = section.get('title', f"Section {i+1}")
            clean_title = title.replace('"', '').replace('(', '').replace(')', '')
            mermaid += f"  Root --> S{i}[{clean_title}]\n"

            subsections = section.get('subsections', [])
            if isinstance(subsections, str):
                try:
                    subsections = json.loads(subsections)
                except:
                    subsections = []

            for j, sub in enumerate(subsections):
                sub_title = sub.get('title', f"Sub {j+1}")
                clean_sub = sub_title.replace('"', '').replace('(', '').replace(')', '')
                mermaid += f"  S{i} --> SS{i}_{j}[{clean_sub}]\n"

        return mermaid

    def get_mermaid_url(self, mermaid_code: str) -> str:
        """Converts mermaid code to a rendered image URL using mermaid.ink."""
        graphbytes = mermaid_code.encode("ascii")
        base64_bytes = base64.b64encode(graphbytes)
        base64_string = base64_bytes.decode("ascii")
        return f"https://mermaid.ink/img/{base64_string}"

    def extract_key_points(self, article: Dict[str, Any], llm_api_key: Optional[str] = None) -> List[str]:
        """Extracts the most critical points. If llm_api_key is provided, could call a summarizer."""
        if llm_api_key:
            # This is a placeholder for a real API call (OpenAI/Anthropic)
            return [f"[LLM Summary] High-level synthesis of {article.get('name')} using AI..."]

        points = []
        abstract = article.get('abstract', '')
        if abstract:
            points.append(f"CORE: {abstract}")

        sections_json = article.get('sections', '[]')
        try:
            sections = json.loads(sections_json)
        except json.JSONDecodeError:
            sections = []

        for section in sections:
            title = section.get('title', 'Unnamed Section')
            content = section.get('content', '')
            if content:
                first_sentence = content.split('. ')[0] + '.' if '. ' in content else content[:150]
                points.append(f"{title}: {first_sentence}")

        return points
