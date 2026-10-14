from pathlib import Path
import importlib.util
import json
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
def offline(event, args):
    if event.startswith("socket.") or event in {"subprocess.Popen", "os.system", "os.exec", "os.posix_spawn"}:
        raise RuntimeError("Demo offline: conexión o proceso externo rechazado")
sys.addaudithook(offline)
spec = importlib.util.spec_from_file_location("original_sample", HERE / "source" / "profile_coherence.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
checks = []
def check(name, condition):
    assert condition, name
    checks.append({"case": name, "passed": True})
import copy
manifest = {"origen":{"fuente":"shopify"},"origenes":{"google_ads":{"fuente":"google_ads"}},"ambitos":{"dia":["date"],"producto":["product"]},"tablas":[{"nombre":"orders","ambitos":["dia","producto"]},{"nombre":"ads","ambitos":["dia"],"origenes_alguno":["google_ads"]},{"nombre":"daily","ambitos":["dia"]}]}
schemas = {"orders":{"date","product","net_sales"},"ads":{"date","spend"},"daily":{"date","product"}}
seed = {"base":[{"nombre":"Ventas","tabla":"orders","fecha":"date","expresion":"net_sales","agregacion":"sum","familia":"tienda","fuente":"shopify","atribucion":"sin_atribucion","unidad":"money"},{"nombre":"Inversión","tabla":"ads","fecha":"date","expresion":"spend","agregacion":"sum","familia":"anuncios","fuente":"google_ads","atribucion":"sin_atribucion","unidad":"money"}],"derivados":[{"nombre":"MER","tabla":"daily","formula":{"op":"div","izquierda":{"ref":"Ventas"},"derecha":{"ref":"Inversión"}},"familia":"combinada","fuente":"shopify_y_anuncios","atribucion":"sin_atribucion","unidad":"ratio"}]}
check("Perfil diario coherente", module.revisar(manifest,seed,schemas) == [])
bad = copy.deepcopy(manifest);bad["tablas"][2]["ambitos"].append("producto")
check("Publicidad sin producto rechaza ese desglose", any("no tiene el ámbito producto" in e for e in module.revisar(bad,seed,schemas)))
bad = copy.deepcopy(seed);bad["derivados"][0]["formula"]["izquierda"] = {"ref":"Ausente"}
check("Referencia inexistente se rechaza", any("no existe" in e for e in module.revisar(manifest,bad,schemas)))
bad = copy.deepcopy(seed);duplicate=copy.deepcopy(bad["base"][0]);duplicate["nombre"]="Ventas duplicadas";bad["base"].append(duplicate)
check("Concepto duplicado se rechaza", any("misma cifra" in e for e in module.revisar(manifest,bad,schemas)))
bad = copy.deepcopy(seed);bad["derivados"][0]["formula"]["op"]="pow"
check("Operación no admitida se rechaza", any("operación desconocida" in e for e in module.revisar(manifest,bad,schemas)))
print(json.dumps({"checks": checks, "passed": len(checks), "network": "forbidden"}, ensure_ascii=False))
