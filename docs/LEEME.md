# Plataforma de datos y MCP

Ingesta, BigQuery, dbt, semántica, dimensiones, métricas, serving y permisos MCP.

## Ver el frontend

Demo guiada del frontend anterior de datos y automatización, con datos ficticios y una conversación con guion. Ilustra esa interfaz; la implementación del almacén, el runtime semántico y el MCP se documenta más abajo.

### Interfaz de datos y automatización · 60s

https://github.com/user-attachments/assets/71898e21-c52d-4f60-90b4-336e08bea58b

[Abrir la demo a pantalla completa](https://chalsai.com/demo.html?script=data-pipelines&utm_source=github&utm_medium=portfolio&utm_campaign=data-platform-mcp) · [Descargar MP4](demos/data-pipelines.mp4)

[Procedencia de los vídeos](demos/manifest.json).

## Qué demuestra este caso

Ingesta, publicación y MCP completos necesitan la infraestructura y cuentas. La demo ejecuta el gate original de coherencia sobre un perfil sintético.

**Resultado del proyecto:** Aproximadamente cinco clientes de data / BI, según el fundador; no se infiere adopción a partir de las demos.

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
