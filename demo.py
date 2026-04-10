from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from statistics import mean
from typing import Any


ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "sample_data.json"
OUTPUT_DIR = ROOT / "output"


@dataclass
class Alert:
    severity: str
    area: str
    message: str


def load_data() -> dict[str, Any]:
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))


def pct_change(current: float, previous: float) -> float:
    if previous == 0:
        return 0.0
    return (current - previous) / previous * 100


def rolling_baseline(values: list[float]) -> float:
    if not values:
        return 0.0
    return mean(values)


def detect_performance_alerts(perf: dict[str, Any]) -> list[Alert]:
    alerts: list[Alert] = []
    current = perf["current_week"]
    prior = perf["previous_week"]

    for metric, label, threshold in [
        ("sales", "Sales", -12),
        ("conversion_rate", "Conversion rate", -10),
        ("account_health", "Account health", -5),
    ]:
        change = pct_change(current[metric], prior[metric])
        if change <= threshold:
            alerts.append(
                Alert(
                    "High" if change <= threshold - 10 else "Medium",
                    "Performance",
                    f"{label} moved {change:.1f}% vs last week.",
                )
            )

    stockout_rate = current["stockout_days"] / 7 * 100
    if stockout_rate >= 20:
        alerts.append(
            Alert(
                "High",
                "Inventory",
                f"Stockouts affected {current['stockout_days']} of 7 days this week.",
            )
        )

    return alerts


def audit_listings(listings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for item in listings:
        issues = []
        if item["title_score"] < 80:
            issues.append(f"title score {item['title_score']}")
        if item["bullet_coverage"] < 90:
            issues.append(f"bullet coverage {item['bullet_coverage']}%")
        if item["image_count"] < 6:
            issues.append(f"only {item['image_count']} images")
        if item["compliance_flag"]:
            issues.append("compliance risk")
        if item["keyword_gap"] >= 5:
            issues.append(f"keyword gap {item['keyword_gap']}")
        if issues:
            findings.append(
                {
                    "sku": item["sku"],
                    "marketplace": item["marketplace"],
                    "issues": issues,
                    "recommendation": item["recommendation"].rstrip("."),
                }
            )
    return findings


def compare_competitors(competitors: list[dict[str, Any]], own_brand: dict[str, Any]) -> list[dict[str, Any]]:
    benchmark = {
        "price": mean([c["price"] for c in competitors]),
        "rating": mean([c["rating"] for c in competitors]),
        "review_count": mean([c["review_count"] for c in competitors]),
    }
    opportunities = []
    for c in competitors:
        if c["price"] < own_brand["price"] * 0.95:
            opportunities.append(
                {
                    "brand": c["brand"],
                    "signal": f"Lower price point at {c['price']:.2f}",
                    "response": "Check whether a bundle, promo, or margin-protected price move is justified.",
                }
            )
        if c["rating"] >= own_brand["rating"] + 0.2:
            opportunities.append(
                {
                    "brand": c["brand"],
                    "signal": f"Rating lead of {c['rating']:.1f} vs our {own_brand['rating']:.1f}",
                    "response": "Review review themes and product content to see if expectations are misaligned.",
                }
            )
    opportunities.append(
        {
            "brand": "Market benchmark",
            "signal": f"Category benchmark price {benchmark['price']:.2f}, rating {benchmark['rating']:.1f}, reviews {benchmark['review_count']:.0f}",
            "response": "Use as a weekly sanity check for pricing and positioning.",
        }
    )
    return opportunities


def summarize_reviews(reviews: list[str]) -> dict[str, Any]:
    themes = {
        "quality": ["quality", "durable", "broken", "cheap"],
        "delivery": ["delivery", "late", "shipping", "arrived"],
        "fit": ["size", "fit", "too small", "too large"],
        "instructions": ["instructions", "manual", "assembly"],
    }
    counts = {k: 0 for k in themes}
    for review in reviews:
        text = review.lower()
        for theme, keywords in themes.items():
            if any(keyword in text for keyword in keywords):
                counts[theme] += 1
    top_themes = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    return {
        "counts": counts,
        "top_themes": [theme for theme, count in top_themes if count > 0],
        "sample_quotes": reviews[:3],
    }


def weekly_summary(data: dict[str, Any]) -> str:
    perf_alerts = detect_performance_alerts(data["performance"])
    listing_findings = audit_listings(data["listings"])
    competitor_opps = compare_competitors(data["competitors"], data["our_brand"])
    review_summary = summarize_reviews(data["reviews"])

    current = data["performance"]["current_week"]
    previous = data["performance"]["previous_week"]

    lines = []
    lines.append("# Weekly E-commerce Ops Summary")
    lines.append("")
    lines.append(f"Reporting week: {data['reporting_week']}")
    lines.append("")
    lines.append("## Headline")
    lines.append(
        f"Sales were {current['sales']:,} vs {previous['sales']:,} last week ({pct_change(current['sales'], previous['sales']):.1f}%). "
        f"Conversion was {current['conversion_rate']:.2f}% and account health was {current['account_health']}."
    )
    lines.append("")
    lines.append("## Alerts")
    if perf_alerts:
        for alert in perf_alerts:
            lines.append(f"- [{alert.severity}] {alert.area}: {alert.message}")
    else:
        lines.append("- No material performance alerts.")
    lines.append("")
    lines.append("## Listing Audit")
    if listing_findings:
        for item in listing_findings:
            lines.append(
                f"- {item['sku']} ({item['marketplace']}): {', '.join(item['issues'])}. Recommended action: {item['recommendation']}."
            )
    else:
        lines.append("- No listing issues detected.")
    lines.append("")
    lines.append("## Competitor Watch")
    for opp in competitor_opps:
        lines.append(f"- {opp['brand']}: {opp['signal']}. {opp['response']}")
    lines.append("")
    lines.append("## Review Themes")
    lines.append(
        f"- Top themes: {', '.join(review_summary['top_themes']) if review_summary['top_themes'] else 'none identified'}."
    )
    lines.append(f"- Sample review volume analysed: {len(data['reviews'])}.")
    lines.append("")
    lines.append("## Recommended Next Actions")
    lines.append("- Validate the stockout cause and decide whether to protect rank with a tactical replenishment or price change.")
    lines.append("- Fix the two lowest-scoring listings and re-run the audit after updates.")
    lines.append("- Review competitor price and rating gaps before approving any pricing move.")
    lines.append("- Escalate compliance risk items to the marketplace owner before publishing changes.")
    return "\n".join(lines)


def explanation_page() -> str:
    return """# What This MVP Automates

This prototype shows how one operator can cover a large part of a junior e-commerce lead workflow with AI-assisted monitoring and structured review.

## Automated

- Performance monitoring against weekly baselines
- Detection of unusual sales, conversion, stock, and account health changes
- Listing audits for titles, bullets, images, keyword gaps, and basic compliance drift
- Competitor tracking using price, rating, and review benchmarks
- Review theme extraction from sample customer feedback
- Weekly summary generation with prioritized actions

## Still Requires Human Judgment

- Approving pricing moves and margin tradeoffs
- Deciding whether a compliance issue is safe to fix immediately or needs escalation
- Choosing which findings matter strategically versus noise
- Coordinating with supply chain, marketing, support, and marketplace owners
- Signing off on listing changes before they go live
- Handling brand-specific nuance, exceptions, and internal politics

## Human Responsibility

The human remains accountable for commercial decisions, cross-functional alignment, and final approval. The automation prepares the evidence, highlights risk, and keeps the workflow moving, but it does not replace ownership.

## Practical Value

The MVP reduces manual checking, speeds up weekly reporting, and makes the operator more consistent. It does not replace the role; it compresses the repetitive work so a single person can spend more time on decisions, coordination, and follow-through.
"""


def main() -> None:
    data = load_data()
    OUTPUT_DIR.mkdir(exist_ok=True)

    report = weekly_summary(data)
    explanation = explanation_page()

    (OUTPUT_DIR / "weekly_summary.md").write_text(report, encoding="utf-8")
    (OUTPUT_DIR / "automation_explanation.md").write_text(explanation, encoding="utf-8")

    print(report)
    print()
    print(f"Wrote {OUTPUT_DIR / 'weekly_summary.md'}")
    print(f"Wrote {OUTPUT_DIR / 'automation_explanation.md'}")


if __name__ == "__main__":
    main()
