"""Extract structured TSMC earnings-call metrics from markdown transcripts.

Reads ../../../markdown/YYYY_QN.md (2020 onwards), produces quarterly.csv with one
row per quarter and ~30 columns covering the five management areas (五管):
財 finance, 銷 marketing/platform mix, 產 production/node mix,
人 HR keyword signals, 發 R&D / roadmap signals.
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

HERE = Path(__file__).resolve()
APP_ROOT = HERE.parents[1]
MD_DIR = APP_ROOT / "data" / "transcripts"
OUT_CSV = APP_ROOT / "data" / "quarterly.csv"

QUARTERS_FOCUS_START = 2020

MONTHS = {
    "JANUARY": 1, "FEBRUARY": 2, "MARCH": 3, "APRIL": 4,
    "MAY": 5, "JUNE": 6, "JULY": 7, "AUGUST": 8,
    "SEPTEMBER": 9, "OCTOBER": 10, "NOVEMBER": 11, "DECEMBER": 12,
}


def parse_call_date(text: str) -> str | None:
    m = re.search(
        r"\b(JANUARY|FEBRUARY|MARCH|APRIL|MAY|JUNE|JULY|AUGUST|SEPTEMBER|OCTOBER|NOVEMBER|DECEMBER)\s+(\d{1,2}),?\s+(\d{4})",
        text,
    )
    if not m:
        return None
    mon = MONTHS[m.group(1)]
    return f"{m.group(3)}-{mon:02d}-{int(m.group(2)):02d}"


RECAP_BOUNDARY = re.compile(
    r"(?:[Nn]ow,?\s+let me recap|[Tt]o recap|[Oo]n a full[- ]year basis|[Cc]oncluding 20\d{2}|[Ff]ull[- ]year recap)"
)


def quarterly_text(text: str) -> str:
    """Truncate at the annual recap so first-match regexes don't grab full-year figures."""
    m = RECAP_BOUNDARY.search(text)
    return text[: m.start()] if m else text


def parse_finance(text: str) -> dict:
    out: dict = {}
    qtext = quarterly_text(text)

    # First NN.N% near "Gross margin" — first occurrence is the actual quarterly margin.
    # 2025 Q4 transcript has typo "Growth margin" — accept either.
    m = re.search(r"[Gg](?:ross|rowth) margin[\s\S]{0,150}?(\d{2}(?:\.\d+)?)%", qtext)
    if m:
        out["gross_margin"] = float(m.group(1))

    m = re.search(r"[Oo]perating margin[\s\S]{0,150}?(\d{2}(?:\.\d+)?)%", qtext)
    if m:
        out["operating_margin"] = float(m.group(1))

    # EPS sometimes wraps to a new line: "EPS was\nTWD22.08"
    m = re.search(r"EPS was\s+TWD\s*(\d+(?:\.\d+)?)", text)
    if m:
        out["eps_twd"] = float(m.group(1))

    m = re.search(r"ROE was (\d+(?:\.\d+)?)%", text)
    if m:
        out["roe"] = float(m.group(1))

    # Quarterly revenue in USD billion — try CFO opening first, then CEO summary.
    # Q4 calls often skip the USD figure in CFO remarks; CEO usually restates it.
    m = re.search(
        r"revenue (?:increased|decreased|grew|declined|reached|was|of)[\s\S]{0,150}?(?:USD\s?\$?|\$)([\d,]+(?:\.\d+)?)\s*billion",
        qtext,
    )
    if not m:
        m = re.search(
            r"concluded our (?:first|second|third|fourth)\s+quarter\s+with revenue\s+of\s+(?:USD\s?\$?|\$)([\d,]+(?:\.\d+)?)\s*billion",
            text,
        )
    if m:
        out["revenue_usd_b"] = float(m.group(1).replace(",", ""))

    m = re.search(
        r"(?:we expect our|expect our)\s+(?:second|third|fourth|first|next)?\s*quarter revenue to be between USD\s?(\d+(?:\.\d+)?)\s+billion and USD\s?(\d+(?:\.\d+)?)\s+billion",
        text,
    )
    if m:
        out["guide_rev_low_usd_b"] = float(m.group(1))
        out["guide_rev_high_usd_b"] = float(m.group(2))

    m = re.search(
        r"gross margin is expected to be between\s+(\d+(?:\.\d+)?)%?\s+and\s+(\d+(?:\.\d+)?)%",
        text,
    )
    if m:
        out["guide_gm_low"] = float(m.group(1))
        out["guide_gm_high"] = float(m.group(2))

    m = re.search(
        r"[Oo]perating margin between\s+(\d+(?:\.\d+)?)%?\s+and\s+(\d+(?:\.\d+)?)%",
        text,
    )
    if m:
        out["guide_om_low"] = float(m.group(1))
        out["guide_om_high"] = float(m.group(2))

    m = re.search(
        r"capital expenditures (?:reached|totaled|were|amounted to|was)\s+(?:USD\s?|\$)?([\d,]+(?:\.\d+)?)\s+billion",
        text,
        re.IGNORECASE,
    )
    if m:
        out["capex_quarter_usd_b"] = float(m.group(1).replace(",", ""))

    m = re.search(
        r"capital budget (?:is expected )?(?:to be )?(?:between\s+)?(?:USD\s?\$?|\$)?(\d+(?:\.\d+)?)\s+billion\s+(?:and|to)\s+(?:USD\s?\$?|\$)?(\d+(?:\.\d+)?)\s+billion",
        text,
        re.IGNORECASE,
    )
    if m:
        out["capex_year_low_usd_b"] = float(m.group(1))
        out["capex_year_high_usd_b"] = float(m.group(2))

    m = re.search(
        r"R&D expenses (?:accounted for|to account for|to be|are expected to be)\s+(?:about\s+)?(\d+(?:\.\d+)?)%",
        text,
    )
    if m:
        out["rd_pct"] = float(m.group(1))

    m = re.search(r"effective tax rate.{0,80}?(\d+(?:\.\d+)?)%", text, re.IGNORECASE)
    if m:
        out["tax_rate"] = float(m.group(1))

    return out


PLATFORMS = {
    "hpc": r"\bHPC\b",
    "smartphone": r"\b[Ss]martphones?\b",
    "iot": r"\bIoT\b",
    "automotive": r"\b[Aa]utomotive\b",
    "dce": r"\b(?:DCE|[Dd]igital [Cc]onsumer [Ee]lectronics)\b",
}


def parse_platform_mix(text: str) -> dict:
    out: dict = {}
    sec = re.search(
        r"revenue (?:contribution )?by platform[\s\S]{50,2000}?(?:Moving on to|Now let|This concludes|balance sheet)",
        text,
    )
    section_text = sec.group(0) if sec else text

    for key, pat in PLATFORMS.items():
        m = re.search(
            pat + r"[\s\S]{0,250}?account(?:ed)? for\s+(\d+(?:\.\d+)?)%",
            section_text,
        )
        if m:
            out[f"plat_{key}_pct"] = float(m.group(1))

    return out


WORD_NUM = {
    "two": "2", "three": "3", "five": "5", "seven": "7",
    "ten": "10", "sixteen": "16", "twenty-eight": "28",
}


def normalize_node_words(text: str) -> str:
    """Replace word-form node names ("Three-nanometer") with digits ("3-nanometer").
    2025 Q4 onwards spells digits as words in technology section."""
    out = text
    for w, n in WORD_NUM.items():
        out = re.sub(rf"\b{w}-nanometer\b", f"{n}-nanometer", out, flags=re.IGNORECASE)
        out = re.sub(rf"\b{w}\s+nanometer\b", f"{n}-nanometer", out, flags=re.IGNORECASE)
    return out


def parse_node_mix(text: str) -> dict:
    """Wafer-revenue share per process node. Format varies across years:
    "3-nanometer" / "3 nanometer" / "3nm" / "Three-nanometer" — normalize first."""
    text = normalize_node_words(text)
    out: dict = {}
    sec = re.search(
        r"revenue by technology[\s\S]{50,2500}?(?:Moving on to|by platform|Now let)",
        text,
    )
    section_text = sec.group(0) if sec else text

    # "5-nanometer", "5 nanometer", "5nm" all appear across years
    nm = r"(?:[-\s]nanometer|nm)"
    verb = r"(?:contributed(?:\s+to)?|was|accounted for|came in at)"

    cm = re.search(
        rf"(\d+){nm}\s+and\s+(\d+){nm}\s+accounted for\s+(\d+(?:\.\d+)?)%\s+and\s+(\d+(?:\.\d+)?)%",
        section_text,
    )
    if cm:
        out[f"node_{cm.group(1)}nm_pct"] = float(cm.group(3))
        out[f"node_{cm.group(2)}nm_pct"] = float(cm.group(4))

    for n in ("2", "3", "5", "7", "10", "16", "28"):
        if f"node_{n}nm_pct" in out:
            continue
        m = re.search(
            rf"\b{n}{nm}\b\s*(?:process technology\s+)?{verb}\s+(\d+(?:\.\d+)?)%",
            section_text,
        )
        if m:
            out[f"node_{n}nm_pct"] = float(m.group(1))

    m = re.search(
        r"[Aa]dvanced [Tt]echnolog(?:ies|y)[\s\S]{0,250}?(?:accounted for|was)\s+(\d+(?:\.\d+)?)%\s+of\s+wafer revenue",
        section_text,
    )
    if m:
        out["node_advanced_pct"] = float(m.group(1))

    return out


HR_KEYWORDS = {
    "employee_mentions": r"\b[Ee]mployees?\b",
    "talent_mentions": r"\b[Tt]alents?\b",
    "training_mentions": r"\b[Tt]raining\b",
    "workforce_mentions": r"\b[Ww]orkforce\b",
    "safety_mentions": r"\b[Ss]afety\b",
    "culture_mentions": r"\b(?:[Cc]ulture|[Vv]alues)\b",
}


def parse_hr_signals(text: str) -> dict:
    return {k: len(re.findall(pat, text)) for k, pat in HR_KEYWORDS.items()}


RD_NODES = {
    "n7": r"\bN7\b",
    "n5": r"\bN5\b",
    "n3": r"\bN3\b",
    "n2": r"\bN2\b",
    "a16": r"\bA16\b",
    "a14": r"\bA14\b",
}


def parse_rd_signals(text: str) -> dict:
    out = {f"mentions_{k}": len(re.findall(pat, text)) for k, pat in RD_NODES.items()}
    out["mentions_arizona"] = len(re.findall(r"\bArizona\b", text))
    out["mentions_japan"] = len(re.findall(r"\bJapan(?:ese)?\b", text))
    out["mentions_germany"] = len(re.findall(r"\bGerman[yi]\b|\bDresden\b|\bESMC\b", text))
    out["mentions_ai"] = len(re.findall(r"\bAI\b|artificial intelligence", text))
    out["mentions_5g"] = len(re.findall(r"\b5G\b", text))
    return out


def quarter_sort_key(qk: str) -> tuple[int, int]:
    y, q = qk.split("_")
    return (int(y), int(q[1]))


def process_one(md_path: Path) -> dict:
    text = md_path.read_text(encoding="utf-8")
    qk = md_path.stem
    y, q = qk.split("_")
    row: dict = {
        "quarter_key": qk,
        "year": int(y),
        "quarter": q,
        "word_count": len(text.split()),
    }
    row["call_date"] = parse_call_date(text)
    row.update(parse_finance(text))
    row.update(parse_platform_mix(text))
    row.update(parse_node_mix(text))
    row.update(parse_hr_signals(text))
    row.update(parse_rd_signals(text))
    return row


def main() -> None:
    rows: list[dict] = []
    for p in sorted(MD_DIR.glob("*.md")):
        try:
            year = int(p.stem.split("_")[0])
        except (ValueError, IndexError):
            continue
        if year < QUARTERS_FOCUS_START:
            continue
        rows.append(process_one(p))

    rows.sort(key=lambda r: quarter_sort_key(r["quarter_key"]))

    seen: set[str] = set()
    all_keys: list[str] = []
    for r in rows:
        for k in r:
            if k not in seen:
                seen.add(k)
                all_keys.append(k)

    OUT_CSV.parent.mkdir(exist_ok=True, parents=True)
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=all_keys)
        w.writeheader()
        w.writerows(rows)

    print(f"Wrote {len(rows)} rows x {len(all_keys)} cols -> {OUT_CSV}")
    print("\nCoverage (% non-null per column):")
    skip = {"quarter_key", "year", "quarter", "call_date", "word_count"}
    for k in all_keys:
        if k in skip:
            continue
        non_null = sum(1 for r in rows if r.get(k) not in (None, ""))
        pct = 100.0 * non_null / len(rows) if rows else 0.0
        print(f"  {k:28s} {pct:5.1f}%  ({non_null}/{len(rows)})")


if __name__ == "__main__":
    main()
