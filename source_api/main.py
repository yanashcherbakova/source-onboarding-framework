from fastapi import FastAPI, Query
from source_api.db import get_connection

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/v1/plans")
def get_plans(limit: int = Query(default=100, le=1000), updated_from = None, cursor = None):
    conn = get_connection()
    cur = conn.cursor()

    sql = """SELECT * FROM plans WHERE 1 = 1"""

    params = []

    if cursor:
        sql += " AND plan_id > %s"
        params.append(cursor)

    if updated_from:
        sql += " AND updated_at > %s"
        params.append(updated_from)

    sql += " ORDER BY plan_id LIMIT %s"
    params.append(limit + 1)

    cur.execute(sql, params)
    rows = cur.fetchall()

    has_next_page = len(rows) > limit

    if has_next_page:
        next_cursor = rows[limit -1][0]
        rows= rows[:limit]
    else:
        next_cursor = None

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
    return {"items" : items, "next_cursor" : next_cursor}

@app.get("/v1/subscriptions")
def get_subscriptions(limit: int = Query(default=100, le=1000), updated_from = None, cursor = None):
    conn = get_connection()
    cur = conn.cursor()

    sql = """SELECT * FROM subscriptions WHERE 1 = 1 """

    params = []

    if cursor:
        sql += " AND subscription_id > %s"
        params.append(cursor)

    if updated_from:
        sql += " AND updated_at > %s"
        params.append(updated_from)

    sql += " ORDER BY subscription_id LIMIT %s"
    params.append(limit + 1)

    cur.execute(sql, params)
    rows = cur.fetchall()

    has_next_page = len(rows) > limit

    if has_next_page:
        next_cursor = rows[limit - 1][0]
        rows = rows[:limit]
    else:
        next_cursor = None

    cur.close()
    conn.close()

    items = []

    for row in rows:
        items.append(
            {
                "subscription_id" : row[0],
                "user_id" : row[1],
                "plan_id" : row[2],
                "status" : row[3],
                "started_at": row[4].isoformat() if row[4] else None,
                "current_period_start": row[5].isoformat() if row[5] else None,
                "current_period_end": row[6].isoformat() if row[6] else None,
                "discount_percent": float(row[7]) if row[7] is not None else None,
                "discount_reason": row[8],
                "canceled_at": row[9].isoformat() if row[9] else None,
                "updated_at": row[10].isoformat() if row[10] else None,
                "deleted": row[11]
            }
        )

    return {"items" : items, "next_cursor" : next_cursor}
