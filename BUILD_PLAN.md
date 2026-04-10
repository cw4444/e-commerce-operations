# MVP Build Plan

This prototype demonstrates how a junior e-commerce lead workflow can be partially automated with sample data and lightweight analysis.

## Scope

The MVP covers five repeatable areas:

1. Performance monitoring
2. Listing audits
3. Competitor tracking
4. Review analysis
5. Weekly summary generation

## Data Sources

The prototype uses sample data structured like the inputs a real operator would receive:

- Weekly sales, conversion, account health, and stockout metrics
- Listing quality scores, image counts, keyword gaps, and compliance flags
- Competitor prices, ratings, and review counts
- Free-text customer review samples

In a production version, those inputs would come from:

- Marketplace reports
- BI dashboards or warehouse tables
- Listing export files
- Competitor monitoring feeds
- Customer review exports or support transcripts

## Tools

The current MVP uses only standard Python libraries:

- `json` for loading sample data
- `statistics` for simple baselines and benchmarks
- `pathlib` for file output
- `dataclasses` for structured alerts

This keeps the demo easy to run and believable without infrastructure overhead.

## Workflow

1. Load sample data.
2. Compare current week metrics against the prior week.
3. Flag anomalies in sales, conversion, account health, and stockouts.
4. Audit each listing for quality and compliance signals.
5. Compare competitor pricing and rating signals.
6. Extract common review themes.
7. Generate a weekly summary with prioritized next actions.
8. Write the result to markdown files for easy review.

## What Is Automated

- Repetitive monitoring
- Pattern detection
- Audit checklisting
- Comparison work
- First-draft reporting

## What Remains Human-Led

- Pricing approval
- Compliance escalation
- Tradeoff decisions
- Cross-functional coordination
- Final sign-off

## Why This Is Credible

The MVP does not pretend to replace the role. It shows how one operator can spend less time checking spreadsheets manually and more time making the decisions that actually require judgment.
