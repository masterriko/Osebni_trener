import bottle 
import model

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
    uporabnik = model.Uporabnik(ime, priimek, datum_rojstva, teza, visina, geslo, mail, spol)
    uporabnik.shrani_v_bazo()
    bottle.redirect("/login")

@bottle.get("/home")    
def get_home():                   
    return bottle.template("home.html")

@bottle.get("/food")    
def get_food():   
    ime_hrane = model.Zivilo.dobi_imena_vseh_zivil()                
    return bottle.template("food.html", hrana = ime_hrane)

@bottle.post("/food")  
def add_food():
    zivilo = None
    ime_zivila = bottle.request.forms.get('ime_zivila')
    cas_obroka = bottle.request.forms.get('cas_obroka')
    kolicina = bottle.request.forms.get("kolicina")
    vrsta_obroka = bottle.request.forms.get("vrsta_obroka")
    obrok = model.Obrok("Zajtrk", cas_obroka)
    if not obrok.preveri_zivilo(ime_zivila):
        prikaz = model.Obrok.prikazi_mozna(ime_zivila) #tole naj se prikaze, da lahko gor klikne uporabnik
    else:
        zivilo = model.Zivilo.dodaj_zivilo()

@bottle.get("/test")    
def get_food():   
    ime_hrane = model.Zivilo.dobi_imena_vseh_zivil()                
    return bottle.template("test.html", hrana = ime_hrane)

@bottle.get("/activity")  
def get_activity():
    return bottle.template("activity.html")

@bottle.post("/activity")  
def add_activity():
    return -1
    #Tukaj napiši katere podatke rabiš za bazo


bottle.run(debug=True, reloader=True)
