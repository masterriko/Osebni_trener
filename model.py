import sqlite3
import re
 
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+.[A-Z|a-z]{2,}\b'

conn = sqlite3.connect("osebni_trener.db")
# Nastavimo, da sledi tujim ključem
conn.execute("PRAGMA foreign_keys = ON")

class Uporabnik:
    def __init__(self, mail, ime = None, priimek = None, datum_rojstva = None, teza = None, visina = None, geslo = None, spol= None):
        #self.id_uporabnika = stevilo_uporabnikov("osebni_trener.sqlite3") + 1
        self.ime = ime
        self.priimek = priimek
        self.datum_rojstva = datum_rojstva
        self.teza = teza
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
        print(self.ime, self.priimek, self.datum_rojstva, self.teza, self.visina, self.geslo, self.mail, self.spol)
        if not self.email_je_ze_v_uporabi():
            with conn:
                conn.execute("""
                INSERT INTO Uporabnik(mail, ime, priimek, datum_rojstva, teza, visina, geslo, spol) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)           
            """, [self.mail, self.ime, self.priimek, self.datum_rojstva, self.teza, self.visina, self.geslo, self.spol])
        else:
            print("Email naslov je že v uporabi.")

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
            if preveri == None:
                return False
            return preveri[0] == geslo
        return False

    #def dobi_uporabnika_z_idjem(self):
    #    """Vrne id trenutnega uporabnika"""
    #    with conn:
    #        cursor = conn.execute("""
    #            SELECT id_uporabnika
    #            FROM uporabnik
    #            WHERE mail = ?
    #        """, [self.mail])
    #        podatki = cursor.fetchone()
    #        return podatki[0]
      
    #@staticmethod
    #def dobi_uporabnike_med_idji(od, do):
    #    print(od, do)
    #    with conn:
    #        cursor = conn.execute("""
    #            SELECT uid, mail, polno_ime 
    #            FROM uporabnik
    #            WHERE ? <= uid AND uid <= ?
    #        """, [od, do])
    #        podatki = list(cursor.fetchall())
    #        
    #        return [
    #            Uporabnik(pod[0], pod[1], pod[2])
    #            for pod in podatki
    #        ]
    #    return []
      
        
    #@staticmethod
    #def dobi_vse_uporabnike():
    #    with conn:
    #        cursor = conn.execute("""
    #            SELECT uid, mail, polno_ime 
    #            FROM uporabnik
    #        """)
    #        podatki = list(cursor.fetchall())
    #        
    #        return [
    #            Uporabnik(pod[0], pod[1], pod[2])
    #            for pod in podatki
    #        ]
    #    return []

            
def check(mail):
    return re.fullmatch(regex, mail)

class Dnevni_vnos:
    def __init__(self, datum, uporabnik):
        self.datum = datum
        self.uporabnik = uporabnik

    def dodaj_v_dnevni_vnos(self):
        with conn:
            cursor2 = conn.execute("""
            INSERT INTO Dnevni_vnos (datum, mail)
            VALUES (?, ?)                 
            """, [self.datum, self.uporabnik])
    ################
    @staticmethod
    def return_dnevnik(mail):
        with conn:
            cursor = conn.execute("SELECT id_dnevnika FROM Dnevni_vnos WHERE mail = ?", [mail])
            podatki = cursor.fetchone()
            return podatki[0]


class Teza:
    def __init__(self, id_teza, tehtanje):
        self.id_teza = id_teza
        self.tehtanje = tehtanje
    def shrani_v_bazo(self):
        with conn:
            cursor = conn.execute("""
            INSERT INTO Teza (tehtanje)
            VALUES (?)                 
            """, [self.tehtanje])
            self.uid = cursor.lastrowid
class Pocutje:
    def __init__(self, ocena, id_dnevnika):
        self.ocena = ocena
        self.id_dnevnika = id_dnevnika
    def shrani_v_bazo(self):
        with conn:
            cursor = conn.execute("""
            INSERT INTO Pocutje (id_dnevni_vnos, ocena)
            VALUES (?, ?)                 
            """, [self.id_dnevnika, self.ocena])
            self.uid = cursor.lastrowid

class Rekreacija:
    def __init__(self, id_aktivnosti, cas_vadbe, trajanje_vadbe_min):
        self.id_aktivnosti = id_aktivnosti
        self.cas_vadbe = cas_vadbe
        self.trajanje_vadbe_min = trajanje_vadbe_min
    #ni do konca narejeno
    def dodaj_aktivnost(self, id_dnevnika):
        with conn:
            cursor = conn.execute("SELECT id_aktivnost FROM Aktivnost WHERE id_aktivnost = ?", [self.id_aktivnosti])
            result = cursor.fetchone()
            if result != None:
                cursor = conn.execute("""
                INSERT INTO Rekreacija (cas_izvedbe, cas_vadbe_min, id_aktivnost, id_dnevni_vnos) 
                VALUES (?, ?, ?, ?)                 
                """, [self.cas_vadbe , self.trajanje_vadbe_min, self.id_aktivnosti, id_dnevnika])
            #self.uid = cursor.lastrowid


class Aktivnost:
    def __init__(self, id_aktivnosti):
        self.id_aktivnosti = id_aktivnosti
    @staticmethod
    def dobi_imena_vseh_aktivnosti():
        with conn:
            cursor = conn.execute("""
                SELECT id_aktivnost
                FROM Aktivnost
            """)
            podatki = list(cursor.fetchall())
            return podatki
        return []

class Zivilo:
    def __init__(self, id_zivilo, ime_zivilo):
        self.id_zivilo = id_zivilo
        self.ime_zivilo = ime_zivilo

    @staticmethod
    def dobi_imena_vseh_zivil():
        with conn:
            cursor = conn.execute("""
                SELECT name 
                FROM Zivilo
            """)
            podatki = list(cursor.fetchall())
            return podatki
        return []

class Obrok:
    def __init__(self, ime_obroka, cas_obroka, zivilo = []):
        self.ime_obroka = ime_obroka
        self.cas_obroka = cas_obroka
        self.zivilo = zivilo # zivilo je tabela, ki vsebuje id (oziroma ime zivila) in njegovo količino

    def dodaj_zivilo(self, ime_zivila, masa):
        """doda zivilo v obrok"""
        with conn:
            cursor = conn.execute("""
            INSERT INTO ZiviloObrok ime_zivila, kolicina
            VALUES ((SELECT name FROM Zivilo WHERE name == ? ), ?)                 
            """, [ime_zivila, masa])
            self.uid = cursor.lastrowid #for znak in ime_zivila:
