# Casos originales de práctica

Diez casos nuevos, uno por día. En el planner, guarda tu predicción y termina el intento antes de revelar la solución. Practica **sin ejecutar código**; es una restricción de simulación tomada de un testimonio, no una regla confirmada para tu invitación.

Cada archivo de caso contiene enunciado y contrato. Los archivos en `cases/instructor/` contienen respuestas: no los abras antes de terminar. Son accesibles para revisión local; el bloqueo del planner es una ayuda de práctica, no un mecanismo de seguridad.

| Día | Caso |
|---|---|
| 1 | [Caso: alertas útiles, sin ruido](d01.md) |
| 2 | [Caso: transferir sin dejar estado parcial](d02.md) |
| 3 | [Caso: recompensas sin exceder el presupuesto](d03.md) |
| 4 | [Caso: navegar disputas sin perder resultados](d04.md) |
| 5 | [Caso: gasto neto y reembolsos parciales](d05.md) |
| 6 | [Case: digital card-number validation](card-number-validation.md) |
| 7 | [Caso: un asistente que sabe cuándo escalar](d07.md) |
| 8 | [Mock A: liquidación con reserva por comercio](d08.md) |
| 9 | [Caso: promoción con fronteras explícitas](d09.md) |
| 10 | [Mock B: reservas de equipo con cancelaciones](d10.md) |

Each session is 60 minutes. Follow its phase timer and reveal stages progressively. Save a prediction before the answer key. The original day-6 API case and the later authorization case remain available in Previous exercises with their original notes. Card-number rules are invented practice, not real payment-card standards or confirmed interview questions.

## Case authoring and review

- The product discussion must stand on its own: identify the user, the situation or proposed product, the customer impact, and the decision to discuss.
- State the event order. A rejected attempt causing a balance decrease is a different problem from a successful retry decreasing it. Do not require learners to guess which happened.
- Define unfamiliar terms in plain language. Leave room for product assumptions and clarification without hiding essential facts.
- Specify technical inputs, units, return shapes, ordering, validation precedence, mutation rules, and relevant boundaries before asking for predictions.
- Start actual and required traces independently from the same initial state. Name the state or output used by each extension.
- Check that examples, tasks, and instructor answers agree. Keep intentional code defects and answer-key material out of the product setup.
- Update both the Markdown case and its full or staged copy in `curriculum/plan.json`. Preserve block IDs, learner attempts, saved progress, and reveal gates.
