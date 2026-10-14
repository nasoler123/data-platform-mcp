# Code tour

[Project](../README.md) · [Architecture](architecture.md) · [Design decisions](decisions.md)

## Start with executable code

1. Read [profile_coherence.py](../source/profile_coherence.py).
2. Inspect the synthetic inputs and assertions in [demo.py](../demo.py).
3. Compare [verification.json](../verification.json) with a fresh local run.

## Selected source from the wider system

| Component | Inspect | Form |
|---|---|---|
| Derived monthly serving rollup | [Open excerpt](../evidence/E11.md) | Código |
| Account-scoped MCP inventory | [Open excerpt](../evidence/E22.md) | Código |
| OAuth and PKCE validation | [Open excerpt](../evidence/E23.md) | Código |
| Read-only SQL guard | [Open excerpt](../evidence/E24.md) | Código |
| Self-contained anyOf schemas | [Open excerpt](../evidence/E25.md) | Código |
| Managed implementation boundaries | [Open excerpt](../evidence/E27.md) | Contrato |
| Generic source profile | [Open excerpt](../evidence/E28.md) | Contrato |
| Business metric seed | [Open excerpt](../evidence/E29.md) | Contrato |
| Order model and economic components | [Open excerpt](../evidence/E30.md) | SQL |
| Row-level economic checks | [Open excerpt](../evidence/E31.md) | SQL |
| Daily grain and attribution limit | [Open excerpt](../evidence/E32.md) | SQL |
| Quality gate before publication | [Open excerpt](../evidence/E33.md) | Código |
| Versioned parity contract | [Open excerpt](../evidence/E34.md) | Contrato |
| Business workflow skill | [Open excerpt](../evidence/E35.md) | Contrato |
| Archived synthetic acceptance note | [Open excerpt](../evidence/E36.md) | Contrato |
| OAuth test setup excerpt | [Open excerpt](../evidence/E37.md) | Prueba |
| Serving test fixture excerpt | [Open excerpt](../evidence/E38.md) | Prueba |
| Historical platform architecture | [Open excerpt](../evidence/E40.md) | Contrato |

These excerpts retain original commit references. Incomplete classes, functions or integrations are presented as excerpts; the bounded executable module is separate. Redactions protect identifiers and are recorded in [provenance.json](../provenance.json).
