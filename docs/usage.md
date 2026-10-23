# Tu espacio de preparación

Abre [Capital One Prep](https://timer.musel.dev/grind/capital-one/). El calendario elige la fecha de Tijuana entre el 23 de octubre y el 1 de noviembre de 2026. Antes del inicio abre el día 1; después del final conserva el día 10. Puedes elegir cualquier fecha. Cada día tiene exactamente 240 minutos de trabajo; toma pausas aparte.

## Página y editor

La página muestra tareas, tiempos por fase, preguntas, entregables, criterios de revisión y fuentes. Abre un bloque y sigue el enunciado. Para trabajar con IA, abre **solo la carpeta del intento** en tu editor: el repositorio principal contiene material del instructor.

```bash
cd /home/musel/Github/capital-one-prep
uv sync
uv run python scripts/practice.py list
uv run python scripts/practice.py start d01-bug
```

El último comando imprime una carpeta nueva. Ábrela en tu editor y lee su README. Allí están los comandos `uv sync`, `uv run pytest` y `uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000`. Los tests iniciales comprueban el arranque; no demuestran que hayas resuelto el ticket.

Al terminar, desde la raíz ejecuta:

```bash
uv run python scripts/practice.py check attempts/NOMBRE-DE-TU-INTENTO
```

La página no ejecuta ni observa tu código local. Registra la ruta, el resultado real y tus decisiones en sus notas. Para pedir revisión: **«Revisa mi intento en attempts/…; corrí estos tests y obtuve este resultado»**. Para empezar otra vez usa `start` de nuevo; no borres tu trabajo. Bug y feature tienen copias independientes.

El día 9 añade código real de Gilded Rose. Usa su comando específico `uv run python external/start.py external-gilded-rose` y sigue el README generado. Su procedencia y licencia están en [external/README.md](../external/README.md).

## Casos y behavioral

En los casos, interpreta las reglas, predice resultados y explica tu corrección sin ejecutar el código. Guarda la predicción y marca el intento terminado antes de abrir la explicación. La solución se oculta para evitar spoilers casuales; no es un control de acceso. No pidas al agente que resuelva el caso antes de tu intento.

Para behavioral, [las plantillas](../behavioral/story-templates.md) están vacías deliberadamente. Usa experiencias ciertas, aportación individual y resultados que puedas defender. Practica preguntas de seguimiento; no memorices respuestas inventadas.

## Guardar el progreso

El progreso, las notas y el temporizador se guardan **solo en este navegador y este origen**. No se sincronizan entre dispositivos. Exporta el JSON y guárdalo en `private/`. Importa el archivo para cambiar de navegador; antes de reemplazar, la interfaz conserva una copia local del estado anterior.

Las carpetas `attempts/` y `private/` están ignoradas por Git. No fuerces su inclusión en commits. El despliegue copia exclusivamente `dist/`. Para revisar tus notas desde esta PC, guarda una exportación local y proporciona su ruta.

Si otra pestaña cambia el progreso, la página bloquea nuevas escrituras para evitar pisarlo. Exporta lo que necesites y recarga. Si el almacenamiento está dañado, descarga la recuperación antes de reiniciar.

## Ejecutar la página localmente

```bash
./scripts/local.sh
```

Abre `http://127.0.0.1:5187/grind/capital-one/`. El sitio local y el publicado usan almacenamientos distintos: exporta/importa si quieres trasladar progreso.

## Verificación y despliegue

```bash
npm ci
npm test
npm run build
uv sync
uv run pytest
uv run python scripts/practice.py verify
```

Los checks de Python comprueban que los 20 starters fallan en el comportamiento objetivo, que las 20 referencias pasan, que iniciar/verificar conserva intentos y que el ejercicio upstream conserva su procedencia y sus reglas. Los tests del planner comprueban calendario, duración, importación y condiciones de revisión. Pasar esos checks no equivale a estar preparado para una entrevista.

`scripts/deploy.sh` requiere cambios guardados y publica una versión estática independiente en el VPS existente. Respalda nginx, cambia el enlace `current` y revierte si fallan sus comprobaciones. No sube respuestas ni modifica el almacenamiento de Grind Recall. La ruta bajo `/grind/` evita la caché de navegación del service worker del temporizador.

El formato de entrevista, las herramientas de IA permitidas y sus tiempos deben contrastarse con tu convocatoria. El plan diferencia documentación oficial, testimonios de candidatos y ejercicios creados; no presenta los escenarios de práctica como preguntas confirmadas.
