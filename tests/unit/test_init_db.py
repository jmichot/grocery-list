import init_db
from src.connexion import get_db_connection
from src.dao import Dao


class TestInitDb():

    def test_reset_db(self):
        init_db.reset_db(True)
        conn = get_db_connection(True)
        things = conn.execute("""Select * from Products""").fetchall()
        things = [tuple(row) for row in things]
        assert things == [(1, 3, 'Tomates'), (2, 30, 'Feuilles')]
        conn.execute("""Insert into Products (name, quantity) values (?, ?)""", ("Test", 50))
        conn.commit()
        things = conn.execute("""Select * from Products""").fetchall()
        things = [tuple(row) for row in things]
        assert things == [(1, 3, 'Tomates'), (2, 30, 'Feuilles'), (3, 50, "Test")]
        init_db.reset_db(True)
        things = conn.execute("""Select * from Products""").fetchall()
        things = [tuple(row) for row in things]
        assert things == [(1, 3, 'Tomates'), (2, 30, 'Feuilles')]

    def test_dao(self):
        init_db.reset_db(True)
        conn = get_db_connection(True)
        dao = Dao(conn)
        pr = dao.getProductById(2)
        print(pr)





