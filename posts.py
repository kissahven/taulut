import db

def add_post(poster_id, title, body):
    sql = "INSERT INTO items (poster_id, title, body) VALUES (?, ?, ?)"
    db.execute(sql, [poster_id, title, body])

def get_posts():
    sql = "SELECT id, title, body FROM items ORDER BY id DESC"
    return db.query(sql)

def get_post(post_id):
    sql = """SELECT i.id, i.poster_id, i.title, i.body, u.id, u.username
                FROM items i
                LEFT JOIN users u ON i.poster_id = u.id
                WHERE i.id = ?"""
    rows = db.query(sql, [post_id])
    return rows[0] if rows else None

def update_post(post_id, title, body):
    sql = "UPDATE items SET title = ?, body = ? WHERE id = ?"
    db.execute(sql, [title, body, post_id])

def remove_post(post_id):
    sql = "DELETE FROM items WHERE id = ?"
    db.execute(sql, [post_id])

def search_posts(query):
    sql = """SELECT id, title, body
            FROM items
            WHERE title LIKE ? OR body LIKE ?
            ORDER BY id DESC"""
    like = "%" + query + "%"
    return db.query(sql, [like, like])