import unittest
from models.author import Author
from models.article import Article
from models.magazine import Magazine
from database.setup import create_tables
from database.connection import get_db_connection

class TestModels(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        
        create_tables()
    
    def setUp(self):
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM articles')
        cursor.execute('DELETE FROM authors')
        cursor.execute('DELETE FROM magazines')
        conn.commit()
        conn.close()

    def test_author_creation(self):
        author = Author("John Doe")
        self.assertEqual(author.name, "John Doe")
        self.assertIsInstance(author.id, int)
    
    def test_article_creation(self):
        author = Author("John Doe")
        magazine = Magazine("Tech Weekly", "Technology")
        article = Article(author, magazine, "Test Title")
        self.assertEqual(article.title, "Test Title")
    
    def test_magazine_creation(self):
        magazine = Magazine("Tech Weekly", "Technology")
        self.assertEqual(magazine.name, "Tech Weekly")
        self.assertEqual(magazine.category, "Technology")

    def test_author_articles(self):
        author = Author("John Doe")
        magazine = Magazine("Tech Weekly", "Technology")
        Article(author, magazine, "Test Title")
        articles = author.articles()
        self.assertTrue(len(articles) > 0)
        self.assertEqual(articles[0]['title'], "Test Title")

    def test_author_magazines(self):
        author = Author("John Doe")
        magazine1 = Magazine("Tech Weekly", "Technology")
        magazine2 = Magazine("Science Monthly", "Science")
        Article(author, magazine1, "Tech Article")
        Article(author, magazine2, "Science Article")
        magazines = author.magazines()
        self.assertTrue(len(magazines) > 0)
        magazine_names = [mag['name'] for mag in magazines]
        self.assertIn("Tech Weekly", magazine_names)
        self.assertIn("Science Monthly", magazine_names)

    def test_magazine_articles(self):
        author = Author("John Doe")
        magazine = Magazine("Tech Weekly", "Technology")
        Article(author, magazine, "Test Title")
        articles = magazine.articles()
        self.assertTrue(len(articles) > 0)
        self.assertEqual(articles[0]['title'], "Test Title")
    
    def test_magazine_contributors(self):
        author1 = Author("John Doe")
        author2 = Author("Jane Smith")
        magazine = Magazine("Tech Weekly", "Technology")
        Article(author1, magazine, "Tech Article 1")
        Article(author1, magazine, "Tech Article 2")
        Article(author2, magazine, "Tech Article 3")
        contributors = magazine.contributors()
        self.assertTrue(len(contributors) > 0)
        contributor_names = [contributor['name'] for contributor in contributors]
        self.assertIn("John Doe", contributor_names)
        self.assertIn("Jane Smith", contributor_names)

    def test_magazine_article_titles(self):
        author = Author("John Doe")
        magazine = Magazine("Tech Weekly", "Technology")
        Article(author, magazine, "Test Title 1")
        Article(author, magazine, "Test Title 2")
        titles = magazine.article_titles()
        self.assertTrue(len(titles) == 2)
        self.assertIn("Test Title 1", titles)
        self.assertIn("Test Title 2", titles)

    def test_magazine_contributing_authors(self):
        author1 = Author("John Doe")
        author2 = Author("Jane Smith")
        magazine = Magazine("Tech Weekly", "Technology")
        Article(author1, magazine, "Tech Article 1")
        Article(author1, magazine, "Tech Article 2")
        Article(author2, magazine, "Tech Article 3")
        contributors = magazine.contributing_authors()


if __name__ == "__main__":
    unittest.main()
