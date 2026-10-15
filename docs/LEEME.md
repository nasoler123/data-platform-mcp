# Plataforma de datos y MCP

Ingesta, BigQuery, dbt, semántica, dimensiones, métricas, serving y permisos MCP.

## Ver el workflow con MCP

Un workflow para una empresa de vinos: **ERP → BigQuery → dbt → Chals AI MCP → Claude**. Las cuatro capturas siguen una misma conversación, desde ventas y aging de cobros hasta Excel e informe de producto. Publicadas con datos sintéticos y nombres anonimizados.

| 1. Ventas | 2. Aging de cobros |
|---|---|
| [![Ventas por sociedad y cliente](carousel/01-sales.jpg)](carousel/01-sales.jpg) | [![Aging y próximos vencimientos](carousel/02-receivables-aging.jpg)](carousel/02-receivables-aging.jpg) |
| 3. Excel | 4. Informe de producto |
| [![Excel con filtros y gráficos](carousel/03-excel.jpg)](carousel/03-excel.jpg) | [![Informe por vino, marca y canal](carousel/04-product-report.jpg)](carousel/04-product-report.jpg) |

[Ver las cuatro imágenes a tamaño completo](mcp-carousel.md) · [Publicación original en LinkedIn](https://lnkd.in/p/ePyCxKwB) · [Procedencia de las imágenes](carousel/manifest.json).

## Qué demuestra este caso

Ingesta, publicación y MCP completos necesitan la infraestructura y cuentas. La demo ejecuta el gate original de coherencia sobre un perfil sintético.

**Uso actual:** La plataforma sigue activa con **dos marcas**. También la utilizo mediante su MCP en **Claude y ChatGPT**, principalmente para desarrollo interno, exploración y proyectos personales y de afición.

### Uso interno: Chals Channel

**Chals Channel** es uno de mis side projects. Reuní varias bases de datos de perfiles de LinkedIn y contenido publicado, y realicé su ingesta, limpieza, normalización, modelado y controles de calidad. Utilizo esos datos a través del MCP de Chals AI en Claude y ChatGPT para análisis y desarrollo internos.

Estado de uso comunicado por el fundador el 15 de octubre de 2026.

## Probar el componente

Requiere Python 3.10 o posterior. No necesita instalar dependencias, introducir claves ni conectar una cuenta.

```sh
python3 -I demo.py
```

La demo usa datos sintéticos y rechaza conexiones de red y subprocesos. Verifica 5 comportamientos del código original. [Resultados](../verification.json).

## Recorrido del código

[source/sample.py](../source/profile_coherence.py) es la muestra ejecutable. Módulo original completo, importado sin ejecutar su CLI ni leer perfiles externos. [Procedencia completa](../provenance.json).

- [E11 Motor analítico DuckDB/Parquet, periodos, ratios y dimensiones](../evidence/E11.md)
- [E22 MCP Analyst, permisos por llamada y aislamiento de cuenta](../evidence/E22.md)
- [E23 OAuth, PKCE, resource audience y sesión](../evidence/E23.md)
- [E24 Validación y ejecución de SQL acotado](../evidence/E24.md)
- [E25 Schemas MCP compatibles con hosts que proyectan anyOf](../evidence/E25.md)
- [E27 Discovery y modelo de implantación gestionada](../evidence/E27.md)
- [E28 Perfil 3.3.0: 32 tablas, fuentes, grano y grupos](../evidence/E28.md)
- [E29 36 métricas base y 26 derivadas, ausencias y semántica](../evidence/E29.md)
- [E30 Modelo dbt de pedidos e identidades económicas](../evidence/E30.md)
- [E31 Controles contra origen, claves, fechas e importes](../evidence/E31.md)
- [E32 Grano diario y límite explícito de atribución](../evidence/E32.md)
- [E33 dbt test, gates de publicación y deuda de atomicidad](../evidence/E33.md)
- [E34 Paridad versionada de modelos y métricas; origen real/sintético separado](../evidence/E34.md)
- [E35 Skill actual 2.0.1, propuesta, ejecución y outputs](../evidence/E35.md)
- [E36 Validaciones sintéticas y límites de aceptación](../evidence/E36.md)
- [E37 Pruebas de identidad, OAuth, scopes y catálogo](../evidence/E37.md)
- [E38 Regresiones de ratios, filtros, periodos y Top-N](../evidence/E38.md)
- [E40 Estado actual, generaciones anteriores y límites de aceptación](../evidence/E40.md)

## Alcance

Este caso conserva una selección de una construcción mayor. Los identificadores de infraestructura y clientes se han anonimizado donde corresponde; la procedencia registra las modificaciones. Para ejecutarla completa se necesitarían sus adaptadores y servicios; esta muestra no despliega ni modifica Chals AI.

[Portada en inglés](../README.md) · [Arquitectura](architecture.md) · [Decisiones](decisions.md) · [Recorrido del código](code-tour.md).
