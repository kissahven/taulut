import db

def add_post(poster_id, title, body, classes):
    sql = "INSERT INTO items (poster_id, title, body) VALUES (?, ?, ?)"
    db.execute(sql, [poster_id, title, body])

    post_id = db.last_insert_id()
    sql = "INSERT INTO post_classes (post_id, name, value) VALUES (?, ?, ?)"
    for class_name, class_value in classes:
        db.execute(sql, [post_id, class_name, class_value])

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

def update_post(post_id, title, body, classes):
    sql = "UPDATE items SET title = ?, body = ? WHERE id = ?"
    db.execute(sql, [title, body, post_id])

    sql = "DELETE FROM post_classes WHERE post_id = ?"
    db.execute(sql, [post_id])
    sql = "INSERT INTO post_classes (post_id, name, value) VALUES (?, ?, ?)"
    for class_name, class_value in classes:
        db.execute(sql, [post_id, class_name, class_value])

def remove_post(post_id):
    sql = "DELETE FROM comments WHERE post_id = ?"
    db.execute(sql, [post_id])
    sql = "DELETE FROM post_classes WHERE post_id = ?"
    db.execute(sql, [post_id])
    sql = "DELETE FROM items WHERE id = ?"
    db.execute(sql, [post_id])

def search_posts(query):
    sql = """SELECT id, title, body
            FROM items
            WHERE title LIKE ? OR body LIKE ?
            ORDER BY id DESC"""
    like = "%" + query + "%"
    return db.query(sql, [like, like])

def add_comment(commenter_id, post_id, comment):
    sql = "INSERT INTO comments (commenter_id, post_id, comment) VALUES (?, ?, ?)"
    db.execute(sql, [commenter_id, post_id, comment])

def get_comments(post_id):
    sql = """SELECT c.id, c.commenter_id, c.comment, u.username, u.id
            FROM comments c
            LEFT JOIN users u ON c.commenter_id = u.id
            WHERE c.post_id = ? """
    return db.query(sql, [post_id])

def save_post(post_id, ):
    sql = "INSERT INTO saved (post_id, saver_id) VALUES (?, ?)"
    db.execute(sql, [post_id, ])

def get_all_classes():
    sql = "SELECT name, value FROM classes"
    result = db.query(sql)

    classes = {}
    for name, value in result:
        classes[name] = []
    for name, value in result:
        classes[name].append(value)

    return classes

def get_post_classes(post_id):
    sql = "SELECT name, value FROM post_classes WHERE post_id = ?"
    return db.query(sql, [post_id])