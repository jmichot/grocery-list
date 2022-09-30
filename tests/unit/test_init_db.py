import init_db
from src.connexion import get_db_connection

class TestInitDb():

    def test_reset_db(self):
        init_db.reset_db()
        conn = get_db_connection()
        things = conn.execute("""Select * from things""").fetchall()
        things = [tuple(row) for row in things]
        assert things == [(1, 3, 'Tomates'), (2, 30, 'Feuilles')]
        conn.execute("""Insert into things (thing, quantity) values (?, ?)""", ("Test", 50))
        conn.commit()
        things = conn.execute("""Select * from things""").fetchall()
        things = [tuple(row) for row in things]
        assert things == [(1, 3, 'Tomates'), (2, 30, 'Feuilles'), (3, 50, "Test")]
        init_db.reset_db()
        things = conn.execute("""Select * from things""").fetchall()
        things = [tuple(row) for row in things]
        assert things == [(1, 3, 'Tomates'), (2, 30, 'Feuilles')]





