# Gilded Rose — repository-based extension

## English interview prompt

You have inherited the Python inventory updater from the open-source Gilded Rose
refactoring kata. Read the existing implementation and preserve its public API.
Implement the upstream requirement for Conjured products without changing the
`Item` class or replacing the caller's `items` list. A small, safe refactor is
welcome if it helps explain your change; rewriting the application is unnecessary.

For this exercise, a Conjured product has a name beginning with the exact,
case-sensitive prefix `Conjured ` (including the space). These are ordinary
perishable products, not combinations with Brie, Backstage, or Sulfuras types.
This prefix convention makes the upstream requirement precise for our tests.

- On each update, reduce its quality by 2 if `sell_in` is positive at the start
  of the update; reduce it by 4 when `sell_in` starts at zero or below.
- Then its `sell_in` decreases by one. Quality must never fall below zero.
- Preserve each item's name, the `Item` API, in-place updates, and behavior for
  all other existing products. Read `GildedRoseRequirements.md` for their rules.
- Calling `update_quality()` must process every item, including mixed inventories.
- No new dependencies, network services, UI, or database are needed.

Examples after one daily update:

| Name | Initial sell_in, quality | Expected sell_in, quality |
| --- | --- | --- |
| Conjured Mana Cake | 3, 6 | 2, 4 |
| Conjured Mana Cake | 0, 8 | -1, 4 |
| Conjured Elixir | 0, 3 | -1, 0 |
| Elixir of the Mongoose | 5, 7 | 4, 6 |

## Trabajo en 30 minutos

1. **5 min — orientación:** lee el requisito y el código. Ejecuta los smoke
   checks; predice el resultado de un Conjured antes de ejecutar el check completo.
2. **20 min — cambio:** confirma el fallo, agrega al menos una prueba propia o
   registra un caso reproducible, implementa y ejecuta los checks. Conserva el
   intento aunque no termines. No leas la solución de referencia durante esta fase.
3. **5 min — explicación en inglés:** “What changed? What existing behavior did
   you protect? Which boundary case was easiest to miss?” Guarda la explicación,
   comandos/resultados y cualquier ayuda utilizada en `notes.md` en tu intento.

Entrega: código del intento, evidencia antes/después y explicación. Criterios:
tasas 2/4 correctas, frontera `sell_in = 0`, suelo en cero, ninguna regresión y
cambio que puedas explicar. Un resultado incompleto sigue siendo útil para revisar.

Es un kata público pequeño. No es un problema confirmado de Capital One ni una
simulación del tamaño de un repositorio de producción. El cronómetro entrena la
lectura de código ajeno y una extensión acotada. Completarlo no demuestra preparación.
