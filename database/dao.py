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
        query = """SELECT LEAST(c.id_rifugio1, c.id_rifugio2) as r1, 
                    GREATEST (c.id_rifugio1, c.id_rifugio2) as r2, 
                    c.distanza, c.difficolta 
                    FROM connessione as c 
                    WHERE c.anno <= %s """
        cursor.execute(query, (year,))
        for row in cursor:
            r1 = row['r1']
            r2 = row['r2']
            distanza = row['distanza']
            difficolta = row['difficolta']

            if difficolta == "facile":
                fattore = 1
            elif difficolta == "media":
                fattore = 1.5
            elif difficolta == "difficile":
                fattore = 2
            else:
                fattore = 1
            peso = distanza * fattore
            results.append(Sentieri(r1, r2, peso))
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

