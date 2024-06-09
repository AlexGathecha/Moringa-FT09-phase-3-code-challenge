from database.connection import get_db_connection

class Article:
    def __init__(self, author, magazine, title, content=""):
        self._author_id = author.id
        self._magazine_id = magazine.id
        self._title = title
        self._content = content
        self._id = self.save()

    def save(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO articles (title, content, author_id, magazine_id) 
            VALUES (?, ?, ?, ?)
        ''', (self._title, self._content, self._author_id, self._magazine_id))
        conn.commit()
        article_id = cursor.lastrowid
        conn.close()
        return article_id

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @property
    def content(self):
        return self._content

    @property
    def author_id(self):
        return self._author_id

    @property
    def magazine_id(self):
        return self._magazine_id

    def author(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM authors WHERE id = ?', (self._author_id,))
        author = cursor.fetchone()
        conn.close()
        return author

    def magazine(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM magazines WHERE id = ?', (self._magazine_id,))
        magazine = cursor.fetchone()
        conn.close()
        return magazine

    def __repr__(self):
        return f'<Article {self.title}>'
