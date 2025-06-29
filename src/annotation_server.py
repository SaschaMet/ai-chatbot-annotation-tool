import os
import sqlite3
from fastapi import FastAPI, Request, HTTPException, Body
from fastapi.responses import FileResponse

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_PATH = os.path.join(BASE_DIR, "index.html")
DB_PATH = os.path.join(BASE_DIR, "../sqlite/annotations.db")

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS annotations (
            id INTEGER PRIMARY KEY,
            query TEXT,
            response TEXT,
            pass BOOLEAN,
            feedback TEXT,
            error_code TEXT
        )
    """)
    conn.commit()
    conn.close()


@app.get("/")
def serve_index():
    return FileResponse(HTML_PATH, media_type="text/html")


@app.post("/save-annotation")
async def save_annotation(request: Request):
    data = await request.json()
    annotation = data.get("annotation")
    if not annotation:
        raise HTTPException(status_code=400, detail="Missing annotation data")
    annotation_id = annotation.get("id")
    query = annotation.get("query")
    response_ = annotation.get("response")
    pass_ = annotation.get("pass")
    feedback = annotation.get("feedback")
    error_code = annotation.get("error_code")
    conn = get_db_connection()
    if annotation_id is not None:
        # Upsert by id
        conn.execute(
            """
            INSERT INTO annotations (id, query, response, pass, feedback, error_code)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                query=excluded.query,
                response=excluded.response,
                pass=excluded.pass,
                feedback=excluded.feedback,
                error_code=excluded.error_code
        """,
            (annotation_id, query, response_, pass_, feedback, error_code),
        )
    else:
        # Insert new
        conn.execute(
            """
            INSERT INTO annotations (query, response, pass, feedback, error_code)
            VALUES (?, ?, ?, ?, ?)
        """,
            (query, response_, pass_, feedback, error_code),
        )
    conn.commit()
    conn.close()
    return {"status": "ok"}


@app.post("/upload-json")
async def upload_json(data: dict = Body(...)):
    # Accepts a dict with a 'data' key containing a list of annotation dicts
    items = data.get("data")
    if not isinstance(items, list):
        raise HTTPException(
            status_code=400, detail="Uploaded JSON must be a list of objects."
        )
    conn = get_db_connection()
    inserted = 0
    for item in items:
        # Accepts keys: id, query, response, pass, feedback, error_code
        annotation_id = item.get("id")
        query = item.get("query")
        response_ = item.get("response")
        pass_ = item.get("pass")
        feedback = item.get("feedback")
        error_code = item.get("error_code")
        if annotation_id is not None:
            conn.execute(
                """
                INSERT INTO annotations (id, query, response, pass, feedback, error_code)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    query=excluded.query,
                    response=excluded.response,
                    pass=excluded.pass,
                    feedback=excluded.feedback,
                    error_code=excluded.error_code
            """,
                (annotation_id, query, response_, pass_, feedback, error_code),
            )
        else:
            conn.execute(
                """
                INSERT INTO annotations (query, response, pass, feedback, error_code)
                VALUES (?, ?, ?, ?, ?)
            """,
                (query, response_, pass_, feedback, error_code),
            )
        inserted += 1
    conn.commit()
    conn.close()
    return {"status": "ok", "inserted": inserted}


@app.get("/annotations")
def get_annotations():
    conn = get_db_connection()
    cursor = conn.execute("SELECT * FROM annotations")
    rows = cursor.fetchall()
    conn.close()
    annotations = [dict(row) for row in rows]
    return {"annotations": annotations}


@app.delete("/annotations")
def delete_annotations():
    conn = get_db_connection()
    conn.execute("DELETE FROM annotations")
    conn.commit()
    conn.close()
    return {"status": "ok", "message": "All annotations deleted."}


if __name__ == "__main__":
    import uvicorn

    init_db()  # Initialize the database
    uvicorn.run("annotation_server:app", host="0.0.0.0", port=8475, reload=True)
