# Data Platform and MCP

**From business data to analysis in Claude and ChatGPT**

*A Chals AI case study — built by Ignacio Soler.*

<a id="the-project"></a>

I built the data platform behind Chals AI: connecting business systems, cleaning and modeling their data, and making it available to AI assistants through MCP. The platform is active with two brands and also supports my internal development and side projects.

I built this project end to end on my own, using AI tools for all programming. My work covered product definition, technical decisions, implementation, integration and validation.

[See the MCP workflow](#see-the-mcp-workflow) · [Explore the implementation](#explore-the-implementation) · [Run the component sample](#run-the-component-sample) · [Español](docs/LEEME.md)

## What I built

- Data ingestion and transformation pipelines using Fivetran, BigQuery and dbt.
- Business models, metric definitions and quality checks to support consistent analysis.
- A semantic runtime and MCP interface that make the prepared data available through Claude and ChatGPT.

**Status:** July 2026–present. **Active with two brands.** I also use the MCP in **Claude and ChatGPT**, primarily for internal development, exploration and hobby projects.

Usage reported by the founder on 15 October 2026.

## See the MCP workflow

A wine-business workflow: **ERP → BigQuery → dbt → Chals AI MCP → Claude**. The four screenshots follow one conversation, from sales analysis and receivables aging to Excel and a product report. Published with synthetic data and anonymized names.

| 1. Sales | 2. Receivables aging |
|---|---|
| [![Sales by company and customer](docs/carousel/01-sales.jpg)](docs/carousel/01-sales.jpg) | [![Receivables aging and upcoming due dates](docs/carousel/02-receivables-aging.jpg)](docs/carousel/02-receivables-aging.jpg) |
| 3. Excel | 4. Product report |
| [![Excel with filters and charts](docs/carousel/03-excel.jpg)](docs/carousel/03-excel.jpg) | [![Sales report by wine, brand and channel](docs/carousel/04-product-report.jpg)](docs/carousel/04-product-report.jpg) |

[View all four slides at full size](docs/mcp-carousel.md) · [Original LinkedIn post](https://lnkd.in/p/ePyCxKwB) · [Image provenance](docs/carousel/manifest.json).

### Internal use: Chals Channel

For this side project, I combined multiple datasets of LinkedIn profiles and published content, then handled ingestion, cleaning, normalization, modeling and quality checks. I explore the prepared data through the same MCP in Claude and ChatGPT for internal analysis and development.

![Data Platform and MCP illustrated architecture](docs/overview.svg)

## Explore the implementation

The runnable component contains the original semantic profile-coherence gate. Selected source excerpts document the wider work: dbt models, data publishing, SQL validation, OAuth and MCP.

| Entry | What to look at |
|---|---|
| [profile_coherence.py](source/profile_coherence.py) | Original executable component |
| [demo.py](demo.py) | Synthetic fixtures and 5 checked behaviors |
| [Architecture](docs/architecture.md) | The wider system and the sample boundary |
| [Design decisions](docs/decisions.md) | Tradeoffs with source links |
| [Code tour](docs/code-tour.md) | 18 selected excerpts from the wider construction |
| [Provenance](provenance.json) | Original paths, commits, hashes and documented redactions |

**Stack across the project:** Fivetran · BigQuery · dbt · Python · Parquet / DuckDB · MCP · OAuth / PKCE.

This public case study includes selected original code and an isolated runnable sample with synthetic data. Production integrations and customer data remain private. Original paths, commits, hashes and redactions are recorded in [provenance.json](provenance.json).

<a id="run-the-sample"></a>

## Run the component sample

Run the original semantic profile-coherence gate locally with synthetic data. Requires **Python 3.10+**, with no package installation or account setup.

```sh
git clone https://github.com/nasoler123/data-platform-mcp.git
cd data-platform-mcp
python3 -I demo.py
python3 verify.py
```

Expected observations:

- A coherent daily store-and-ad profile passes.
- Adding an unsupported product grain to its combined metric is rejected.
- Missing references, duplicate concepts and unsupported formula operations are rejected.

The sample runs offline and rejects network connections and external subprocesses. `verify.py` checks local links, instruction parity, the source hash, credential patterns and the recorded results of the component checks. [Recorded local results](verification.json).

## More from Chals AI

These projects cover my work across business automation, financial software, AI agents and data infrastructure.

[Financial Modeling SaaS](https://github.com/nasoler123/financial-modeling-saas) · [AI Agent Harness](https://github.com/nasoler123/ai-agent-harness) · [Invoice Automation](https://github.com/nasoler123/invoice-automation)

[Ignacio Soler](https://github.com/nasoler123) · [LinkedIn](https://www.linkedin.com/in/ignacio-soler-esteban/)
