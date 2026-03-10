from fastapi import FastAPI, Query
from source_api.db import get_connection

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/v1/plans")
def get_plans(limit: int = Query(default=100, le=1000), updated_from = None):
    conn = get_connection()
    cur = conn.cursor()

    sql = """SELECT * FROM plans"""

    params = []

    if updated_from:
        sql += " WHERE updated_at > %s"
        params.append(updated_from)

    sql += " ORDER BY plan_id LIMIT %s"
    params.append(limit)

    cur.execute(sql, params)
    rows = cur.fetchall()

    cur.close()
    conn.close()

    items = []
    for row in rows:
        items.append(
            {
                "plan_id": row[0],
                "plan_name" : row[1],
                "price" : float(row[2]),
                "updated_at" : row[3].isoformat(),
                "deleted" : row[4]
            }
        )
    return {"items" : items}

