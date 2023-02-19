import bottle 
import model

@bottle.route('/static/css/<filename:re:.*\.css>')
def send_css(filename):
    return bottle.static_file(filename, root='static/css')

@bottle.route('/static/img/<filename:re:.*\.png>')
def send_img(filename):
    return bottle.static_file(filename, root='static/img')
    
@bottle.get("/login")    
@bottle.get("/")    
def get_login():                   
    return bottle.template("login.html")

@bottle.post("/login") 
@bottle.post("/") 
def log_in():
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
def add_user():
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
    return bottle.template("food.html")

@bottle.post("/food")  
def add_food():
    return -1
    #Tukaj napiši katere podatke rabiš za bazo

@bottle.get("/activity")  
def add_activity():
    return bottle.template("activity.html")

@bottle.post("/activity")  
def add_activity():
    return -1
    #Tukaj napiši katere podatke rabiš za bazo


bottle.run(debug=True, reloader=True)
