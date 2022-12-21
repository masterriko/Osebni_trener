
def naredi_tabele(conn):
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS 
            uporabnik(uid INTEGER PRIMARY KEY,
                      email TEXT, 
                      polno_ime TEXT
                      )             
        """
        )
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sledilec(
                zacetek INTEGER,
                tarca INTEGER,
                razlog TEXT,
                FOREIGN KEY(zacetek) REFERENCES uporabnik(uid),
                FOREIGN KEY(tarca) REFERENCES uporabnik(uid)
            )
        """)

def napolni_podatke(conn):
    uporabniki = [
        ("koprivec.filip@gmail.com", "Filip"),
        ("koprivec1.filip@gmail.com", "Filip 1"),
        ("koprivec.filip2@gmail.com", "Filip 2"),
    ]
    with conn:
        
        for email, name in uporabniki:
            conn.execute("""
    INSERT INTO uporabnik(email, polno_ime) VALUES
    (?, ?) """, [email, name])

def pripravi_bazo(conn):
    with conn:
        cur = conn.execute("SELECT COUNT(*) FROM sqlite_master")
        if cur.fetchone() != (0, ):
            return
    naredi_tabele(conn)
    napolni_podatke(conn)
