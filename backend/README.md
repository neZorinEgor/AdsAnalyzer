# Backend

```bash
bash mysql.sh
```

```bash
alembic upgrade head;uvicorn src.main:app --reload
```

# DevMode:
```bash
bash mysql.sh
alembic upgrade head
uvicorn src.main:app --reload 
```