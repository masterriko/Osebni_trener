import sqlite3

import naredi_bazo
import re
 
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+.[A-Z|a-z]{2,}\b'

conn = sqlite3.connect("osebni_trener.sqlite3")
# Nastavimo, da sledi tujim ključem
conn.execute("PRAGMA foreign_keys = ON")

naredi_bazo.pripravi_bazo()

class Uporabnik:
    def __init__(self, ime, priimek, datum_rojstva, teza, uporabnisko_ime, visina, geslo, mail, spol):
        #self.id_uporabnika = stevilo_uporabnikov("osebni_trener.sqlite3") + 1
        self.ime = ime
        self.priimek = priimek
        self.datum_rojstva = datum_rojstva
        self.teza = teza
        self.uporabnisko_ime= uporabnisko_ime
        self.geslo = geslo
        self.mail = mail
        self.spol = spol
        self.visina = visina
    def email_je_ze_v_uporabi(self):
        '''Preverimo ali je mail že v uporabi'''
        with conn:
            cursor = conn.execute("SELECT 1 FROM uporabnik WHERE mail = ?", [self.mail])
            return bool(cursor.fetchone())

    def shrani_v_bazo(self):
        if not self.email_je_ze_v_uporabi():
            with conn:
                conn.execute("""
                UPDATE Uporabnik 
                SET id_uporabnika=?, ime=?, priimek=?, datum_rojstva=?, teza=?, uporabnisko_ime=?, visina=?, geslo=?, mail=?, spol=?           
            """, [self.id_uporabnika, self.ime, self.priimek, self.datum_rojstva, self.teza, self.uporabnisko_ime, self.visina, self.geslo, self.mail, self.spol])
        else:
            print("Email naslov je že v uporabi.")
       
    @staticmethod
    def dobi_uporabnika(mail):
        with conn:
            cursor = conn.execute("""
                SELECT uid, email, polno_ime 
                FROM uporabnik
                WHERE mail=?
            """, [email])
            podatki = cursor.fetchone()
            
            return Uporabnik(podatki[0], podatki[1], podatki[2])

    @staticmethod
    def preveri_mail_in_geslo(mail, geslo):
        if mail != None and check(mail):
            with conn:
                cursor = conn.execute("""
                    SELECT geslo
                    FROM uporabnik
                    WHERE mail=?
                """, [mail])
                preveri = cursor.fetchone()
            return preveri == geslo
        return False

    @staticmethod
    def dobi_uporabnika_z_idjem(uid):
        with conn:
            cursor = conn.execute("""
                SELECT uid, mail, polno_ime 
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
                SELECT uid, mail, polno_ime 
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
                SELECT uid, mail, polno_ime 
                FROM uporabnik
            """)
            podatki = list(cursor.fetchall())
            
            return [
                Uporabnik(pod[0], pod[1], pod[2])
                for pod in podatki
            ]
        return []
            
def check(mail):
    return re.fullmatch(regex, mail)

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

    
class Dnevni_vnos:
    def __init__(self, id_dnevnika, datum, uporabnik):
        self.id_dnevnika = id_dnevnika
        self.datum = datum
        self.uporabnik = uporabnik.id_uporabnika
class Pocutje:
    def __init__(self, id_pocutja, ocena):
        self.id_pocutja = id_pocutja
        self.ocena = ocena
    def shrani_v_bazo(self):
        if self.ocena is not None:
            with conn:
                conn.execute("""
                UPDATE Pocutje 
                SET id_pocutja=?, ocena=?           
            """, [self.id_pocutja, self.ocena])
        else:
            with conn:
                cursor = conn.execute("""
                INSERT INTO Pocutje (ocena)
                VALUES (?)                 
                """, [self.ocena])
                self.uid = cursor.lastrowid
class Rekreacija:
    def __init__(self, id_rekreacije, srcni_utrip, stevilo_korakov, cas_izvedbe, cas_vadbe_min):
        self.id_rekreacije = id_rekreacije
        self.srcni_utrip = srcni_utrip
        self.stevilo_korakov = stevilo_korakov
        self.cas_izvedbe = cas_izvedbe
        self.cas_vadbe_min = cas_vadbe_min
    def shrani_v_bazo(self):
        with conn:
            cursor = conn.execute("""
            INSERT INTO Rekreacija (srcni_utrip, stevilo_korakov, cas_izvedbe, cas_vadbe_min)
            VALUES (?, ?, ?, ?)                 
            """, [self.srcni_utrip, self.stevilo_korakov, self.cas_izvedbe, self.cas_vadbe_min])
            self.uid = cursor.lastrowid
class Aktivnost:
    def __init__(self, id_aktivnosti, tip, poraba_kalorij):
        self.id_aktivnosti = id_aktivnosti
        self.tip = tip
class Obrok:
    def __init__(self, id_obroka, cas_obroka):
        self.cas_obroka = cas_obroka
    def shrani_v_bazo(self):
        with conn:
            cursor = conn.execute("""
            INSERT INTO Obrok (cas_obroka)
            VALUES (?)                 
            """, [self.cas_obroka])
            self.uid = cursor.lastrowid
class Zivilo:
    def __init__(self, id_zivila, je_tekocina, ogljikovi_hidrati, ime, vlaknine_mg, kalorije_kcal, beljakovine):
        ##Tukaj uporabiva Ninja API in nato se sklicujeva iz tega classa za ostale tabele.
        self.id_zivila = id_zivila
        self.je_tekocina = je_tekocina
        self.ogljikovi_hidrati = ogljikovi_hidrati
        self.ime = ime
        self.vlaknine_mg = vlaknine_mg
        self.kalorije_kcal = kalorije_kcal
        self.beljakovine = beljakovine
    def shrani_v_bazo(self):
        if self.id_zivilo is not None:
            with conn:
                conn.execute("""
                UPDATE Zivilo
                SET id_zivila=?, je_tekocija=?, ogljikovi_hidrati=?, ime=?, vlaknine_mg=?, kalorije_kcal=?, beljakovine=?            
            """, [self.id_zivila, self.je_tekocina, self.ogljikovi_hidrati, self.ime, self.vlaknine_mg, self.kalorije_kcal, self.beljakovine])
        else:
            with conn:
                cursor = conn.execute("""
                INSERT INTO Zivilo (je_tekocina, ogljikovi_hidrati, , cas_vadbe_min)
                VALUES (?, ?, ?, ?)                 
                """, [self.ocena])
                self.uid = cursor.lastrowid
class Minerali:
    def __init__(self, id_minerali, pdv, ime_minerali): 
        self.id_minerali = id_minerali
        self.pdv = pdv
        self.ime_minerali = ime_minerali
    def shrani_v_bazo(self):
        with conn:
            cursor = conn.execute("""
            INSERT INTO Minerali (pdv, ime_minerali)
            VALUES (?, ?)                 
            """, [self.pdv, self.ime_minerali])
            self.uid = cursor.lastrowid
class Vitamini:
    def __init__(self, id_vitamini, pdv, ime_vitamini):
        self.id_vitamini = id_vitamini
        self.pdv = pdv
        self.ime_vitamini = ime_vitamini
    def shrani_v_bazo(self):
        with conn:
            cursor = conn.execute("""
            INSERT INTO Vitamini (pdv, ime_vitamini)
            VALUES (?, ?)                 
            """, [self.pdv, self.ime_vitamini])
            self.uid = cursor.lastrowid
class Mascobe:
    def __init__(self, id_mascobe, pdv, ime_mascobe):
        self.id_mascobe = id_mascobe
        self.pdv = pdv
        self.ime_mascobe = ime_mascobe
    def shrani_v_bazo(self):
        with conn:
            cursor = conn.execute("""
            INSERT INTO Mascobe (pdv, ime_mascobe)
            VALUES (?, ?)                 
            """, [self.pdv, self.ime_mascobe])
            self.uid = cursor.lastrowid