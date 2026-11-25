# US Life Sciences Quality Assurance Job Finder

Find **Quality Assurance Specialist** and **Senior Quality Assurance Specialist** openings across the USA, including on-site, hybrid and US-eligible remote roles.

This is a personalized fork of [FirstUser369/hourly-ai-data-job-monitor](https://github.com/FirstUser369/hourly-ai-data-job-monitor). The search profile, employers and workflow have been changed from AI/data jobs to life-sciences QA.

## Search preferences

| Preference | Behavior |
|---|---|
| Target | QA Specialist / Senior QA Specialist, plus related QA Associate, QA Analyst, Quality Systems and Quality Compliance specialist titles |
| Industries | Pharmaceuticals, biotech, biologics, medical devices, diagnostics and related regulated life-sciences operations |
| Location | USA and explicitly US-eligible or worldwide remote roles |
| Work style | On-site, hybrid and remote included |
| Experience | Entry through senior specialists; no five-year ceiling |
| Sponsorship | No filter: jobs with sponsorship, without sponsorship and with unspecified policies remain eligible |
| Exclusions | Software QA/test automation, internships, management and unrelated industries |

A job must have a relevant title, life-sciences context and regulated-quality responsibilities in its title/description. Call-center QA is excluded when the only industry evidence is a pharmaceutical client in company boilerplate. A bare "Remote" location without US eligibility evidence is omitted. Sponsorship text is not interpreted as a promise of sponsorship.

## Run a search

1. Open this repository's **Actions** tab. If GitHub has disabled workflows on the new fork, enable them.
2. Select **Find US Quality Assurance Specialist jobs**.
3. Click **Run workflow**, choose **main**, and run it. The optional discovery checkbox revalidates/adds supported public employer feeds.
4. Open the completed run's **Summary** for a job table with application links.
5. Download **qa-specialist-jobs-<run ID>** under Artifacts for the full CSV, JSON, summary and source-health reports.

The first completed search checks the **previous seven days**. Subsequent searches check postings with usable source timestamps after the previous completed search. Change **first_run_lookback_days** in [job_profile.yml](job_profile.yml) before your first run to use a different initial window.

The workflow is **manual**. It does not run hourly or send emails. No API keys or SMTP secrets are needed. Its **contents: write** permission saves search history to this repository.

## Change your requirements

Edit [job_profile.yml](job_profile.yml):

- **title_functions** and **title_levels** control the job-title matches.
- **life_sciences_terms** establish industry relevance.
- **required_quality_terms** establish regulated QA responsibilities.
- **quality_terms** increase relevance scores for CAPA, batch review, deviations, audits and related work.
- **max_experience_years: null** keeps all experience levels eligible.
- **himalayas_queries** and **smartrecruiters_queries** control source searches.
- **include_fortune500: false** keeps optional discovery focused on the configured life-sciences employers.

Results are ranked by QA relevance and recency. Experience classifications describe the ad; they do not screen out senior specialists.

## Employer coverage

The initial configuration includes **12 employer feeds**, whose public APIs responded successfully on November 25, 2026:

Genezen, ProKidney, Legend Biotech, Beam Therapeutics, Prime Medicine, Interpath Laboratory, Orca Bio, eGenesis, AbbVie, SGS, LGC Group and Eurofins.

The larger SmartRecruiters feeds are searched with QA terms and paginated, rather than reading only their first 200 unrelated vacancies. Jobicy, Working Nomads and Himalayas provide supplementary attributed listings. AI/new-graduate GitHub trackers are no longer added to the active search.

Add employer feeds to [boards.yml](boards.yml), or official careers pages to [career_pages.yml](career_pages.yml) and run optional discovery. Supported adapters: Greenhouse, Lever, Ashby and SmartRecruiters.

This is a focused starting list, not every US employer. Workday, Oracle and custom portals need additional adapters; companies such as Foundation Medicine are not claimed as integrated. A working API does not guarantee a matching opening.

## Freshness and limitations

- Employer timestamps and third-party posting claims are labeled separately. **Himalayas reports update time**, which may describe an older job.
- Undated jobs are excluded from the time-window report. Some Lever feeds do not expose creation dates.
- Application pages are checked before inclusion. Blocked or uncertain pages are omitted; availability can change later.
- Partial source failures appear in the Summary and **feed_health.json**. A completed partial scan advances the checkpoint, so failed feeds may have gaps. If every source fails, the checkpoint is preserved and the workflow reports failure.
- Jobicy uses a minimum one-hour cache interval. Cached results may lag a new posting.
- **qa_jobs.sqlite3** stores this fork's scan checkpoint and job history. It is separate from the upstream AI/data database.
- Search history and source caches are committed in the fork. Do not put credentials or private résumé information in tracked files.
- The legacy **Send test email** workflow is separate and only runs if manually selected and configured. It is not part of this finder.

## Local validation

Use Python 3.12:

    python -m venv .venv
    .venv/bin/python -m pip install -r requirements.txt
    .venv/bin/python -m unittest discover -s tests -v
    .venv/bin/python on_demand.py
