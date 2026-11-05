#!/usr/bin/env python3
"""Assign every keyword in keywords/Dallas-Power-Washing-Keywords.xlsx to a page (target or
supporting) or to the deliberately-unused list with a one-line reason. Writes docs/keyword-plan.md.

Usage: python3 scripts/keyword_plan.py   (exit code 1 if any row is left unclassified)
"""
import sys
from collections import defaultdict
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parent.parent

# keyword -> (page URL, role)
T, S = "TARGET", "supporting"
N = "supporting (near me or national: not proof of Dallas demand)"
PLAN = {
    "power washing dallas": ("/", T), "power washing dallas tx": ("/", T),
    "pressure washing dallas": ("/", T), "pressure washing dallas texas": ("/", T), "pressure washing dallas tx": ("/", T),
    "pressure washing in dallas tx": ("/", T),
    "power washing services near me": ("/", N), "power washing in my area": ("/", N), "power washing service in my area": ("/", N),
    "pressure washing dfw": ("/service-areas/", T),
    "house washing dallas": ("/pressure-washing/", T), "house washing services near me": ("/pressure-washing/", N),
    "house washing fort worth": ("/fort-worth-pressure-washing/", S),
    "commercial pressure washing dallas": ("/power-washing/", T), "parking lot pressure washing dallas": ("/power-washing/", S),
    "driveway cleaning dallas": ("/driveway-cleaning/", T), "concrete cleaning dallas": ("/driveway-cleaning/", T),
    "how often pressure wash driveway": ("/driveway-cleaning/", N), "driveway cleaning fort worth": ("/fort-worth-pressure-washing/", S),
    "roof cleaning dallas": ("/roof-soft-wash/", T), "soft washing dallas": ("/roof-soft-wash/", T), "roof cleaning fort worth": ("/roof-soft-wash/", S),
    "fence cleaning dallas": ("/fence-cleaning/", T),
    "how much does pressure washing cost per square foot": ("/pressure-washing-cost-dallas/", T),
    "house washing cost": ("/pressure-washing-cost-dallas/", T), "how much is a pressure washing job": ("/pressure-washing-cost-dallas/", N),
    "how much is house washing": ("/pressure-washing-cost-dallas/", N),
    "how often pressure wash house": ("/how-often-to-pressure-wash-a-house/", T),
    "pressure washing fort worth": ("/fort-worth-pressure-washing/", T), "power washing fort worth": ("/fort-worth-pressure-washing/", T),
    "pressure washing frisco": ("/frisco-pressure-washing/", T), "power washing frisco": ("/frisco-pressure-washing/", T),
    "pressure washing denton": ("/denton-pressure-washing/", T), "power washing denton": ("/denton-pressure-washing/", S),
    "pressure washing carrollton": ("/carrollton-pressure-washing/", T), "power washing carrollton": ("/carrollton-pressure-washing/", S),
    "pressure washing plano": ("/plano-pressure-washing/", T), "power washing plano": ("/plano-pressure-washing/", T),
    "pressure washing arlington": ("/arlington-pressure-washing/", T), "power washing arlington": ("/arlington-pressure-washing/", S),
    "power washing mckinney": ("/mckinney-pressure-washing/", T), "pressure washing mckinney": ("/mckinney-pressure-washing/", T),
    "power washing flower mound": ("/flower-mound-pressure-washing/", T), "pressure washing flower mound": ("/flower-mound-pressure-washing/", S),
    "pressure washing addison": ("/addison-pressure-washing/", T),
    "pressure washing southlake": ("/southlake-pressure-washing/", T),
    "pressure washing keller": ("/keller-pressure-washing/", T), "pressure washing grapevine": ("/grapevine-pressure-washing/", T),
    # under 30 searches: covered on the service areas page, no page of their own
    "power washing garland": ("/service-areas/", S), "pressure washing garland": ("/service-areas/", S),
    "power washing irving": ("/service-areas/", S), "pressure washing irving": ("/service-areas/", S),
    "power washing richardson": ("/service-areas/", S), "pressure washing richardson": ("/service-areas/", S),
    "pressure washing grand prairie": ("/service-areas/", S), "pressure washing mansfield": ("/service-areas/", S),
    "pressure washing rockwall": ("/service-areas/", S), "power washing allen": ("/service-areas/", S), "pressure washing allen": ("/service-areas/", S),
    "power washing lewisville": ("/service-areas/", S), "pressure washing lewisville": ("/service-areas/", S),
    "pressure washing coppell": ("/service-areas/", S), "pressure washing mesquite": ("/service-areas/", S),
    "pressure washing rowlett": ("/service-areas/", S), "pressure washing the colony": ("/service-areas/", S),
    "pressure washing wylie": ("/service-areas/", S),
}
UNUSED = {
    "gutter cleaning dallas": "gutter cleaning is not a service of this site (brief): 390 searches, no page",
    "how much to charge for power washing": "asked by people running a washing business, not by customers",
    "how much to charge for a pressure washing job": "asked by people running a washing business, not by customers",
}


def main():
    wb = openpyxl.load_workbook(ROOT / "keywords" / "Dallas-Power-Washing-Keywords.xlsx", read_only=True)
    rows = [r for r in wb["ALL"].iter_rows(values_only=True)][1:]
    assigned, unused, missing, seen = defaultdict(list), [], [], set()
    for r in rows:
        kw = r[0]
        if not kw or kw.startswith("Source:") or kw in seen or r[1] is None:
            continue
        seen.add(kw)
        vol, sd, group = r[1], r[4], r[6]
        if kw in PLAN:
            url, role = PLAN[kw]
            assigned[url].append((kw, vol, sd, group, role))
        elif kw in UNUSED:
            unused.append((kw, vol, sd, group, UNUSED[kw]))
        else:
            missing.append(kw)
    if missing:
        print("UNCLASSIFIED:", missing)
        return 1
    n = sum(len(v) for v in assigned.values())
    out = ["# Keyword plan (Dallas Power Washing Pro, Nov 5 2026)", "",
           "Source: keywords/Dallas-Power-Washing-Keywords.xlsx (Ubersuggest, United States, read Nov 5 2026), ALL tab,",
           f"{len(seen)} unique keywords. Generated by `python3 scripts/keyword_plan.py`. Every keyword is assigned to one page",
           "or listed as deliberately unused with a reason.", "",
           "Rules applied:",
           "- Maurice's rule: 30 or more monthly searches earns a page of its own. A \"0\" means no data, not no demand.",
           "- \"Near me\" and national question terms are supporting terms only, never read as proof of Dallas demand.",
           "- Addison keeps its page on Search Console evidence although Ubersuggest shows 0.",
           "- Allen and Irving have too little data and 301 to /service-areas/. Garland, Richardson and other cities at 10 or 0",
           "  are covered honestly on /service-areas/.",
           "- Search Console showed Google testing: pressure washing dallas, power washing services, exterior wall pressure",
           "  washing, dfw pressure washing, house washing dallas, soft washing dallas, pressure washing dallas tx, residential",
           "  pressure washing. These shaped the wording of the home, /pressure-washing/, /roof-soft-wash/ and /service-areas/ pages.", "",
           f"Assigned: {n}. Unused: {len(unused)}.", "", "## Assigned keywords by page", ""]
    for url in sorted(assigned, key=lambda u: (u != "/", u)):
        out += [f"### {url}", "", "| Keyword | Volume | SD | Group | Role |", "|---|---:|---:|---|---|"]
        for kw, vol, sd, group, role in sorted(assigned[url], key=lambda x: (x[4] != T, -(x[1] or 0), x[0])):
            out.append(f"| {kw} | {vol:,} | {sd} | {group} | {role} |")
        out.append("")
    out += ["## Deliberately unused", "", "| Keyword | Volume | SD | Group | Reason |", "|---|---:|---:|---|---|"]
    for kw, vol, sd, group, why in unused:
        out.append(f"| {kw} | {vol:,} | {sd} | {group} | {why} |")
    (ROOT / "docs" / "keyword-plan.md").write_text("\n".join(out) + "\n")
    print(f"assigned {n}, unused {len(unused)}, total {len(seen)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
