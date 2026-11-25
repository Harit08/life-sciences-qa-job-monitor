"""Match US life-sciences QA specialist roles using the editable job profile."""
import re
from pathlib import Path
import yaml

PROFILE = yaml.safe_load(Path(__file__).with_name("job_profile.yml").read_text(encoding="utf-8"))


def phrases(items):
    """Match whole phrases while allowing punctuation between their words."""
    return re.compile(
        r"\b(?:" + "|".join(r"[\s,./()_-]+".join(map(re.escape, item.split())) for item in items) + r")\b",
        re.I,
    )


FUNCTION = phrases(PROFILE["title_functions"])
LEVEL = phrases(PROFILE["title_levels"])
EXCLUDED_TITLE = phrases(PROFILE["excluded_title_terms"])
DOMAIN = phrases(PROFILE["life_sciences_terms"])
QUALITY = phrases(PROFILE["quality_terms"])
REGULATED_QUALITY = phrases(PROFILE["required_quality_terms"])
SENIOR = re.compile(r"\b(?:senior|sr[.]?|lead|principal|staff)\b", re.I)
YEARS = re.compile(
    r"(?<!\d)(\d{1,2})(?:\s*(?:[-–—]|to)\s*(\d{1,2}))?\s*\+?\s*"
    r"(?:years?|yrs?)\s+(?:of\s+)?(?:(?:relevant|professional|related|industry|work|"
    r"pharmaceutical|biotech|GMP|quality|assurance)\s+){0,5}experience\b",
    re.I,
)


def target_title(title):
    """Coarse title screen used before requesting an employer's full job ad."""
    title = title or ""
    return bool(FUNCTION.search(title) and LEVEL.search(title) and not EXCLUDED_TITLE.search(title))


def experience_label(title, description=""):
    """Describe experience without imposing a five-year ceiling."""
    mentions = list(YEARS.finditer(description or ""))
    years = min(int(match.group(1)) for match in mentions) if mentions else None
    # Alternative qualification paths are descriptive, not an eligibility gate.
    if SENIOR.search(title or ""):
        return "experience: senior specialist"
    if years is None:
        return "experience not specified"
    if years <= 2:
        return "experience: entry level"
    if years <= 5:
        return "experience: experienced specialist"
    return "experience: senior specialist"


def assess(title, description="", min_score=5):
    """Return (accepted, score, reasons) for QA roles in the requested industry.

    Sponsorship and work authorization text never affects matching.
    Senior specialist roles remain eligible regardless of the stated years.
    """
    title, description = title or "", description or ""
    if not target_title(title):
        return False, 0, ["outside QA specialist title target"]
    if not DOMAIN.search(title + " " + description):
        return False, 0, ["life-sciences context not established"]
    if not REGULATED_QUALITY.search(title + " " + description):
        return False, 0, ["regulated QA responsibilities not established"]
    required = [int(match.group(1)) for match in YEARS.finditer(description)]
    maximum = PROFILE.get("max_experience_years")
    if maximum is not None and required and min(required) > maximum:
        return False, 0, ["experience exceeds configured maximum"]
    score = 10
    reasons = ["QA specialist title", "life-sciences context"]
    if re.search(r"\b(?:quality assurance|qa)\b", title, re.I):
        score += 3
        reasons.append("quality assurance in title")
    signals = {match.group(0).casefold() for match in QUALITY.finditer(description)}
    if signals:
        score += min(len(signals), 5)
        reasons.append("quality systems / GMP responsibilities")
    reasons.append(experience_label(title, description))
    return score >= min_score, score, reasons


US_CODES = r"AL|AK|AZ|AR|CA|CO|CT|DE|FL|GA|HI|ID|IL|IN|IA|KS|KY|LA|ME|MD|MA|MI|MS|MN|MT|NE|NV|NH|NJ|NM|NY|NC|ND|OH|OK|OR|PA|RI|SC|SD|TN|TX|UT|VT|VA|WA|WV|WI|WY|DC"
US_STATES = (
    "Alabama|Alaska|Arizona|Arkansas|California|Colorado|Connecticut|Delaware|"
    "Florida|Georgia|Hawaii|Idaho|Illinois|Indiana|Iowa|Kansas|Kentucky|Louisiana|"
    "Maine|Maryland|Massachusetts|Michigan|Minnesota|Mississippi|Missouri|Montana|"
    "Nebraska|Nevada|New Hampshire|New Jersey|New Mexico|New York|North Carolina|"
    "North Dakota|Ohio|Oklahoma|Oregon|Pennsylvania|Rhode Island|South Carolina|"
    "South Dakota|Tennessee|Texas|Utah|Vermont|Virginia|Washington|West Virginia|"
    "Wisconsin|Wyoming|District of Columbia"
)


def us_eligible(location="", country=None):
    location = (location or "").strip()
    country = str(country or "").strip().upper()
    if country in ("US", "USA", "UNITED STATES", "UNITED STATES OF AMERICA"):
        return True
    if country and country not in ("WORLDWIDE", "GLOBAL"):
        return False
    if re.search(r"\b(?:united states|u[.]?s[.]?a?[.]?|worldwide|global|anywhere)\b", location, re.I):
        return True
    if re.search(r"\b(?:canada|united kingdom|europe|india|germany|france|australia)\b", location, re.I):
        return False
    if re.search(r",\s*(?:" + US_CODES + r")\b", location):
        return True
    if re.search(r"\b(?:" + US_STATES + r")\b", location, re.I):
        return True
    if re.search(r"\b(?:NYC|New York City|Bay Area|Silicon Valley|Atlanta|Boston|"
                 r"Chicago|Seattle|San Francisco|Austin|Dallas|Houston|Denver|Los Angeles|"
                 r"San Diego|Miami|Philadelphia|Phoenix|Raleigh|Nashville)\b", location, re.I):
        return True
    # A bare "Remote" or "North America" does not prove US eligibility.
    return False
