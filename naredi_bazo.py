import sqlite3
import pandas as pd
db = sqlite3.connect("osebni_trener.db")

df1 = pd.read_csv(r'data/modified.csv')
hranila = []
for col in df1.columns:
    hranila.append(col) #hranila vsebuje imena stolpcev, dolzina je 77

df2 = pd.read_csv(r'data/exercise_dataset.csv')

def pripravi_bazo(): 
    with db as cursor:
        # Uporabnik (#1)
        cursor.execute(""" CREATE TABLE IF NOT EXISTS Uporabnik
            (
                id_uporabnika INTEGER PRIMARY KEY AUTOINCREMENT,
                ime TEXT,
                priimek TEXT,
                datum_rojstva DATE NOT NULL,
                teza INTEGER NOT NULL,
                uporabnisko_ime TEXT NOT NULL,
                visina INTEGER NOT NULL,
                geslo VARCHAR(255) NOT NULL,
                mail TEXT NOT NULL,
                spol SMALLINT NOT NULL
            );""")
        # Dnevni vnos (#2)
        cursor.execute("""CREATE TABLE IF NOT EXISTS Dnevni_vnos
            (
                id_dnevnika INTEGER PRIMARY KEY,
                datum DATE NOT NULL,
                id_uporabnika INTEGER NOT NULL,
                id_pocutja INTEGER NOT NULL,
                FOREIGN KEY (id_uporabnika) REFERENCES Uporabnik(id_uporabnika)
            );""")

        # Pocutje (#3)
        cursor.execute("""CREATE TABLE IF NOT EXISTS Pocutje
            (
                id_pocutja INTEGER PRIMARY KEY,
                id_dnevni_vnos INTEGER,
                ocena INTEGER NOT NULL,
                FOREIGN KEY (id_dnevni_vnos) REFERENCES Dnevni_vnos(id_dnevnika) 
            );""")

        # Rekreacija (#4)
        cursor.execute("""CREATE TABLE IF NOT EXISTS Rekreacija
            (
                id_rekreacije INTEGER PRIMARY KEY,
                srcni_utrip INTEGER NOT NULL,
                stevilo_korakov INTEGER NOT NULL,
                cas_izvedbe TIME NOT NULL,
                cas_vadbe_min TIME,
                id_aktivnost INTEGER,
                FOREIGN KEY (id_aktivnost) REFERENCES Aktivnost(id_aktivnost)
            );""")

        # Aktivnost (#5)
        cursor.execute("""CREATE TABLE IF NOT EXISTS Aktivnost
            (
                id_aktivnosti INTEGER PRIMARY KEY NOT NULL,
                tip TEXT NOT NULL,
                poraba_kalorij_na_kg DECIMAL NOT NULL
            );""")

        # Obrok (#6)
        cursor.execute("""CREATE TABLE IF NOT EXISTS Obrok
            (
                id_obroka INTEGER PRIMARY KEY NOT NULL,
                ime_obroka TEXT NOT NULL,
                cas_obroka TIME NOT NULL,
                id_dnevni_vnos INTEGER,
                FOREIGN KEY (id_dnevni_vnos) REFERENCES Dnevni_vnos(id_dnevnika)
            );""")

        # Zivilo (#7)
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS Zivilo
            (   id_zivila INTEGER PRIMARY KEY,
                {hranila[0]}  TEXT NOT NULL,
                {hranila[1]}  TEXT NOT NULL,
                {hranila[2]}  TEXT NOT NULL,
                {hranila[3]}  TEXT NOT NULL,
                {hranila[4]}  TEXT NOT NULL,
                {hranila[5]}  TEXT NOT NULL,
                {hranila[6]}  TEXT NOT NULL,
                {hranila[7]}  TEXT NOT NULL,
                {hranila[8]}  TEXT NOT NULL,
                {hranila[9]}  TEXT NOT NULL,
                {hranila[10]} TEXT NOT NULL,
                {hranila[11]} TEXT NOT NULL,
                {hranila[12]} TEXT NOT NULL,
                {hranila[13]} TEXT NOT NULL,
                {hranila[14]} TEXT NOT NULL,
                {hranila[15]} TEXT NOT NULL,
                {hranila[16]} TEXT NOT NULL,
                {hranila[17]} TEXT NOT NULL,
                {hranila[18]} TEXT NOT NULL,
                {hranila[19]} TEXT NOT NULL,
                {hranila[20]} TEXT NOT NULL,
                {hranila[21]} TEXT NOT NULL,
                {hranila[22]} TEXT NOT NULL,
                {hranila[23]} TEXT NOT NULL,
                {hranila[24]} TEXT NOT NULL,
                {hranila[25]} TEXT NOT NULL,
                {hranila[26]} TEXT NOT NULL,
                {hranila[27]} TEXT NOT NULL,
                {hranila[28]} TEXT NOT NULL,
                {hranila[29]} TEXT NOT NULL,
                {hranila[30]} TEXT NOT NULL,
                {hranila[31]} TEXT NOT NULL,
                {hranila[32]} TEXT NOT NULL,
                {hranila[33]} TEXT NOT NULL,
                {hranila[34]} TEXT NOT NULL,
                {hranila[35]} TEXT NOT NULL,
                {hranila[36]} TEXT NOT NULL,
                {hranila[37]} TEXT NOT NULL,
                {hranila[38]} TEXT NOT NULL,
                {hranila[39]} TEXT NOT NULL,
                {hranila[40]} TEXT NOT NULL,
                {hranila[41]} TEXT NOT NULL,
                {hranila[42]} TEXT NOT NULL,
                {hranila[43]} TEXT NOT NULL,
                {hranila[44]} TEXT NOT NULL,
                {hranila[45]} TEXT NOT NULL,
                {hranila[46]} TEXT NOT NULL,
                {hranila[47]} TEXT NOT NULL,
                {hranila[48]} TEXT NOT NULL,
                {hranila[49]} TEXT NOT NULL,
                {hranila[50]} TEXT NOT NULL,
                {hranila[51]} TEXT NOT NULL,
                {hranila[52]} TEXT NOT NULL,
                {hranila[53]} TEXT NOT NULL,
                {hranila[54]} TEXT NOT NULL,
                {hranila[55]} TEXT NOT NULL,
                {hranila[56]} TEXT NOT NULL,
                {hranila[57]} TEXT NOT NULL,
                {hranila[58]} TEXT NOT NULL,
                {hranila[59]} TEXT NOT NULL,
                {hranila[60]} TEXT NOT NULL,
                {hranila[61]} TEXT NOT NULL,
                {hranila[62]} TEXT NOT NULL,
                {hranila[63]} TEXT NOT NULL,
                {hranila[64]} TEXT NOT NULL,
                {hranila[65]} TEXT NOT NULL,
                {hranila[66]} TEXT NOT NULL,
                {hranila[67]} TEXT NOT NULL,
                {hranila[68]} TEXT NOT NULL,
                {hranila[69]} TEXT NOT NULL,
                {hranila[70]} TEXT NOT NULL,
                {hranila[71]} TEXT NOT NULL,
                {hranila[72]} TEXT NOT NULL,
                {hranila[73]} TEXT NOT NULL,
                {hranila[74]} TEXT NOT NULL,
                {hranila[75]} TEXT NOT NULL
            );""")
        
        # ZiviloObrok (#8):
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS ZiviloObrok
            (   id_zivila INTEGER NOT NULL,
                ime_zivila TEXT NOT NULL,
                id_obroka INTEGER NOT NULL,
                kolicina INTEGER NOT NULL,
                FOREIGN KEY (id_zivila) REFERENCES Zivilo(id_zivilo),
                FOREIGN KEY (id_obroka) REFERENCES Obrok(id_obrok)) 
                 """)

        cursor.execute(f"""CREATE TABLE IF NOT EXISTS Omejitve
            (   id_zivila INTEGER NOT NULL,
                ime_zivila TEXT NOT NULL,
                id_obroka INTEGER NOT NULL,
                kolicina INTEGER NOT NULL,
                FOREIGN KEY (id_zivila) REFERENCES Zivilo(id_zivilo),
                FOREIGN KEY (id_obroka) REFERENCES Obrok(id_obrok)) 
                 """)

def napolni_nujne_podatke(conn):
    for row in df1.itertuples():
        i = 0
        with conn: # mogoce je ena več ali ena manj
            conn.execute(f"""
            INSERT INTO Zivilo ({hranila[0]}, {hranila[1]}, {hranila[2]}, {hranila[3]}, {hranila[4]}, {hranila[5]}, {hranila[6]}, {hranila[7]}, {hranila[8]}, {hranila[9]}, {hranila[10]} , {hranila[11]} , {hranila[12]} ,{ hranila[13]} , {hranila[14]} , {hranila[15]} , {hranila[16]} , {hranila[17]} , {hranila[18]} , {hranila[19]} , {hranila[20]} , {hranila[21]} , {hranila[22]} , {hranila[23]} , {hranila[24]} , {hranila[25]} , {hranila[26]} , {hranila[27]} , {hranila[28]} ,{ hranila[29]} , {hranila[30]} , {hranila[31]} , {hranila[32]} , {hranila[33]} , {hranila[34]} , {hranila[35]} , {hranila[36]} , {hranila[37]} , {hranila[38]} , {hranila[39]} , {hranila[40]} , {hranila[41]} , {hranila[42]} , {hranila[43]} , {hranila[44]} , {hranila[45]} , {hranila[46]} , {hranila[47]} , {hranila[48]} , {hranila[49]} , {hranila[50]} , {hranila[51]} , {hranila[52]} ,{ hranila[53]} , {hranila[54]} , {hranila[55]} ,{ hranila[56]} , {hranila[57]} , {hranila[58]} ,{ hranila[59]} , {hranila[60]} , {hranila[61]} , {hranila[62]} , {hranila[63]} , {hranila[64]} , {hranila[65]} ,{hranila[66]} ,{ hranila[67]} , {hranila[68]} , {hranila[69]} , {hranila[70]} , {hranila[71]} , {hranila[72]} , {hranila[73]} , {hranila[74]}, {hranila[75]} )
            VALUES ('{row[1]}', '{row[2]}', '{row[3]}', '{row[4]}', '{row[5]}', '{row[6]}', '{row[7]}', '{row[8]}', '{row[9]}', '{row[10]}' , '{row[11]}' , '{row[12]}' , '{row[13]}' , '{row[14]}' , '{row[15]}' , '{row[16]}' , '{row[17]}' , '{row[18]}' , '{row[19]}' , '{row[20]}' , '{row[21]}' , '{row[22]}' , '{row[23]}' , '{row[24]}' , '{row[25]}' , '{row[26]}' , '{row[27]}' , '{row[28]}' , '{row[29]}' , '{row[30]}' , '{row[31]}' , '{row[32]}' , '{row[33]}' , '{row[34]}' , '{row[35]}' , '{row[36]}', '{row[37]}', '{row[38]}', '{row[39]}', '{row[40]}', '{row[41]}', '{row[42]}', '{row[43]}', '{row[44]}', '{row[45]}' , '{row[46]}' , '{row[47]}' , '{row[48]}' , '{row[49]}' , '{row[50]}' , '{row[51]}' , '{row[52]}' , '{row[53]}' , '{row[54]}' , '{row[55]}' , '{row[56]}' , '{row[57]}' , '{row[58]}' , '{row[59]}' , '{row[60]}' , '{row[61]}' , '{row[62]}' , '{row[63]}' , '{row[64]}' , '{row[65]}' , '{row[66]}' , '{row[67]}' , '{row[68]}' , '{row[69]}' , '{row[70]}', '{row[71]}', '{row[72]}', '{row[73]}', '{row[74]}', '{row[75]}', {row[76]})
                        """)
    for row in df2.itertuples():
        with conn:
            x = row[6]
            conn.execute(f""" 
            INSERT INTO Aktivnost (tip, poraba_kalorij_na_kg)
            VALUES ('{row[1]}', {row[6]})
            """)
def pripravi_vse(conn):
    pass

#pripravi_bazo()
#napolni_nujne_podatke(db)
