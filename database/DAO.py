from database.DB_connect import DBConnect
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass


    @staticmethod
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append(
                    State(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_sightings():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from sighting s 
                    order by `datetime` asc """
            cursor.execute(query)

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getMaxMinLat():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT MIN(s.lat), MAX(s.lat)
                    FROM state s """
            cursor.execute(query)

            for row in cursor:
                result.append( (row["MIN(s.lat)"], row["MAX(s.lat)"]) )
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getMaxMinLng():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT MIN(s.Lng), MAX(s.Lng)
                        FROM state s """
            cursor.execute(query)

            for row in cursor:
                result.append((row["MIN(s.Lng)"], row["MAX(s.Lng)"]))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllForme():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT DISTINCT s.shape 
                        FROM sighting s 
                        WHERE s.shape is not NULL and s.shape != "" AND s.shape != "unknown"
                        GROUP BY s.shape
                        ORDER BY s.shape DESC"""
            cursor.execute(query)

            for row in cursor:
                result.append(row["shape"])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllNodi(lat, lng, forma):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT DISTINCT s.*
                        FROM state s, sighting sg
                        WHERE s.Lat > %s AND s.Lng > %s AND sg.shape = %s
                        AND s.id = sg.state """
            cursor.execute(query, (lat, lng, forma))

            for row in cursor:
                result.append(State(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllVicini():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT *
                    FROM neighbor n """
            cursor.execute(query,)

            for row in cursor:
                result.append( (row["state1"], row["state2"]) )
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getCalcolaPeso(stato, forma):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT SUM(s.duration)
                FROM sighting s 
                WHERE s.state = %s AND S.shape = %s"""
            cursor.execute(query, (stato,forma))

            for row in cursor:
                result.append(row["SUM(s.duration)"])
            cursor.close()
            cnx.close()
        return result









