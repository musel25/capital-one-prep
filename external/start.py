"""Copy the pinned public kata into a new workspace; never reset an attempt."""
import argparse
import json
import shutil
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TASK_ID = "external-gilded-rose"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("task_id", choices=[TASK_ID])
    parser.add_argument("--output-root", type=Path, default=ROOT / "attempts")
    args = parser.parse_args()
    output = args.output_root.resolve()
    output.mkdir(parents=True, exist_ok=True)
    attempt = Path(tempfile.mkdtemp(prefix=f"{TASK_ID}-", dir=output))
    upstream = HERE / "upstream/gilded-rose"
    copies = {
        upstream / "python/gilded_rose.py": "gilded_rose.py",
        upstream / "python/texttest_fixture.py": "texttest_fixture.py",
        upstream / "license.txt": "LICENSE",
        upstream / "GildedRoseRequirements.md": "GildedRoseRequirements.md",
        HERE / "TASK.md": "TASK.md",
    }
    for source, name in copies.items():
        shutil.copyfile(source, attempt / name)
    provenance = json.loads((HERE / "provenance.json").read_text())
    (attempt / ".external-attempt.json").write_text(json.dumps({
        "id": TASK_ID, "source": provenance["repository"], "commit": provenance["commit"],
    }, indent=2) + "\n")
    (attempt / "README.md").write_text(f"""# Gilded Rose — tu intento

Abre esta carpeta en tu editor y lee TASK.md. Conserva esta ruta para continuar
o pedir revisión. Todos los comandos siguientes se ejecutan desde la raíz:

```sh
cd {ROOT}
uv run python external/check.py {attempt} --smoke
uv run python external/check.py {attempt}
uv run python {attempt}/texttest_fixture.py 3
```

El starter conserva el código upstream sin modificar. Los smoke checks deben
pasar; los checks Conjured deben fallar antes de tu cambio. La tarea es completar
esa extensión sin cambiar Item ni romper las reglas anteriores. Guarda tu
explicación en notes.md aquí. No hace falta instalar nada adicional.

`start.py` crea otro intento; nunca lo uses para intentar reabrir éste. Continúa
editando esta carpeta. Los checks no copian soluciones ni reescriben tus archivos.
No abras external/reference/ hasta terminar y explicar tu intento.

Fuente: {provenance['repository']}/tree/{provenance['commit']}/python
Licencia MIT upstream incluida en LICENSE. Guía: external/README.md en la raíz.
""")
    print(attempt)


if __name__ == "__main__":
    main()
