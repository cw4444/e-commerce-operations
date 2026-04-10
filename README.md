# E-commerce Operations MVP

This repo contains a small, credible prototype that demonstrates how a junior e-commerce lead workflow can be partially automated using sample data.

The idea is simple: based on Shane Legg's "laptop rule," a large portion of this kind of role is made up of screen-based, repeatable knowledge work. That makes it a strong candidate for AI-assisted workflows that monitor performance, audit listings, compare competitors, summarise review themes, and draft weekly ops briefs.

Built with Codex from OpenAI: [chatgpt.com/codex/cloud](https://chatgpt.com/codex/cloud)

## What it does

- Performance monitoring
- Listing audit checks
- Competitor tracking
- Review theme analysis
- Weekly summary generation
- Interactive filters and a lightweight chart for the live demo

## What is automated

- Weekly performance checks against a baseline
- Listing quality and compliance checks
- Competitor comparison across price, rating, and review count
- Review theme extraction from sample feedback
- First-draft weekly reporting

## What still needs a human

- Pricing decisions
- Tradeoff calls
- Compliance escalation
- Cross-functional coordination
- Final approval before changes go live

## Run

```bash
python demo.py
```

## Output

The script writes:

- `output/weekly_summary.md`
- `output/automation_explanation.md`

## Intent

This is a practical MVP, not a full replacement for a human operator. It is designed to show how one person with AI support can cover a large amount of the repetitive weekly workflow while keeping judgment, accountability, and coordination with the human operator.
