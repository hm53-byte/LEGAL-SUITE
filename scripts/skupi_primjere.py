"""pytest plugin: prvi uspjesan poziv svakog generatora -> pristup/primjeri.json (argumenti po imenu).

Pokretanje iz korijena: PYTHONPATH=scripts PRIMJERI_IZLAZ=pristup/primjeri.json python -m pytest tests -p skupi_primjere
"""
import copy, functools, importlib, inspect, json, pkgutil, os
from pathlib import Path

ZAPISANO = {}

def _json_ok(v):
    try:
        json.dumps(v, ensure_ascii=False); return True
    except TypeError:
        return False

def pytest_configure(config):
    import generatori
    for m in pkgutil.iter_modules(generatori.__path__):
        mod = importlib.import_module(f"generatori.{m.name}")
        for ime, f in list(vars(mod).items()):
            if not (ime.startswith("generiraj_") and inspect.isfunction(f) and f.__module__ == mod.__name__):
                continue
            sig = inspect.signature(f)
            kljuc = f"{m.name}/{ime[len('generiraj_'):]}"
            def omot(*a, __f=f, __sig=sig, __k=kljuc, **kw):
                rez = __f(*a, **kw)
                if __k not in ZAPISANO and isinstance(rez, str) and "Greška" not in rez[:200]:
                    b = __sig.bind(*a, **kw); b.apply_defaults()
                    args = {k: copy.deepcopy(v) for k, v in b.arguments.items()}
                    if _json_ok(args):
                        ZAPISANO[__k] = args
                return rez
            functools.update_wrapper(omot, f)
            setattr(mod, ime, omot)

def pytest_sessionfinish(session, exitstatus):
    izlaz = Path(os.environ["PRIMJERI_IZLAZ"])
    izlaz.write_text(json.dumps(dict(sorted(ZAPISANO.items())), ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\nprimjera: {len(ZAPISANO)}")
