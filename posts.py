import db

def add_post(poster_id, title, body):
    sql = "INSERT INTO items (poster_id, title, body) VALUES (?, ?, ?)"
    db.execute(sql, [poster_id, title, body])

def get_posts():
    sql = "SELECT id, title, body FROM items"
    return db.query(sql)
