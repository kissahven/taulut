import db

def add_post(poster_id, title, body):
    sql = "INSERT INTO items (poster_id, title, body) VALUES (?, ?, ?)"
    db.execute(sql, [poster_id, title, body])

def get_posts():
    sql = "SELECT id, title, body FROM items ORDER BY id DESC"
    return db.query(sql)

def get_post(post_id):
    sql = """SELECT id, poster_id, title, body
                FROM items
                WHERE items.id = ?"""
    rows = db.query(sql, [post_id])
    return rows[0]