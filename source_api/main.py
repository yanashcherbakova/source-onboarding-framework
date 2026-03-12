from fastapi import FastAPI, Query, HTTPException, Response
from source_api.db import get_connection
import time

FAILURE_MODE = None

app = FastAPI()

def check_failure_mode(response : Response):
    if FAILURE_MODE == "RATE_LIMIT":
        response.headers["Retry-After"] = "30"
        raise HTTPException(status_code=429, detail="Rate limit exceded")
        
    if FAILURE_MODE == "FLAKY_500":
        raise HTTPException(status_code=500, detail="Internal server error")
    
    if FAILURE_MODE == "TIMEOUT":
        time.sleep(20)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/v1/plans")
def get_plans(response : Response, limit: int = Query(default=100, le=1000), updated_from = None, cursor = None):
    check_failure_mode(response)

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
def get_subscriptions(response : Response, limit: int = Query(default=100, le=1000), updated_from = None, cursor = None):
    check_failure_mode(response)
    
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


@app.get("/v1/subscription_events")
def get_subscription_events(response : Response, limit: int = Query(default=100, le=100), updated_from = None, cursor = None):
    check_failure_mode(response)
    
    conn = get_connection()
    cur = conn.cursor()

    sql = """SELECT * FROM subscription_events WHERE 1 = 1"""

    params = []
    if updated_from:
        sql += " AND updated_at > %s"
        params.append(updated_from)

    if cursor:
        sql += " AND event_id > %s"
        params.append(cursor)

    sql += " ORDER BY event_id LIMIT %s"
    params.append(limit + 1)

    cur.execute(sql, params)
    rows = cur.fetchall()

    has_next_page = len(rows) > limit

    if has_next_page:
        next_cursor = rows[limit - 1][0]
        rows = rows[:limit]
    else:
        next_cursor = None

    items = []
    for row in rows:
        items.append(
            {
                "event_id" : row[0],
                "subscription_id" : row[1],
                "event_type" : row[2],
                "event_time" : row[3].isoformat() if row[3] else None,
                "amount" : float(row[4]) if row[4] else None,
                "currency" : row[5],
                "discount_percent" : float(row[6]) if row[6] else None,
                "valid_from" : row[7].isoformat() if row[7] else None,
                "metadata" : row[8],
                "updated_at" : row[9].isoformat() if row[9] else None,
                "deleted" : row[10],
            }
        )

    return {"items" : items, "next_cursor" : next_cursor}
