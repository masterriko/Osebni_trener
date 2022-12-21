import sqlite3

db = sqlite3.connect("osebni_trener.db")

def pripravi_bazo(): 
    with db as cursor:
        # Uporabnik (#1)
        cursor.execute(""" CREATE TABLE IF NOT EXISTS Uporabnik
            (
                id_uporabnika INTEGER PRIMARY KEY,
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
                poraba_kalorij_na_uro INTEGER NOT NULL
            );""")

        # Obrok (#6)
        cursor.execute("""CREATE TABLE IF NOT EXISTS Obrok
            (
                id_obroka INTEGER PRIMARY KEY NOT NULL,
                cas_obroka TIME NOT NULL,
                id_dnevni_vnos INTEGER,
                FOREIGN KEY (id_dnevni_vnos) REFERENCES Dnevni_vnos(id_dnevnika)
            );""")

        # Zivilo (#7)
        cursor.execute("""CREATE TABLE IF NOT EXISTS Zivilo
            (
                id_zivila INTEGER PRIMARY KEY,
                je_tekocina SMALLINT NOT NULL,
                ogljikovi_hidrati INTEGER NOT NULL,
                ime TEXT NOT NULL,
                vlaknine_mg INTEGER NOT NULL,
                kalorije_kcal INTEGER NOT NULL,
                beljakovine INTEGER NOT NULL,
                kolicina INTEGER
            );""")

        # Minerali (#8)
        cursor.execute("""CREATE TABLE IF NOT EXISTS Minerali
            (
                id INTEGER PRIMARY KEY,
                kolicina INTEGER,
                pdv INTEGER NOT NULL,
                ime_minerala TEXT
            );""")

        # Mascobe (#9)
        cursor.execute("""CREATE TABLE IF NOT EXISTS Mascobe
            (
                id_mascobe INTEGER PRIMARY KEY NOT NULL,
                pdv INTEGER NOT NULL,
                ime_mascobe TEXT
            );""")

        # Vitamini (#10)
        cursor.execute("""CREATE TABLE IF NOT EXISTS Vitamini
            (
                id INTEGER PRIMARY KEY,
                vrsta INTEGER, 
                pdv INTEGER NOT NULL,
                ime_vitamina VARCHAR(100)
            );""")

        # Obrok_Zivilo (#11)
        cursor.execute("""CREATE TABLE IF NOT EXISTS Obrok_Zivilo
            (
                id_obroka INTEGER PRIMARY KEY,
                id_zivila INTEGER NOT NULL,
                kolicina INTEGER NOT NULL,
                FOREIGN KEY (id_obroka) REFERENCES Obrok(id_obroka)
            );""")

        # Minerali_Zivilo (#12)
        cursor.execute("""CREATE TABLE IF NOT EXISTS Minerali_Zivilo
            (
                id_zivila INTEGER NOT NULL,
                id_minerali INTEGER NOT NULL,
                kolicina_mg INTEGER NOT NULL,
                FOREIGN KEY (id_zivila) REFERENCES Zivilo(id_zivila),
                FOREIGN KEY (id_minerali) REFERENCES Minerali(id)    
            );
        """)

        # Vitamini_Zivilo (#13)
        cursor.execute("""CREATE TABLE IF NOT EXISTS Vitamini_Zivilo
            (   
                id_vitamini INTEGER NOT NULL,
                id_zivilo INTEGER NOT NULL,
                kolicina_mg INTEGER NOT NULL,
                FOREIGN KEY (id_vitamini) REFERENCES Vitamini(id),
                FOREIGN KEY (id_zivilo) REFERENCES Zivilo(id_zivila)   
            );
        """)

def napolni_nujne_podatke(conn):
    with conn:
        conn.execute("""
        INSERT INTO uporabnik (username, name)
        ("email@email.com", "Neko ime)
                    """)

def pripravi_vse(conn):
    pass

pripravi_bazo()
