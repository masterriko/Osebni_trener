import sqlite3
import baza
#V modelu bo delal vse kar bo povezano z bazo.
conn = sqlite3.connect("osebni_trener.sqlite3") #connecti se na projekt
# TODO: Tukaj moramo ustvarit bazo, če je še ni.
baza.pripravi_vse(conn)

class Model:
    def dobi_vse_uporabnike(self):
        return ["2214142","2214142","2214142","2214142","2214142","2214142"]
        pass
#        with conn:
#            cur = conn.execute(""" 
#            SELECT * FROM Aktivnost
#            """)
#            return cur.fetchall()