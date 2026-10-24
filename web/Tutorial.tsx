import { Play } from "lucide-react";
import type { Day } from "./types";
import { formatDuration } from "./model";
import { CopyButton, Markdown } from "./TaskDialog";

const firstCommand = `cd /home/musel/Github/capital-one-prep
uv sync
uv run python scripts/practice.py start d01-bug`;

export function Tutorial({
  firstDay,
  openFirstDay,
}: {
  firstDay: Day;
  openFirstDay: () => void;
}) {
  return (
    <section className="resource-page tutorial-page">
      <p className="date-heading">Tu recorrido en 2 minutos</p>
      <h1>Empieza aquí</h1>
      <p className="day-focus">
        Elige un ejercicio. Practica en tu editor o en voz alta y guarda el
        resultado.
      </p>
      <ol className="tutorial-steps">
        <li>
          <strong>Abre el bloque del día.</strong> Lee el enunciado y usa su
          comando o prompt para preparar el ejercicio.
        </li>
        <li>
          <strong>Practica.</strong> El reloj es opcional. Cerrar el ejercicio
          no lo pausa; usa «Pausar» para detenerlo.
        </li>
        <li>
          <strong>Guarda tus notas.</strong> En «Mi intento y revisión»,
          registra el resultado. «Exportar» descarga un respaldo.
        </li>
      </ol>

      <h2 className="tutorial-heading">
        Tu primer día:{" "}
        {formatDuration(firstDay.blocks.reduce((n, b) => n + b.minutes, 0))}
      </h2>
      <ul className="tutorial-agenda">
        {firstDay.blocks.map((block) => (
          <li key={block.id}>
            <span>{block.title}</span>
            <strong>{formatDuration(block.minutes)}</strong>
          </li>
        ))}
      </ul>
      <p className="muted">Las pausas son aparte.</p>
      <button className="button primary tutorial-start" onClick={openFirstDay}>
        <Play size={16} /> Abrir el día 1
      </button>

      <details className="tutorial-detail">
        <summary>Ejemplo completo: tu primer ejercicio en el editor</summary>
        <Markdown>{`### A. Crea una copia del bug del día 1
Abre una terminal y ejecuta lo siguiente. Si ya tienes un intento y quieres continuar, vuelve a **esa misma carpeta**; no necesitas ejecutar start otra vez.`}</Markdown>
        <div className="command-row">
          <code className="multiline-command">{firstCommand}</code>
          <CopyButton text={firstCommand} />
        </div>
        <Markdown>{`### B. Abre la carpeta que devuelve el comando
Usa **Open Folder / Abrir carpeta** en tu editor. Abre solo esa carpeta de \`attempts/\`, no todo el repositorio: así tu agente trabaja sobre el intento sin tener a la vista las respuestas del instructor. Lee su README.

En una terminal **dentro de esa carpeta**, ejecuta (si ya existe .venv, omite uv venv):

\`\`\`bash
uv venv
uv sync
uv run pytest
uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
\`\`\`

Abre **http://127.0.0.1:8000** para ver la aplicación del ejercicio. Si el puerto está ocupado, usa \`--port 8001\` y abre ese puerto. Deja el servidor en esa terminal; usa una segunda terminal para pruebas. Al cambiar de intento, detén el servidor anterior con **Ctrl+C** y arranca el de la nueva carpeta. Reiniciar la app restablece sus datos ficticios.

Los tests iniciales comprueban el arranque: pueden pasar aunque el bug siga presente. Añade una prueba que reproduzca el ticket.

### C. Investiga con el agente y decide tú
Puedes empezar con: “Read the task README. Locate the relevant behavior and tests. Propose a reproduction and likely cause before editing. Keep changes within this attempt folder.”

Revisa su hipótesis, pide un cambio acotado y comprueba el diff y los resultados. Si no tienes un agente configurado, usa un chat como apoyo y realiza tú las ediciones y pruebas. La página no incluye un chat de IA ni configura tu editor. Durante la entrevista real, usa únicamente las herramientas autorizadas.

### D. Comprueba el intento desde la raíz
En otra terminal, reemplaza TU-CARPETA por el nombre real que recibiste en el paso A:

\`\`\`bash
cd /home/musel/Github/capital-one-prep
uv run python scripts/practice.py check attempts/TU-CARPETA
\`\`\`

**Passed**: pasaron las comprobaciones cubiertas. **Failed**: queda un requisito por cumplir; es normal antes de resolver el starter. **Error**: hubo un problema de ejecución o configuración, no una evaluación correcta de la solución. Guarda el resultado real.

La feature se crea con \`uv run python scripts/practice.py start d01-feature\`, desde la raíz, como otra copia limpia. Conservarás el trabajo del bug.

### E. Registra y pide revisión
En “Mi intento y revisión”, guarda la ruta, las pruebas y tu explicación. Puedes decirme: **“Revisa mi intento en attempts/…, este fue el resultado y aquí me atasqué.”** Puedo revisar los archivos de esta PC. No necesitas publicar tu solución.`}</Markdown>
      </details>

      <details className="tutorial-detail">
        <summary>Cómo trabajar los casos, behavioral y Python</summary>
        <Markdown>{`- **Business case:** razona sin ejecutar código ni pedir la respuesta a la IA. Habla en inglés, aplica las reglas, predice resultados y explica los defectos. En “Mi intento y revisión”, guarda tu predicción, termina el intento y después pulsa “He terminado: abrir explicación”.
- **Behavioral:** la guía está dentro del bloque. Elige un proyecto real y un episodio, sigue las preguntas en orden y escribe en “Mi intento y revisión”. Practica en inglés; no necesitas abrir un archivo externo.
- **Python / LeetCode:** pulsa “Copiar prompt” para pedir al agente local un starter y pruebas sin solución. Implementa tú la función y ejecuta el comando uv indicado. Si eliges una alternativa LeetCode, sustituye el ejercicio original dentro del mismo tiempo.

Registra el resultado dentro de cada bloque. No hay un bloque adicional de cierre; puedes exportar el progreso cuando quieras.`}</Markdown>
      </details>

      <details className="tutorial-detail">
        <summary>Dónde se guarda todo y cómo continuar mañana</summary>
        <Markdown>{`- **Código:** en la carpeta local de cada intento. Vuelve a abrirla para continuar; ejecutar start crea una copia nueva y conserva las anteriores.
- **Notas, respuestas, checklists y reloj:** en este navegador. La predicción tiene un botón de guardado; las notas se guardan al escribir. Si aparece un error de guardado, copia tu texto antes de salir.
- **Respaldo:** “Exportar” descarga un JSON. Guárdalo en la carpeta local private/. “Importar” permite llevarlo a otro navegador; confirma el reemplazo solo después de elegir el archivo correcto.
- **Mañana:** abre la página y elige el día que corresponda en el calendario de Tijuana. Si dejaste seleccionada otra fecha, usa “Volver a hoy”. El botón “Continuar” abre un bloque en curso; también puedes abrir cualquier fila.
- **Revisión conmigo:** proporciona la ruta del intento. Para que lea también tus notas de la página, exporta el JSON y dime dónde lo guardaste. No se sincroniza automáticamente con esta conversación.

No hace falta hacer git push de tus intentos. attempts/ y private/ están excluidos del repositorio público.`}</Markdown>
      </details>
    </section>
  );
}
