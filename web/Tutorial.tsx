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
        <Markdown>{`### Abre y ejecuta la copia
Abre la carpeta devuelta en tu editor y lee su README. Trabaja solo en esa copia para evitar las soluciones del instructor.

Desde la carpeta del intento (omite \`uv venv\` si ya existe .venv):

\`\`\`bash
uv venv
uv sync
uv run pytest
uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
\`\`\`

Abre http://127.0.0.1:8000. Usa otra terminal para pruebas. Si el puerto está ocupado, usa 8001. Detén el servidor con Ctrl+C al cambiar de intento; reiniciarlo restablece los datos.

Los tests iniciales solo prueban el arranque. Añade una prueba del fallo, pide un cambio acotado a tu agente y revisa el diff.

### Comprueba el resultado
Desde la raíz del repositorio:

\`\`\`bash
uv run python scripts/practice.py check attempts/TU-CARPETA
\`\`\`

**Passed:** pasan los checks. **Failed:** falta un requisito. **Error:** fallo de ejecución o configuración.

Crea la feature por separado con \`uv run python scripts/practice.py start d01-feature\`. Guarda la ruta y los resultados en “Mi intento y revisión”.`}</Markdown>
      </details>

      <details className="tutorial-detail">
        <summary>Cómo trabajar los casos, behavioral y Python</summary>
        <Markdown>{`- **Caso técnico:** responde la parte de producto y traza el código sin ejecutarlo. Guarda la predicción antes de revelar.
- **Behavioral:** responde las preguntas del día en inglés con experiencias reales.
- **Python:** copia el prompt para preparar un starter local, implementa la función y ejecuta sus pruebas.`}</Markdown>
      </details>

      <details className="tutorial-detail">
        <summary>Dónde se guarda todo y cómo continuar mañana</summary>
        <Markdown>{`- **Código:** permanece en la carpeta de tu intento. Abrirla permite continuar; start crea otra copia.
- **Notas y reloj:** se guardan en este navegador. Si aparece un error de guardado, copia el texto antes de salir.
- **Respaldo:** Exportar descarga un JSON; Importar permite llevarlo a otro navegador.
- **Revisión con IA:** comparte la ruta del intento o de la exportación. Las notas del sitio no se comparten automáticamente.

No publiques tus respuestas: attempts/ y private/ están excluidos de Git.`}</Markdown>
      </details>
    </section>
  );
}
