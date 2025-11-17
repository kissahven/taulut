import db

def add_post(poster_id, title, body):
    sql = "INSERT INTO items (poster_id, title, body) VALUES (?, ?, ?)"
    db.execute(sql, [poster_id, title, body])

def get_posts():
    sql = "SELECT id, title, body FROM items"
    return db.query(sql)

def get_post(item_id):
    sql = """ SELECT items.poster_id,
                    items.title,
                    items.body,
                    users.username
                FROM items, users
                WHERE users.id = items.poster_id 
                AND items.id = ?
                ;"""
    return db.query(sql, [item_id])
