#!/usr/bin/env python3
"""Coherencia de un perfil: que ningún análisis pueda caerse por su estructura.

El motor de análisis exige que un filtro o un desglose resuelva en la tabla de
CADA métrica de la vista. La primera copia real (21/9/2026) lo demostró por las
malas: «Ventas netas» mezclaba `lineas_pedido` (con producto) y `pedidos` (sin
él), y todo análisis filtrado por producto murió con BI_FILTER_UNRESOLVED.

Estas reglas lo impiden por construcción, antes de publicar:

  1. Toda tabla que declara un ámbito lleva TODAS sus columnas (con esquemas).
  2. Todo ámbito citado por una tabla está declarado en `ambitos`.
  3. Cada driver base cita una tabla del manifiesto, y su fecha, su expresión y
     las columnas de su filtro existen en esa tabla (con esquemas).
  4. Cada derivado cita drivers que existen, sin ciclos, con una fórmula bien
     formada: `{ref: <métrica>}`, `{valor: <número>}` (constante, no es una
     referencia) u `{op: add|sub|mul|div, izquierda, derecha}`.
  5. Todas las tablas que intervienen en un derivado comparten, al menos, los
     ámbitos de la tabla que lo aloja: lo que se puede cortar en el derivado se
     puede cortar en cada una de sus piezas.

Desde el perfil 3.0 (una métrica por concepto, ADR-0021 de chals-ai):

  6. Metadatos: toda métrica lleva `familia`, `fuente`, `atribucion` y `unidad`
     con valores permitidos. `fuente` es la de una fuente del manifiesto
     (`origen.fuente`, `origenes.<servicio>.fuente`) o una de varias
     (`anuncios`, `shopify_y_anuncios`); una métrica de una fuente de anuncios
     vive en una tabla que se construye desde ella. Una métrica `combinada`
     derivada se apoya al menos en una base de la tienda y en una de anuncios o
     combinada; una base `combinada` vive en una tabla que cruza la tienda con
     la publicidad (`depende_de` y `origenes_alguno`), como «Inversión
     publicitaria en la tienda» (3.3.0).
  7. Un concepto, una vez: no hay dos drivers base con la misma agregación,
     expresión y filtro (la repetición por nivel de 2.x), y ningún nombre se
     repite entre base y derivados.
  8. Orden: un derivado solo cita métricas definidas antes en el fichero (las
     bases primero). Core los crea en ese orden.
  9. Exploración: ninguna métrica se aloja en una tabla con `exploracion: true`
     ni la usa como pieza.
 10. `reemplaza`: los nombres antiguos que cita una métrica no son nombres
     vigentes de la semilla y no se repiten entre métricas.

Sin esquemas (modo estático) se comprueba todo menos 1 y la parte de 3 que
necesita columnas: es el gate de `bin/chals-client publish-profile`. Con los
esquemas de las tablas construidas (`runner/validar_perfil.py`) se comprueba
todo.

Uso:  python3 runner/coherencia.py profiles/<perfil>
"""

from __future__ import annotations

import math
import re
import sys
from pathlib import Path

PALABRAS_SQL = {
    "and", "or", "not", "is", "null", "true", "false", "in", "like", "between",
    "case", "when", "then", "else", "end", "cast", "as", "date", "timestamp",
}
OPERACIONES = {"add", "sub", "mul", "div"}
FAMILIAS = {"tienda", "anuncios", "combinada"}
# `fuente` de las métricas que no son de una sola fuente: de todas las
# plataformas de anuncios conectadas (3.3.0; antes `google_ads_y_meta_ads`) y
# las combinadas de tienda y anuncios.
FUENTES_DE_VARIAS = {"anuncios", "shopify_y_anuncios"}
# Las de un manifiesto que no declara las suyas (`origen.fuente`,
# `origenes.<servicio>.fuente`, desde la 3.2.1).
FUENTES_POR_DEFECTO = {"shopify", "google_ads", "meta_ads", "tiktok_ads", "amazon_ads"}
ATRIBUCIONES = {"sin_atribucion", "plataforma"}
UNIDADES = {"money", "count", "ratio"}


def columnas_de(expresion: str) -> set[str]:
    """Identificadores que una expresión o filtro SQL simple lee como columnas."""

    sin_literales = re.sub(r"'(?:[^']|'')*'", " ", str(expresion or ""))
    sin_funciones = re.sub(r"\b[a-zA-Z_][a-zA-Z0-9_]*\s*\(", " ", sin_literales)
    return {
        token
        for token in re.findall(r"\b[a-zA-Z_][a-zA-Z0-9_]*\b", sin_funciones)
        if token.lower() not in PALABRAS_SQL and not token.isdigit()
    }


def normalizar_sql(texto: str) -> str:
    """Forma canónica de una expresión o filtro para comparar definiciones.

    Espacios (también alrededor de operadores: `a=b` es `a = b`) y mayúsculas
    fuera de los literales no cuentan; un filtro que es solo una conjunción de
    condiciones (sin OR ni paréntesis) no depende del orden de sus condiciones.
    """

    partes = re.split(r"('(?:[^']|'')*')", str(texto or ""))
    plano = "".join(
        p if p.startswith("'")
        else re.sub(r"\s*(<=|>=|!=|<>|[=<>+\-*/(),])\s*", r"\1", re.sub(r"\s+", " ", p.lower()))
        for p in partes
    ).strip()
    fuera = re.sub(r"'(?:[^']|'')*'", "''", plano)
    if "(" in fuera or re.search(r"\bor\b", fuera):
        return plano
    return " and ".join(sorted(c.strip() for c in re.split(r"\s+and\s+", plano)))


def es_constante(nodo: object) -> bool:
    valor = nodo.get("valor") if isinstance(nodo, dict) else None
    return (isinstance(valor, (int, float)) and not isinstance(valor, bool)
            and math.isfinite(valor))


def errores_formula(nodo: object) -> list[str]:
    """Qué está mal formado en una fórmula (lista vacía = bien formada)."""

    if not isinstance(nodo, dict):
        return [f"nodo {nodo!r} no es un mapa"]
    if set(nodo) == {"ref"}:
        return [] if isinstance(nodo["ref"], str) and nodo["ref"] else [f"ref vacía o no textual: {nodo!r}"]
    if set(nodo) == {"valor"}:
        return [] if es_constante(nodo) else [f"constante no numérica o no finita: {nodo!r}"]
    if "op" in nodo:
        errores = [] if nodo["op"] in OPERACIONES else [f"operación desconocida '{nodo['op']}'"]
        if set(nodo) != {"op", "izquierda", "derecha"}:
            errores.append(f"una operación lleva op, izquierda y derecha, no {sorted(nodo)}")
        return errores + errores_formula(nodo.get("izquierda")) + errores_formula(nodo.get("derecha"))
    return [f"nodo sin ref, valor ni op: {nodo!r}"]


def fuentes_permitidas(manifest: dict) -> tuple[set[str], dict[str, str]]:
    """Valores válidos de `fuente` y, de cada fuente de anuncios, su servicio.

    Salen del manifiesto (`origen.fuente` y `origenes.<servicio>.fuente`); si no
    declara ninguna, las de siempre. Más las de varias fuentes.
    """

    origenes = manifest.get("origenes") or {}
    de_origenes = {str(o["fuente"]): servicio for servicio, o in origenes.items()
                   if isinstance(o, dict) and o.get("fuente")}
    principal = (manifest.get("origen") or {}).get("fuente")
    propias = set(de_origenes) | ({str(principal)} if principal else set())
    return (propias or FUENTES_POR_DEFECTO) | FUENTES_DE_VARIAS, de_origenes


def revisar(
    manifest: dict,
    semilla: dict,
    esquemas: dict[str, set[str]] | None = None,
) -> list[str]:
    """Incoherencias del perfil. Lista vacía = coherente.

    `esquemas` son las columnas de las tablas construidas; una tabla ausente se
    trata como omitida (su origen no existe) y sus drivers no se comprueban,
    igual que Core no los siembra.
    """

    problemas: list[str] = []
    ambitos: dict[str, list[str]] = {
        str(k): list(v or []) for k, v in (manifest.get("ambitos") or {}).items()
    }
    tablas = {t["nombre"]: t for t in manifest.get("tablas") or []}
    ambitos_de = {nombre: set(t.get("ambitos") or []) for nombre, t in tablas.items()}
    exploracion = {nombre for nombre, t in tablas.items() if t.get("exploracion") is True}
    for nombre, t in tablas.items():
        if "exploracion" in t and not isinstance(t["exploracion"], bool):
            problemas.append(f"{nombre}: `exploracion` tiene que ser true o false, no {t['exploracion']!r}")

    # 2 y 1: ámbitos declarados y completos.
    for nombre, declarados in ambitos_de.items():
        for ambito in sorted(declarados - set(ambitos)):
            problemas.append(f"{nombre}: declara el ámbito '{ambito}', que no existe en `ambitos`")
        if esquemas is not None and nombre in esquemas:
            for ambito in sorted(declarados & set(ambitos)):
                faltan = [c for c in ambitos[ambito] if c not in esquemas[nombre]]
                if faltan:
                    problemas.append(
                        f"{nombre}: declara el ámbito '{ambito}' y le faltan {', '.join(faltan)}"
                    )

    construida = (lambda n: n in esquemas) if esquemas is not None else (lambda n: True)
    lista_base = list(semilla.get("base") or [])
    lista_derivados = list(semilla.get("derivados") or [])
    base = {d["nombre"]: d for d in lista_base}
    derivados = {d["nombre"]: d for d in lista_derivados}

    # 7 (nombres): cada nombre, una vez entre base y derivados.
    vistos: set[str] = set()
    for d in lista_base + lista_derivados:
        if d["nombre"] in vistos:
            problemas.append(f"'{d['nombre']}': el nombre se repite en la semilla")
        vistos.add(d["nombre"])

    # 3: drivers base.
    for nombre, d in base.items():
        tabla = d.get("tabla")
        if tabla not in tablas:
            problemas.append(f"driver '{nombre}': la tabla '{tabla}' no está en el manifiesto")
            continue
        if tabla in exploracion:
            problemas.append(f"driver '{nombre}': se aloja en {tabla}, que es de exploración (sin métricas gobernadas)")
        if esquemas is None or not construida(tabla):
            continue
        usadas = {d.get("fecha", "")} | columnas_de(d.get("expresion", "")) | columnas_de(d.get("filtro", ""))
        faltan = sorted(c for c in usadas if c and c not in esquemas[tabla])
        if faltan:
            problemas.append(f"driver '{nombre}': {tabla} no tiene {', '.join(faltan)}")

    # 7 (definiciones): la misma cifra no vive dos veces, ni por nivel.
    definiciones: dict[tuple[str, str, str], str] = {}
    for d in lista_base:
        clave = (str(d.get("agregacion") or "").lower(), normalizar_sql(d.get("expresion", "")),
                 normalizar_sql(d.get("filtro") or "TRUE"))
        if clave in definiciones:
            otro = base.get(definiciones[clave]) or {}
            donde = (f"en {d.get('tabla')} y {otro.get('tabla')}" if otro.get("tabla") != d.get("tabla")
                     else f"en la misma tabla {d.get('tabla')}")
            problemas.append(
                f"driver '{d['nombre']}': es la misma cifra que '{definiciones[clave]}' ({donde}): "
                "un concepto se define una vez y se corta por sus dimensiones"
            )
        else:
            definiciones[clave] = d["nombre"]

    # 4, 8 y 5: derivados.
    orden = {d["nombre"]: i for i, d in enumerate(lista_derivados)}
    for nombre, d in derivados.items():
        for error in errores_formula(d.get("formula")):
            problemas.append(f"derivado '{nombre}': fórmula mal formada: {error}")
        for ref in refs(d.get("formula") or {}):
            if ref in derivados and orden[ref] >= orden[nombre]:
                problemas.append(f"derivado '{nombre}': cita '{ref}', que se define después (o es él mismo)")

    def piezas(nombre: str, visto: tuple[str, ...] = ()) -> set[str] | None:
        if nombre in visto:
            problemas.append(f"derivado '{visto[0]}': ciclo en {' -> '.join(visto + (nombre,))}")
            return None
        if nombre in base:
            return {nombre}
        if nombre not in derivados:
            problemas.append(f"derivado '{visto[-1] if visto else nombre}': cita '{nombre}', que no existe")
            return None
        resultado: set[str] = set()
        for ref in refs(derivados[nombre].get("formula") or {}):
            sub = piezas(ref, visto + (nombre,))
            if sub is None:
                return None
            resultado |= sub
        return resultado

    bases_de: dict[str, set[str]] = {n: {n} for n in base}
    for nombre, d in derivados.items():
        anfitriona = d.get("tabla")
        if anfitriona not in tablas:
            problemas.append(f"derivado '{nombre}': la tabla '{anfitriona}' no está en el manifiesto")
            continue
        if anfitriona in exploracion:
            problemas.append(f"derivado '{nombre}': se aloja en {anfitriona}, que es de exploración (sin métricas gobernadas)")
        bases = piezas(nombre)
        if not bases:
            continue
        bases_de[nombre] = bases
        implicadas = {base[b]["tabla"] for b in bases}
        for tabla in sorted(implicadas & exploracion):
            problemas.append(f"derivado '{nombre}': usa como pieza {tabla}, que es de exploración")
        if not all(construida(t) for t in implicadas | {anfitriona}):
            continue  # Core lo omite si falta una pieza: no es incoherente
        requeridos = ambitos_de.get(anfitriona, set())
        for tabla in sorted(implicadas):
            faltan = requeridos - ambitos_de.get(tabla, set())
            if faltan:
                problemas.append(
                    f"derivado '{nombre}': se aloja en {anfitriona} ({', '.join(sorted(requeridos))}) "
                    f"pero usa {tabla}, que no tiene el ámbito {', '.join(sorted(faltan))}: "
                    "un filtro o desglose por esas dimensiones haría caer el análisis"
                )

    # 6: metadatos de cada métrica.
    fuentes, servicio_de = fuentes_permitidas(manifest)
    permitidos = (("familia", FAMILIAS), ("fuente", fuentes), ("atribucion", ATRIBUCIONES), ("unidad", UNIDADES))
    for d in lista_base + lista_derivados:
        for clave, valores in permitidos:
            if d.get(clave) not in valores:
                problemas.append(
                    f"'{d['nombre']}': `{clave}` es {d.get(clave)!r}; tiene que ser uno de {', '.join(sorted(valores))}"
                )
        servicio = servicio_de.get(str(d.get("fuente")))
        anfitriona = tablas.get(d.get("tabla")) or {}
        if servicio and anfitriona and servicio not in (anfitriona.get("origenes_alguno") or []):
            problemas.append(
                f"'{d['nombre']}': es de la fuente {servicio} y se aloja en {d.get('tabla')}, que no se construye desde ella"
            )
        if d.get("familia") != "combinada":
            continue
        if d["nombre"] in base:
            if not (anfitriona.get("depende_de") and anfitriona.get("origenes_alguno")):
                problemas.append(
                    f"'{d['nombre']}': es una base combinada y {d.get('tabla')} no cruza la tienda con la publicidad"
                )
        elif d["nombre"] in bases_de:
            familias = {base[b].get("familia") for b in bases_de[d["nombre"]]}
            if "tienda" not in familias or not familias & {"anuncios", "combinada"}:
                problemas.append(
                    f"'{d['nombre']}': es combinada y no se apoya en una base de la tienda y otra de anuncios"
                )

    # 10: reemplaza.
    citado_por: dict[str, str] = {}
    for d in lista_base + lista_derivados:
        reemplaza = d.get("reemplaza")
        if reemplaza is None:
            continue
        if not isinstance(reemplaza, list) or not all(isinstance(r, str) and r for r in reemplaza):
            problemas.append(f"'{d['nombre']}': `reemplaza` tiene que ser una lista de nombres")
            continue
        for antiguo in reemplaza:
            if antiguo in vistos:
                problemas.append(f"'{d['nombre']}': reemplaza a '{antiguo}', que es un nombre vigente de la semilla")
            if antiguo in citado_por:
                problemas.append(
                    f"'{d['nombre']}': reemplaza a '{antiguo}', que ya reemplaza '{citado_por[antiguo]}'"
                )
            citado_por.setdefault(antiguo, d["nombre"])
    return problemas


def refs(formula: dict) -> list[str]:
    """Métricas que cita una fórmula. Las constantes no son referencias."""

    if not isinstance(formula, dict) or "valor" in formula:
        return []
    if "ref" in formula:
        return [str(formula["ref"])]
    return refs(formula.get("izquierda")) + refs(formula.get("derecha"))


def principal(argv: list[str]) -> int:
    import yaml

    if len(argv) != 2:
        print(__doc__)
        return 1
    raiz = Path(argv[1])
    manifest = yaml.safe_load((raiz / "manifest.yaml").read_text()) or {}
    semilla = yaml.safe_load((raiz / "drivers.seed.yaml").read_text()) or {}
    problemas = revisar(manifest, semilla)
    for problema in problemas:
        print(f"  INCOHERENTE  {problema}")
    if problemas:
        print(f"{len(problemas)} incoherencia(s): el perfil no se publica")
        return 1
    print(f"perfil coherente: {len(manifest.get('tablas') or [])} tablas, "
          f"{len(semilla.get('base') or [])} drivers base, {len(semilla.get('derivados') or [])} derivados")
    return 0


if __name__ == "__main__":
    sys.exit(principal(sys.argv))
