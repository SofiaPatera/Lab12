from database.DB_connect import DBConnect
from model.sentieri import Sentieri
from model.rifugio import Rifugio

class DAO:
    """
    Implementare tutte le funzioni necessarie a interrogare il database.
    """
    @staticmethod
    def leggiSentieri(year):
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """SELECT c.id, LEAST(c.id_rifugio1, c.id_rifugio2) as id_rifugio1, 
                    GREATEST (c.id_rifugio1, c.id_rifugio2) as id_rifugio2, 
                    c.distanza, c.difficolta, c.anno, c.durata
                    FROM connessione as c 
                    WHERE c.anno <= %s """
        cursor.execute(query, (year,))
        for row in cursor:
            results.append(Sentieri(**row))
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def leggiRifugio(year):
        conn = DBConnect.get_connection()
        results = []
        query = """SELECT DISTINCT r.id, r.nome, r.localita, r.altitudine, r.capienza, r.aperto
                    FROM connessione as c, rifugio as r 
                    WHERE ( c.id_rifugio1 = r.id or c.id_rifugio2 = r.id) and c.anno <= %s 
                    GROUP BY r.nome"""
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (year,))
        for row in cursor:
            results.append(Rifugio(**row))
        cursor.close()
        conn.close()
        return results

