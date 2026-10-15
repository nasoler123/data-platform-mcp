# Data Platform and MCP

Business metrics with explicit grain, source meaning and execution boundaries.

[Watch the frontend](#watch-the-frontend) · [Run the sample](#run-the-sample) · [Architecture](docs/architecture.md) · [Design decisions](docs/decisions.md) · [Code tour](docs/code-tour.md) · [Español](docs/LEEME.md)

## Watch the frontend

A guided demo of the earlier data-and-automation frontend, with synthetic data and a scripted chat. It illustrates that interface; the warehouse, semantic runtime and MCP implementation are documented below.

### Data and automation interface · 60s

https://github.com/user-attachments/assets/71898e21-c52d-4f60-90b4-336e08bea58b

[Open the full-screen demo](https://chalsai.com/demo.html?script=data-pipelines&utm_source=github&utm_medium=portfolio&utm_campaign=data-platform-mcp) · [Download MP4](docs/demos/data-pipelines.mp4)

[Media provenance](docs/demos/manifest.json).

![Data Platform and MCP illustrated architecture](docs/overview.svg)

## The project

An apparently plausible metric can be wrong because its pieces have different grain, filters, source definitions or ownership. An agent must respect those constraints before turning a question into a result.

**My work.** I connected source systems, built and checked curated models, defined base and derived business metrics, and exposed governed analysis through a semantic runtime and MCP. The stack uses BigQuery as the authoritative warehouse and Parquet/DuckDB as derived serving. I led the product and technical construction, using AI-assisted development alongside integration and verification.

**Period.** July–October 2026.

**Project outcome.** Approximately five data / BI clients in total, according to the founder. This is declared adoption, not a client count inferred from repository folders.

## What you can inspect here

The executable sample runs the original semantic profile-coherence gate against synthetic dictionaries. dbt SQL, publishing, SQL checks and OAuth/MCP behavior are source excerpts. It does not connect to Fivetran, BigQuery or a live MCP.

| Entry | What to look at |
|---|---|
| [profile_coherence.py](source/profile_coherence.py) | Original executable component |
| [demo.py](demo.py) | Synthetic fixtures and 5 checked behaviors |
| [Architecture](docs/architecture.md) | The wider system and the sample boundary |
| [Design decisions](docs/decisions.md) | Tradeoffs with source links |
| [Code tour](docs/code-tour.md) | 18 selected excerpts from the wider construction |
| [Provenance](provenance.json) | Original paths, commits, hashes and documented redactions |

## Run the sample

Requires **Python 3.10+**, with no package installation or account setup.

```sh
git clone https://github.com/nasoler123/data-platform-mcp.git
cd data-platform-mcp
python3 -I demo.py
python3 verify.py
```

The sample runs offline with synthetic data; it rejects socket operations and external subprocesses. `verify.py` checks the result receipt, source hash, local links, instruction parity and credential patterns. These checks cover the published sample rather than the full production system.

Expected observations:

- A coherent daily store-and-ad profile passes.
- Adding an unsupported product grain to its combined metric is rejected.
- Missing references, duplicate concepts and unsupported formula operations are rejected.

[Recorded local results](verification.json).

## Stack in context

Fivetran · BigQuery · dbt · Python · Parquet / DuckDB · MCP · OAuth / PKCE.

The stack describes the wider construction. The executable sample uses Python's standard library; the remaining integrations appear in the code tour.

## Related work

This case belongs to the evolution of **Chals AI**, from document automation and a financial product to agent tooling and managed data infrastructure. The cases overlap; they are not four separate companies.

[Invoice Automation](https://github.com/nasoler123/invoice-automation) · [Financial Modeling SaaS](https://github.com/nasoler123/financial-modeling-saas) · [AI Agent Harness](https://github.com/nasoler123/ai-agent-harness)

[Ignacio Soler](https://github.com/nasoler123) · [LinkedIn](https://www.linkedin.com/in/ignacio-soler-esteban/)
