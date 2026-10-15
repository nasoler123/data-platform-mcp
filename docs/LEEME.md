# Plataforma de datos y MCP

**De los datos de negocio al análisis en Claude y ChatGPT**

*Un caso de Chals AI — construido por Ignacio Soler.*

Construí la plataforma de datos de Chals AI: conecté sistemas de negocio, limpié y modelé sus datos, y los puse a disposición de asistentes de IA mediante MCP. La plataforma está activa con dos marcas y también la utilizo para desarrollo interno y proyectos personales.

Construí este proyecto yo solo, de principio a fin, utilizando herramientas de IA para toda la programación. Me encargué de la definición del producto, las decisiones técnicas, la implementación, la integración y la validación.

[Ver el workflow](#ver-el-workflow-con-mcp) · [Explorar la implementación](#explorar-la-implementación) · [Probar el componente](#probar-el-componente) · [English](../README.md)

## Qué construí

- Pipelines de ingesta y transformación con Fivetran, BigQuery y dbt.
- Modelos de negocio, definiciones de métricas y controles de calidad para apoyar análisis coherentes.
- Un motor semántico y una interfaz MCP que permiten consultar los datos preparados desde Claude y ChatGPT.

**Estado:** Julio de 2026–actualidad. **Activo con dos marcas.** También utilizo el MCP en **Claude y ChatGPT**, principalmente para desarrollo interno, exploración y proyectos personales y de afición.

Uso comunicado por el fundador el 15 de octubre de 2026.

## Ver el workflow con MCP

Un workflow para una empresa de vinos: **ERP → BigQuery → dbt → Chals AI MCP → Claude**. Las cuatro capturas siguen una misma conversación, desde ventas y aging de cobros hasta Excel e informe de producto. Publicadas con datos sintéticos y nombres anonimizados.

| 1. Ventas | 2. Aging de cobros |
|---|---|
| [![Ventas por sociedad y cliente](carousel/01-sales.jpg)](carousel/01-sales.jpg) | [![Aging y próximos vencimientos](carousel/02-receivables-aging.jpg)](carousel/02-receivables-aging.jpg) |
| 3. Excel | 4. Informe de producto |
| [![Excel con filtros y gráficos](carousel/03-excel.jpg)](carousel/03-excel.jpg) | [![Informe por vino, marca y canal](carousel/04-product-report.jpg)](carousel/04-product-report.jpg) |

[Ver las cuatro imágenes a tamaño completo](mcp-carousel.md) · [Publicación original en LinkedIn](https://lnkd.in/p/ePyCxKwB) · [Procedencia de las imágenes](carousel/manifest.json).

### Uso interno: Chals Channel

Para este proyecto personal reuní varias bases de datos de perfiles de LinkedIn y contenido publicado, y realicé su ingesta, limpieza, normalización, modelado y controles de calidad. Exploro los datos preparados a través del mismo MCP en Claude y ChatGPT para análisis y desarrollo internos.

![Arquitectura de Plataforma de datos y MCP](overview.svg)

## Explorar la implementación

El componente ejecutable contiene el control original de coherencia de perfiles semánticos. Los extractos de código documentan el trabajo más amplio: modelos dbt, publicación de datos, validación SQL, OAuth y MCP.

| Recurso | Qué puedes consultar |
|---|---|
| [profile_coherence.py](../source/profile_coherence.py) | Componente original ejecutable |
| [demo.py](../demo.py) | Datos sintéticos y 5 comportamientos comprobados |
| [Arquitectura](architecture.md) | Sistema completo y alcance de la muestra |
| [Decisiones de diseño](decisions.md) | Decisiones y referencias al código |
| [Recorrido del código](code-tour.md) | 18 extractos seleccionados de la implementación |
| [Procedencia](../provenance.json) | Rutas originales, commits, hashes y modificaciones documentadas |

<details>
<summary>Ver los extractos seleccionados</summary>

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

</details>

**Tecnologías del proyecto:** Fivetran · BigQuery · dbt · Python · Parquet / DuckDB · MCP · OAuth / PKCE.

Este caso público incluye código original seleccionado y una muestra ejecutable aislada con datos sintéticos. Las integraciones de producción y los datos de clientes se mantienen privados. Las rutas originales, commits, hashes y modificaciones se registran en [provenance.json](../provenance.json).

## Probar el componente

Ejecuta localmente el control original de coherencia de perfiles semánticos con datos sintéticos. Requiere **Python 3.10 o posterior**, sin instalar dependencias ni conectar una cuenta. Ejecuta estos comandos desde la terminal:

```sh
git clone https://github.com/nasoler123/data-platform-mcp.git
cd data-platform-mcp
python3 -I demo.py
python3 verify.py
```

Resultados esperados:

- Un perfil coherente con datos diarios de tienda y publicidad supera la validación.
- Añadir un nivel de producto no soportado a una métrica combinada se rechaza.
- Las referencias ausentes, los conceptos duplicados y las operaciones de fórmula no soportadas se rechazan.

La muestra funciona sin conexión y rechaza conexiones de red y subprocesos externos. `verify.py` comprueba enlaces locales, igualdad de instrucciones, hash del código, patrones de credenciales y coincidencia con los resultados registrados de las comprobaciones del componente. [Resultados registrados](../verification.json).

## Más proyectos de Chals AI

Estos proyectos recogen mi trabajo en automatización de negocio, software financiero, agentes de IA e infraestructura de datos.

[Financial Modeling SaaS](https://github.com/nasoler123/financial-modeling-saas) · [AI Agent Harness](https://github.com/nasoler123/ai-agent-harness) · [Invoice Automation](https://github.com/nasoler123/invoice-automation)

[Ignacio Soler](https://github.com/nasoler123) · [LinkedIn](https://www.linkedin.com/in/ignacio-soler-esteban/)
