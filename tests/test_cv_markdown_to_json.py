"""Tests for scripts/cv_markdown_to_json.py"""

import json
import os
import tempfile
from datetime import date, datetime
from pathlib import Path

import pytest
import yaml

# Add scripts directory to path so we can import the module
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from cv_markdown_to_json import (
    DateTimeEncoder,
    create_cv_json,
    extract_author_info,
    parse_config,
    parse_education,
    parse_markdown_cv,
    parse_portfolio,
    parse_publications,
    parse_skills,
    parse_talks,
    parse_teaching,
    parse_work_experience,
)


# ---------------------------------------------------------------------------
# DateTimeEncoder
# ---------------------------------------------------------------------------

class TestDateTimeEncoder:
    def test_encodes_datetime(self):
        dt = datetime(2024, 3, 15, 10, 30, 0)
        result = json.dumps({"d": dt}, cls=DateTimeEncoder)
        assert '"2024-03-15T10:30:00"' in result

    def test_encodes_date(self):
        d = date(2024, 3, 15)
        result = json.dumps({"d": d}, cls=DateTimeEncoder)
        assert '"2024-03-15"' in result

    def test_raises_for_non_date(self):
        with pytest.raises(TypeError):
            json.dumps({"d": {1, 2, 3}}, cls=DateTimeEncoder)


# ---------------------------------------------------------------------------
# parse_markdown_cv
# ---------------------------------------------------------------------------

class TestParseMarkdownCv:
    def _write(self, tmp_path, content):
        p = tmp_path / "cv.md"
        p.write_text(content)
        return str(p)

    def test_strips_front_matter(self, tmp_path):
        md = "---\ntitle: CV\nlayout: page\n---\n\nEducation\n=========\n* PhD, MIT, 2020\n"
        sections = parse_markdown_cv(self._write(tmp_path, md))
        assert "Education" in sections

    def test_extracts_multiple_sections(self, tmp_path):
        md = (
            "Education\n=========\n* PhD, MIT, 2020\n\n"
            "Skills\n======\nPython, Java\n"
        )
        sections = parse_markdown_cv(self._write(tmp_path, md))
        assert "Education" in sections
        assert "Skills" in sections

    def test_empty_file(self, tmp_path):
        sections = parse_markdown_cv(self._write(tmp_path, ""))
        assert sections == {}

    def test_section_content_preserved(self, tmp_path):
        md = "Education\n=========\n* PhD, MIT, 2020\n"
        sections = parse_markdown_cv(self._write(tmp_path, md))
        assert "PhD" in sections.get("Education", "")


# ---------------------------------------------------------------------------
# parse_config
# ---------------------------------------------------------------------------

class TestParseConfig:
    def test_nonexistent_file(self):
        assert parse_config("/nonexistent/config.yml") == {}

    def test_valid_yaml(self, tmp_path):
        cfg = tmp_path / "_config.yml"
        cfg.write_text(yaml.dump({"name": "Test User", "url": "https://example.com"}))
        result = parse_config(str(cfg))
        assert result["name"] == "Test User"
        assert result["url"] == "https://example.com"


# ---------------------------------------------------------------------------
# extract_author_info
# ---------------------------------------------------------------------------

class TestExtractAuthorInfo:
    def test_empty_config(self):
        result = extract_author_info({})
        assert result["name"] == ""
        assert result["profiles"] == []

    def test_top_level_name_and_url(self):
        result = extract_author_info({"name": "Alice", "url": "https://alice.io"})
        assert result["name"] == "Alice"
        assert result["website"] == "https://alice.io"

    def test_author_overrides_name(self):
        config = {"name": "Fallback", "author": {"name": "Real Name"}}
        result = extract_author_info(config)
        assert result["name"] == "Real Name"

    def test_email_and_location(self):
        config = {"author": {"email": "a@b.com", "location": "Boston"}}
        result = extract_author_info(config)
        assert result["email"] == "a@b.com"
        assert result["location"]["city"] == "Boston"

    def test_employer_and_bio_summary(self):
        config = {"author": {"employer": "ACME", "bio": "Researcher"}}
        result = extract_author_info(config)
        assert "ACME" in result["summary"]
        assert "Researcher" in result["summary"]

    def test_bio_only_summary(self):
        config = {"author": {"bio": "Researcher"}}
        result = extract_author_info(config)
        assert result["summary"] == "Researcher"

    def test_social_profiles(self):
        config = {
            "author": {
                "github": "alice",
                "linkedin": "alice-doe",
                "twitter": "alicedoe",
                "googlescholar": "https://scholar.google.com/alice",
                "orcid": "https://orcid.org/0000-0001",
                "researchgate": "https://researchgate.net/alice",
            }
        }
        result = extract_author_info(config)
        networks = {p["network"] for p in result["profiles"]}
        assert networks == {"GitHub", "LinkedIn", "Twitter", "Google Scholar", "ORCID", "ResearchGate"}

    def test_github_profile_url(self):
        config = {"author": {"github": "alice"}}
        result = extract_author_info(config)
        gh = [p for p in result["profiles"] if p["network"] == "GitHub"][0]
        assert gh["url"] == "https://github.com/alice"
        assert gh["username"] == "alice"


# ---------------------------------------------------------------------------
# parse_education
# ---------------------------------------------------------------------------

class TestParseEducation:
    def test_empty_text(self):
        assert parse_education("") == []

    def test_single_entry(self):
        text = "* Ph.D. in Computer Science, MIT, 2020"
        entries = parse_education(text)
        assert len(entries) == 1
        assert entries[0]["institution"] == "MIT"
        assert entries[0]["area"] == "Ph.D. in Computer Science"
        assert entries[0]["endDate"] == "2020"

    def test_entry_with_gpa(self):
        text = "* B.S. in Math, Stanford, 2016, GPA: 3.9"
        entries = parse_education(text)
        assert entries[0]["gpa"] == "3.9"

    def test_multiple_entries(self):
        text = "* Ph.D., MIT, 2020\n* B.S., Stanford, 2016"
        entries = parse_education(text)
        assert len(entries) == 2


# ---------------------------------------------------------------------------
# parse_work_experience
# ---------------------------------------------------------------------------

class TestParseWorkExperience:
    def test_empty_text(self):
        assert parse_work_experience("") == []

    def test_single_entry(self):
        text = "* Researcher, Google, 2018 - 2022"
        entries = parse_work_experience(text)
        assert len(entries) == 1
        assert entries[0]["company"] == "Google"
        assert entries[0]["position"] == "Researcher"
        assert entries[0]["startDate"] == "2018"
        assert entries[0]["endDate"] == "2022"

    def test_entry_with_present(self):
        text = "* Engineer, Meta, 2020 - present"
        entries = parse_work_experience(text)
        assert entries[0]["endDate"] == "present"

    def test_entry_with_highlights(self):
        text = "* Researcher, Google, 2018 - 2022\n  - Led team of 5\n  - Published 3 papers"
        entries = parse_work_experience(text)
        assert len(entries[0]["highlights"]) == 2


# ---------------------------------------------------------------------------
# parse_skills
# ---------------------------------------------------------------------------

class TestParseSkills:
    def test_empty_text(self):
        assert parse_skills("") == []

    def test_single_category(self):
        text = "Programming: Python, Java, C++"
        entries = parse_skills(text)
        assert len(entries) == 1
        assert entries[0]["name"] == "Programming"
        assert "Python" in entries[0]["keywords"]

    def test_multiple_categories(self):
        text = "Programming: Python, Java\nFrameworks: PyTorch, TensorFlow"
        entries = parse_skills(text)
        assert len(entries) == 2


# ---------------------------------------------------------------------------
# parse_publications (filesystem-based)
# ---------------------------------------------------------------------------

class TestParsePublications:
    def test_nonexistent_dir(self):
        assert parse_publications("/nonexistent/dir") == []

    def test_parses_md_files(self, tmp_path):
        pub_dir = tmp_path / "_publications"
        pub_dir.mkdir()
        (pub_dir / "2024-01-01-paper.md").write_text(
            "---\ntitle: My Paper\nvenue: NeurIPS\ndate: 2024-01-01\npaperurl: https://example.com\nexcerpt: A summary\n---\nBody text\n"
        )
        pubs = parse_publications(str(pub_dir))
        assert len(pubs) == 1
        assert pubs[0]["name"] == "My Paper"
        assert pubs[0]["publisher"] == "NeurIPS"
        assert pubs[0]["website"] == "https://example.com"

    def test_skips_non_md(self, tmp_path):
        pub_dir = tmp_path / "_publications"
        pub_dir.mkdir()
        (pub_dir / "notes.txt").write_text("not a publication")
        assert parse_publications(str(pub_dir)) == []

    def test_multiple_publications_sorted(self, tmp_path):
        pub_dir = tmp_path / "_publications"
        pub_dir.mkdir()
        (pub_dir / "2024-01-01-a.md").write_text("---\ntitle: A\nvenue: V\ndate: 2024-01-01\n---\n")
        (pub_dir / "2023-06-01-b.md").write_text("---\ntitle: B\nvenue: V\ndate: 2023-06-01\n---\n")
        pubs = parse_publications(str(pub_dir))
        assert len(pubs) == 2
        # sorted by filename → 2023 before 2024
        assert pubs[0]["name"] == "B"
        assert pubs[1]["name"] == "A"


# ---------------------------------------------------------------------------
# parse_talks
# ---------------------------------------------------------------------------

class TestParseTalks:
    def test_nonexistent_dir(self):
        assert parse_talks("/nonexistent/dir") == []

    def test_parses_talk(self, tmp_path):
        talks_dir = tmp_path / "_talks"
        talks_dir.mkdir()
        (talks_dir / "2024-01-01-talk.md").write_text(
            "---\ntitle: My Talk\nvenue: ICML\ndate: 2024-01-01\nlocation: Vienna\nexcerpt: A great talk\n---\n"
        )
        talks = parse_talks(str(talks_dir))
        assert len(talks) == 1
        assert talks[0]["name"] == "My Talk"
        assert talks[0]["event"] == "ICML"
        assert talks[0]["location"] == "Vienna"


# ---------------------------------------------------------------------------
# parse_teaching
# ---------------------------------------------------------------------------

class TestParseTeaching:
    def test_nonexistent_dir(self):
        assert parse_teaching("/nonexistent/dir") == []

    def test_parses_teaching(self, tmp_path):
        teach_dir = tmp_path / "_teaching"
        teach_dir.mkdir()
        (teach_dir / "2024-spring-cs101.md").write_text(
            "---\ntitle: CS101\nvenue: MIT\ndate: 2024-01-15\ntype: TA\nexcerpt: Intro to CS\n---\n"
        )
        teaching = parse_teaching(str(teach_dir))
        assert len(teaching) == 1
        assert teaching[0]["course"] == "CS101"
        assert teaching[0]["institution"] == "MIT"
        assert teaching[0]["role"] == "TA"


# ---------------------------------------------------------------------------
# parse_portfolio
# ---------------------------------------------------------------------------

class TestParsePortfolio:
    def test_nonexistent_dir(self):
        assert parse_portfolio("/nonexistent/dir") == []

    def test_parses_portfolio(self, tmp_path):
        port_dir = tmp_path / "_portfolio"
        port_dir.mkdir()
        (port_dir / "project.md").write_text(
            "---\ntitle: Cool Project\ncollection: portfolio\ndate: 2024-03-01\npermalink: /portfolio/cool\nexcerpt: Something cool\n---\n"
        )
        items = parse_portfolio(str(port_dir))
        assert len(items) == 1
        assert items[0]["name"] == "Cool Project"
        assert items[0]["url"] == "/portfolio/cool"


# ---------------------------------------------------------------------------
# create_cv_json (integration)
# ---------------------------------------------------------------------------

class TestCreateCvJson:
    def test_creates_valid_json(self, tmp_path):
        # Set up a minimal repo structure
        repo = tmp_path / "repo"
        repo.mkdir()
        pages = repo / "_pages"
        pages.mkdir()

        # Create a CV markdown file
        cv_md = pages / "cv.md"
        cv_md.write_text(
            "---\ntitle: CV\nlayout: page\n---\n\n"
            "Education\n=========\n* Ph.D., MIT, 2020\n\n"
            "Work experience\n===============\n* Researcher, Google, 2018 - 2022\n\n"
            "Skills\n======\nProgramming: Python, Java\n"
        )

        # Create config
        config_file = repo / "_config.yml"
        config_file.write_text(yaml.dump({
            "name": "Test User",
            "url": "https://example.com",
            "author": {"name": "Test User", "github": "testuser"},
        }))

        # Create required dirs (even if empty)
        (repo / "_publications").mkdir()
        (repo / "_talks").mkdir()
        (repo / "_teaching").mkdir()
        (repo / "_portfolio").mkdir()

        output = tmp_path / "cv.json"
        create_cv_json(str(cv_md), str(config_file), str(repo), str(output))

        assert output.exists()
        data = json.loads(output.read_text())

        assert data["basics"]["name"] == "Test User"
        assert len(data["education"]) == 1
        assert len(data["work"]) == 1
        assert len(data["skills"]) == 1
        assert isinstance(data["publications"], list)
        assert isinstance(data["presentations"], list)

    def test_handles_missing_sections(self, tmp_path):
        repo = tmp_path / "repo"
        repo.mkdir()
        pages = repo / "_pages"
        pages.mkdir()

        cv_md = pages / "cv.md"
        cv_md.write_text("---\ntitle: CV\n---\nJust some text\n")

        config_file = repo / "_config.yml"
        config_file.write_text(yaml.dump({"name": "Nobody"}))

        for d in ("_publications", "_talks", "_teaching", "_portfolio"):
            (repo / d).mkdir()

        output = tmp_path / "cv.json"
        create_cv_json(str(cv_md), str(config_file), str(repo), str(output))

        data = json.loads(output.read_text())
        assert data["basics"]["name"] == "Nobody"
        assert data["education"] == []
        assert data["work"] == []
