# Design decisions

[Project](../README.md) · [Architecture](architecture.md) · [Code tour](code-tour.md)

## A metric needs compatible dimensions

A combined store/ad-spend table has daily grain. Product or campaign attribution cannot be invented by joining unrelated cuts. [Inspect the source](../evidence/E32.md).

## Reconcile economic identities

The dbt controls compare row-level components and totals, with explicit treatment of tax, edited orders and exclusions. [Inspect the source](../evidence/E31.md).

## Distinguish absence from zero

A metric requiring a missing source remains unavailable. A missing investment value is not silently converted into zero. [Inspect the source](../evidence/E32.md).

## Test before publishing

The runner gates known data-quality failures before publication. That gate does not make subsequent BigQuery copies atomic under infrastructure failure. [Inspect the source](../evidence/E33.md).

## Keep the MCP boundary explicit

Account-scoped inventory fails closed; OAuth/PKCE and typed schemas govern the edge. The coherence demo does not test authentication. [Inspect the source](../evidence/E22.md).

## Handle host schema projection

Each anyOf branch receives a self-contained object schema so a host projecting the union preserves the requested analysis fields. [Inspect the source](../evidence/E25.md).

