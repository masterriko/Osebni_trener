import sqlite3

import naredi_bazo

conn = sqlite3.connect("baza.sqlite3")
# Nastavimo, da sledi tujim ključem
conn.execute("PRAGMA foreign_keys = ON")

naredi_bazo.pripravi_bazo(conn)

class Uporabnik:
    def __init__(self, uid, email, polno_ime):
        self.uid = uid
        self.email = email
        self.polno_ime = polno_ime
        
    def shrani_v_bazo(self):
        if self.uid is not None:
            with conn:
                conn.execute("""
                UPDATE uporabnik 
                SET email=?, polno_ime=?
                WHERE uid=?                 
            """, [self.email, self.polno_ime, self.uid])
        else:
            with conn:
                cursor = conn.execute("""
                INSERT INTO uporabnik (email, polno_ime)
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
            
    def dobi_moje_tarce(self):
        with conn:
            cursor = conn.execute("""
                SELECT uid, email, polno_ime FROM 
                uporabnik INNER JOIN
                sledilec ON uporabnik.uid = sledilec.tarca
                WHERE 
                zacetek = ?
                """, [self.uid]
            )   
            podatki = list(cursor.fetchall())
            
            return [
                Uporabnik(pod[0], pod[1], pod[2])
                for pod in podatki
            ]       
    
    def dobi_sledilce(self):
        with conn:
            cursor = conn.execute("""
                SELECT uid, email, polno_ime FROM 
                uporabnik INNER JOIN
                sledilec ON uporabnik.uid = sledilec.zacetek
                WHERE 
                tarca = ?
                """, [self.uid]
            )   
            podatki = list(cursor.fetchall())
            
            return [
                Uporabnik(pod[0], pod[1], pod[2])
                for pod in podatki
            ]
