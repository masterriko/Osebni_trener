import sqlite3
import pandas as pd
db = sqlite3.connect("osebni_trener.db")

df1 = pd.read_csv(r'data/modified.csv')
met = []
for col in df1.columns:
    met.append(col) #met vsebuje imena stolpcev, dolzina je 77

df2 = pd.read_csv(r'data/exercise_dataset.csv')
met2 = [] #vseboval bo ime in porabo kalorij na kg
for col in df2.columns:
    met2.append(col)
    
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
                {met[0]}  TEXT NOT NULL,
                {met[1]}  TEXT NOT NULL,
                {met[2]}  TEXT NOT NULL,
                {met[3]}  TEXT NOT NULL,
                {met[4]}  TEXT NOT NULL,
                {met[5]}  TEXT NOT NULL,
                {met[6]}  TEXT NOT NULL,
                {met[7]}  TEXT NOT NULL,
                {met[8]}  TEXT NOT NULL,
                {met[9]}  TEXT NOT NULL,
                {met[10]} TEXT NOT NULL,
                {met[11]} TEXT NOT NULL,
                {met[12]} TEXT NOT NULL,
                {met[13]} TEXT NOT NULL,
                {met[14]} TEXT NOT NULL,
                {met[15]} TEXT NOT NULL,
                {met[16]} TEXT NOT NULL,
                {met[17]} TEXT NOT NULL,
                {met[18]} TEXT NOT NULL,
                {met[19]} TEXT NOT NULL,
                {met[20]} TEXT NOT NULL,
                {met[21]} TEXT NOT NULL,
                {met[22]} TEXT NOT NULL,
                {met[23]} TEXT NOT NULL,
                {met[24]} TEXT NOT NULL,
                {met[25]} TEXT NOT NULL,
                {met[26]} TEXT NOT NULL,
                {met[27]} TEXT NOT NULL,
                {met[28]} TEXT NOT NULL,
                {met[29]} TEXT NOT NULL,
                {met[30]} TEXT NOT NULL,
                {met[31]} TEXT NOT NULL,
                {met[32]} TEXT NOT NULL,
                {met[33]} TEXT NOT NULL,
                {met[34]} TEXT NOT NULL,
                {met[35]} TEXT NOT NULL,
                {met[36]} TEXT NOT NULL,
                {met[37]} TEXT NOT NULL,
                {met[38]} TEXT NOT NULL,
                {met[39]} TEXT NOT NULL,
                {met[40]} TEXT NOT NULL,
                {met[41]} TEXT NOT NULL,
                {met[42]} TEXT NOT NULL,
                {met[43]} TEXT NOT NULL,
                {met[44]} TEXT NOT NULL,
                {met[45]} TEXT NOT NULL,
                {met[46]} TEXT NOT NULL,
                {met[47]} TEXT NOT NULL,
                {met[48]} TEXT NOT NULL,
                {met[49]} TEXT NOT NULL,
                {met[50]} TEXT NOT NULL,
                {met[51]} TEXT NOT NULL,
                {met[52]} TEXT NOT NULL,
                {met[53]} TEXT NOT NULL,
                {met[54]} TEXT NOT NULL,
                {met[55]} TEXT NOT NULL,
                {met[56]} TEXT NOT NULL,
                {met[57]} TEXT NOT NULL,
                {met[58]} TEXT NOT NULL,
                {met[59]} TEXT NOT NULL,
                {met[60]} TEXT NOT NULL,
                {met[61]} TEXT NOT NULL,
                {met[62]} TEXT NOT NULL,
                {met[63]} TEXT NOT NULL,
                {met[64]} TEXT NOT NULL,
                {met[65]} TEXT NOT NULL,
                {met[66]} TEXT NOT NULL,
                {met[67]} TEXT NOT NULL,
                {met[68]} TEXT NOT NULL,
                {met[69]} TEXT NOT NULL,
                {met[70]} TEXT NOT NULL,
                {met[71]} TEXT NOT NULL,
                {met[72]} TEXT NOT NULL,
                {met[73]} TEXT NOT NULL,
                {met[74]} TEXT NOT NULL,
                {met[75]} TEXT NOT NULL
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


def napolni_nujne_podatke(conn):
    #Napolni tabelo zivilo
    for row in df1.itertuples():
        i = 0
        with conn: # mogoce je ena več ali ena manj
            conn.execute(f"""
            INSERT INTO Zivilo ({met[0]}, {met[1]}, {met[2]}, {met[3]}, {met[4]}, {met[5]}, {met[6]}, {met[7]}, {met[8]}, {met[9]}, {met[10]} , {met[11]} , {met[12]} ,{ met[13]} , {met[14]} , {met[15]} , {met[16]} , {met[17]} , {met[18]} , {met[19]} , {met[20]} , {met[21]} , {met[22]} , {met[23]} , {met[24]} , {met[25]} , {met[26]} , {met[27]} , {met[28]} ,{ met[29]} , {met[30]} , {met[31]} , {met[32]} , {met[33]} , {met[34]} , {met[35]} , {met[36]} , {met[37]} , {met[38]} , {met[39]} , {met[40]} , {met[41]} , {met[42]} , {met[43]} , {met[44]} , {met[45]} , {met[46]} , {met[47]} , {met[48]} , {met[49]} , {met[50]} , {met[51]} , {met[52]} ,{ met[53]} , {met[54]} , {met[55]} ,{ met[56]} , {met[57]} , {met[58]} ,{ met[59]} , {met[60]} , {met[61]} , {met[62]} , {met[63]} , {met[64]} , {met[65]} ,{met[66]} ,{ met[67]} , {met[68]} , {met[69]} , {met[70]} , {met[71]} , {met[72]} , {met[73]} , {met[74]}, {met[75]} )
            VALUES ('{row[1]}', '{row[2]}', '{row[3]}', '{row[4]}', '{row[5]}', '{row[6]}', '{row[7]}', '{row[8]}', '{row[9]}', '{row[10]}' , '{row[11]}' , '{row[12]}' , '{row[13]}' , '{row[14]}' , '{row[15]}' , '{row[16]}' , '{row[17]}' , '{row[18]}' , '{row[19]}' , '{row[20]}' , '{row[21]}' , '{row[22]}' , '{row[23]}' , '{row[24]}' , '{row[25]}' , '{row[26]}' , '{row[27]}' , '{row[28]}' , '{row[29]}' , '{row[30]}' , '{row[31]}' , '{row[32]}' , '{row[33]}' , '{row[34]}' , '{row[35]}' , '{row[36]}', '{row[37]}', '{row[38]}', '{row[39]}', '{row[40]}', '{row[41]}', '{row[42]}', '{row[43]}', '{row[44]}', '{row[45]}' , '{row[46]}' , '{row[47]}' , '{row[48]}' , '{row[49]}' , '{row[50]}' , '{row[51]}' , '{row[52]}' , '{row[53]}' , '{row[54]}' , '{row[55]}' , '{row[56]}' , '{row[57]}' , '{row[58]}' , '{row[59]}' , '{row[60]}' , '{row[61]}' , '{row[62]}' , '{row[63]}' , '{row[64]}' , '{row[65]}' , '{row[66]}' , '{row[67]}' , '{row[68]}' , '{row[69]}' , '{row[70]}', '{row[71]}', '{row[72]}', '{row[73]}', '{row[74]}', '{row[75]}', {row[76]})
                        """)
    for row in df2.itertuples():
        with conn:
            x = row[6]
            conn.execute(f""" 
            INSERT INTO Aktivnost (tip, poraba_kalorij_na_kg)
            VALUES ('{row[1]}', {row[6]})
            """)
