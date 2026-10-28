## Reference solution

```python
from pydantic import BaseModel, Field

# write a Food pydantic model

class Food(BaseModel):
    id: int
    name: str
    serving_size: str
    kcal_per_serving: int
    protein_grams: float
    fibre_grams: float = 0
```
