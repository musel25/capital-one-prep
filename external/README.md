# Gilded Rose: extensión en código upstream real

Este ejercicio usa archivos reales de
[emilybache/GildedRose-Refactoring-Kata](https://github.com/emilybache/GildedRose-Refactoring-Kata/tree/d6407909c73b2ba61bfa7568af0d9bdce1902fd5/python),
fijados al commit `d6407909c73b2ba61bfa7568af0d9bdce1902fd5`.
Es un kata pequeño de refactorización y extensión, no una pregunta confirmada de
Capital One ni un repositorio grande de producción. Fuente de tipo **repository**.

## Empezar sin sobrescribir trabajo

Desde la raíz de `capital-one-prep`:

```sh
uv run python external/start.py external-gilded-rose
```

El comando imprime una ruta absoluta nueva, por ejemplo
`/home/musel/Github/capital-one-prep/attempts/external-gilded-rose-abcd1234`.
Abre **esa carpeta** en tu editor. Guarda la ruta; para continuar, vuelve a la
misma carpeta. Cada ejecución de `start.py` crea otro intento independiente y
nunca reinicia uno anterior. `attempts/` está excluido de Git.

En los comandos siguientes, reemplaza `ATTEMPT_PATH` por la ruta impresa. Ejecútalos
desde la raíz del proyecto. El README generado dentro del intento ya incluye los
comandos con tu ruta exacta.

```sh
uv run python external/check.py ATTEMPT_PATH --smoke
uv run python external/check.py ATTEMPT_PATH
uv run python ATTEMPT_PATH/texttest_fixture.py 3
```

El primer comando debe pasar desde el inicio. El segundo debe fallar para
Conjured antes de tu cambio; al terminar, debe pasar completo. El fixture muestra
la evolución del inventario, pero su salida por sí sola no demuestra corrección.
No se requiere instalar las dependencias opcionales del repositorio upstream.
Se utiliza el entorno `uv` del proyecto y la biblioteca estándar.

Lee `TASK.md` en tu intento para el requisito completo en inglés. Presupuesta
**5 min lectura + 20 min implementación + 5 min explicación** dentro de los 90
minutos técnicos del día 9. Sustituye tiempo de revisión de ese bloque: no agrega
tiempo a las cuatro horas diarias. Si no acabas, conserva el intento y sus fallos.
Puedes pedir revisión compartiendo su ruta exacta y `notes.md` con resultados,
decisiones y ayudas recibidas. El navegador no inspecciona automáticamente tu código.

## Procedencia y licencia

- `upstream/gilded-rose/` conserva **sin modificaciones** cuatro archivos del
  commit fijado: implementación Python, fixture de consola, requisitos y licencia.
  Es una selección explícita; no es un clon completo ni incluye la suite upstream.
- `provenance.json` registra las rutas originales y sus hashes de blobs Git.
  `tests/test_external.py` comprueba los hashes, incluidas las nuevas líneas.
- Leímos la implementación, el fixture, los requisitos y la licencia antes de
  ejecutar el código. No se ejecutan scripts de instalación upstream.
- La [licencia MIT original](upstream/gilded-rose/license.txt) conserva
  `Copyright (c) 2015 @emilybache` y se copia íntegra a cada intento como `LICENSE`.
- `TASK.md`, `start.py` y `check.py` son material de práctica local. La convención
  del prefijo `Conjured ` está documentada; no se presenta como detalle upstream.

## Revisión posterior al intento

La solución local está en `reference/gilded_rose.py`; es un derivado del archivo
upstream bajo su licencia MIT y conserva `Item`. No se copia a tu carpeta. Ábrela
solo después de guardar tu intento y tu explicación. Anota la ayuda si la consultas.

Para verificar el material como instructor, sin tocar intentos del alumno:

```sh
uv run python external/check.py external/upstream/gilded-rose/python --smoke
uv run python external/check.py external/upstream/gilded-rose/python
uv run python external/check.py external/reference
uv run pytest tests/test_external.py -q
```

El segundo comando tiene salida **1 esperada**: prueba la extensión ausente en
el código upstream. El primero, tercero y cuarto deben salir con **0**. El checker
devuelve **2** si no puede cargar el archivo o ejecutarlo; eso no equivale a un fallo
normal de requisitos. Usa `--json` para conservar evidencia estructurada.
