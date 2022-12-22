import sqlite3

import naredi_bazo

conn = sqlite3.connect("baza.sqlite3")
# Nastavimo, da sledi tujim ključem
conn.execute("PRAGMA foreign_keys = ON")

naredi_bazo.pripravi_bazo(conn)

class Uporabnik:
    def __init__(self, id_uporabnika, ime, priimek, datum_rojstva, teza, uporabnisko_ime, visina, geslo, mail, spol):
        self.id_uporabnika = id_uporabnika
        self.ime = ime
        self.priimek = priimek
        self.datum_rojstva = datum_rojstva
        self.teza = teza
        self.uporabnisko_ime= uporabnisko_ime
        self.geslo = geslo
        self.mail = mail
        self.spol = spol

    def shrani_v_bazo(self):
        if self.mail is not None:
            with conn:
                conn.execute("""
                UPDATE Uporabnik 
                SET id_uporabnika=?, ime=?, priimek=?, datum_rojstva=?, teza=?, uporabnisko_ime=?, visina=?, geslo=?, mail=?, spol=?           
            """, [self.id_uporabnika, self.ime, self.priimek, self.datum_rojstva, self.teza, self.uporabnisko_ime, self.visina, self.geslo, self.mail, self.spol])
        else:
            with conn:
                cursor = conn.execute("""
                INSERT INTO uporabnik (ime, priimek, datum_rojstva)
                VALUES (?, ?)                 
                """, [self.email, self.polno_ime])
                self.uid = cursor.lastrowid
            
    @staticmethod
    def dobi_uporabnika(email):
        with conn:
            cursor = conn.execute("""
                SELECT uid, email, polno_ime 
                FROM uporabnik
                WHERE email=?
            """, [email])
            podatki = cursor.fetchone()
            
            return Uporabnik(podatki[0], podatki[1], podatki[2])
     
    @staticmethod
    def dobi_uporabnika_z_idjem(uid):
        with conn:
            cursor = conn.execute("""
                SELECT uid, email, polno_ime 
                FROM uporabnik
                WHERE uid=?
            """, [uid])
            podatki = cursor.fetchone()
            
            return Uporabnik(podatki[0], podatki[1], podatki[2])
      
    @staticmethod
    def dobi_uporabnike_med_idji(od, do):
        print(od, do)
        with conn:
            cursor = conn.execute("""
                SELECT uid, email, polno_ime 
                FROM uporabnik
                WHERE ? <= uid AND uid <= ?
            """, [od, do])
            podatki = list(cursor.fetchall())
            
            return [
                Uporabnik(pod[0], pod[1], pod[2])
                for pod in podatki
            ]
        return []
      
        
    @staticmethod
    def dobi_vse_uporabnike():
        with conn:
            cursor = conn.execute("""
                SELECT uid, email, polno_ime 
                FROM uporabnik
            """)
            podatki = list(cursor.fetchall())
            
            return [
                Uporabnik(pod[0], pod[1], pod[2])
                for pod in podatki
            ]
        return []
            
    #def dobi_moje_tarce(self):
    #    with conn:
    #        cursor = conn.execute("""
    #            SELECT uid, email, polno_ime FROM 
    #            uporabnik INNER JOIN
    #            sledilec ON uporabnik.uid = sledilec.tarca
    #            WHERE 
    #            zacetek = ?
    #            """, [self.uid]
    #        )   
    #        podatki = list(cursor.fetchall())
    #        
    #        return [
    #            Uporabnik(pod[0], pod[1], pod[2])
    #            for pod in podatki
    #        ]       
    
    #def dobi_sledilce(self):
    #    with conn:
    #        cursor = conn.execute("""
    #            SELECT uid, email, polno_ime FROM 
    #            uporabnik INNER JOIN
    #            sledilec ON uporabnik.uid = sledilec.zacetek
    #            WHERE 
    #            tarca = ?
    #            """, [self.uid]
    #        )   
    #        podatki = list(cursor.fetchall())
    #        
    #        return [
    #            Uporabnik(pod[0], pod[1], pod[2])
    #            for pod in podatki
    #        ]
