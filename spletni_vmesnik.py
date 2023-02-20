import bottle 
import model
import sqlite3
import datetime
conn = sqlite3.connect('osebni_trener.db')

@bottle.route('/static/css/<filename:re:.*\.css>')
def send_css(filename):
    return bottle.static_file(filename, root='static/css')

@bottle.route('/static/img/<filename:re:.*\.png>')
def send_img(filename):
    return bottle.static_file(filename, root='static/img')

@bottle.route('/static/javascript/<filename:re:.*\.js>')
def send_javascript(filename):
    return bottle.static_file(filename, root='static/javascript')
    
@bottle.get("/login")    
@bottle.get("/")    
def get_login():                   
    return bottle.template("login.html")

@bottle.post("/login") 
@bottle.post("/") 
def add_login():
    mail = bottle.request.forms.get('mail')
    geslo = bottle.request.forms.get('geslo')

    veljavnost = model.Uporabnik.preveri_mail_in_geslo(mail, geslo)
    if veljavnost:
        print("Odobren vstop")
        bottle.response.set_cookie('mail', mail, path='/')
        bottle.redirect("/home")
    else:
        print("ponovi geslo")
        bottle.redirect("/login")

@bottle.get("/signup")    
def get_signup():                   
    return bottle.template("signup.html")

@bottle.post("/signup") 
def add_signup():
    ime = bottle.request.forms.get('ime')
    priimek = bottle.request.forms.get('priimek')
    datum_rojstva = bottle.request.forms.get('datum_rojstva')
    teza = bottle.request.forms.get('teza')
    visina = bottle.request.forms.get('visina')
    geslo = bottle.request.forms.get('geslo')
    mail = bottle.request.forms.get('mail')
    spol = bottle.request.forms.get('spol')
    print(ime, priimek, datum_rojstva, teza, visina, geslo, mail, spol)
    uporabnik = model.Uporabnik(mail, ime, priimek, datum_rojstva, teza, visina, geslo, spol)
    uporabnik.shrani_v_bazo()
    date = datetime.datetime.now()
    date = date.strftime("%Y-%m-%d %H:%M:%S")
    dnevnik = model.Dnevni_vnos(date, mail)
    dnevnik.dodaj_v_dnevni_vnos()

    bottle.redirect("/login")

 
def get_user():
    '''
    Pogleda, kdo je uporabnik in vrne njegov mail.
    '''
    uporabnik_mail = bottle.request.get_cookie('mail')
    if uporabnik_mail is not None:
        return uporabnik_mail
    else:
        return None

@bottle.get("/home")    
def get_home():                   
    return bottle.template("home.html")

@bottle.get("/food")    
def get_food():   
    ime_hrane = model.Zivilo.dobi_imena_vseh_zivil()  
    uporabnik_mail = bottle.request.get_cookie('mail')              
    return bottle.template("food.html", hrana = ime_hrane)

@bottle.post("/food")  
def add_food():
    ime_zivila = bottle.request.forms.get('hrana')
    cas_obroka = bottle.request.forms.get('cas_obroka')
    vrsta_obroka = bottle.request.forms.get("vrsta_obroka")
    obrok = model.Obrok(vrsta_obroka, cas_obroka)
    if not obrok.preveri_zivilo(ime_zivila):
        prikaz = model.Obrok.prikazi_mozna(ime_zivila) #tole naj se prikaze, da lahko gor klikne uporabnik
    else:
        print("ja")
        zivilo = model.Zivilo.dodaj_zivilo()
    bottle.redirect("/food")

@bottle.get("/activity")  
def get_activity():
    ime_aktivnosti = model.Aktivnost.dobi_imena_vseh_aktivnosti()                
    return bottle.template("activity.html", aktivnost = ime_aktivnosti)


@bottle.post("/activity")  
def add_activity():
    ime_aktivnosti = bottle.request.forms.get("ime_aktivnosti")
    cas_aktivnosti = bottle.request.forms.get("cas_aktivnosti")
    trajanje_aktivnosti = bottle.request.forms.get("trajanje")
    rekreacija = model.Rekreacija(ime_aktivnosti, cas_aktivnosti, trajanje_aktivnosti)
    mail = get_user()
    id_dnevnika = model.Dnevni_vnos.return_dnevnik(mail)
    rekreacija.dodaj_aktivnost(id_dnevnika)
    bottle.redirect("/activity")

    #Tukaj napiši katere podatke rabiš za bazo

@bottle.get("/feeling")  
def get_feeling():               
    return bottle.template("feeling.html")


@bottle.post("/feeling")  
def add_feeling():
    ocena = bottle.request.forms.get("ocena")
    mail = get_user()
    date = datetime.datetime.now()
    date = date.strftime("%Y-%m-%d %H:%M:%S")
    id_dnevnika = model.Dnevni_vnos.return_dnevnik(mail)
    #dnevnik = model.Dnevni_vnos(date, mail)
    #dnevnik.dodaj_v_dnevni_vnos()
    pocutje = model.Pocutje(ocena, id_dnevnika)
    pocutje.shrani_v_bazo()
    bottle.redirect("/feeling")



bottle.run(debug=True, reloader=True)
