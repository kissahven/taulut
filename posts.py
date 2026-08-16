import db

def add_post(poster_id, title, body):
    sql = "INSERT INTO items (poster_id, title, body) VALUES (?, ?, ?)"
    db.execute(sql, [poster_id, title, body])

def get_posts():
    sql = "SELECT id, title, body FROM items ORDER BY id DESC"
    return db.query(sql)

def get_post(post_id):
    sql = """SELECT items.id, items.poster_id, items.title, items.body, users.id, users.username
                FROM items
                FULL JOIN users ON items.poster_id = users.id
                WHERE items.id = ?"""
    rows = db.query(sql, [post_id])
    for row in rows:
        print(row)
    return rows[0]