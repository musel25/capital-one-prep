## Reference solution

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to PyBites' FastAPI Learning Path 🐍 🎉"}
```
