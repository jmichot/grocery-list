import init_db
from src.connexion import get_db_connection
from src.dao import Dao


class TestInitDb():

    def test_reset_db(self):
        init_db.reset_db(True)
        conn = get_db_connection(True)
        things = conn.execute("""Select * from Products""").fetchall()
        things = [tuple(row) for row in things]
        assert len(things) == 0

