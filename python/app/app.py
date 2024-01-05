from flask import Flask, render_template, redirect, request, jsonify,url_for
from flask_sqlalchemy import SQLAlchemy
import os
import hashlib
import flask_login

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@mysql/tech'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Utente(db.Model):
    __tablename__ = 'utente'

    USERNAME = db.Column(db.String(80), primary_key=True)
    NOME = db.Column(db.String(80))
    COGNOME = db.Column(db.String(80))
    MAIL = db.Column(db.String(255))
    PASSWORD = db.Column(db.String(255))
    DATA = db.Column(db.Date)
    RUOLO=db.Column(db.String(80))

class Film(db.Model):
    __tablename__ = 'film'

    COD_FILM = db.Column(db.Integer, primary_key=True)
    NOME_FILM = db.Column(db.String(80))
    DESCRIZIONE = db.Column(db.String(300))
    ANNO=db.Column(db.Integer)

class Categoria(db.Model):
    __tablename__ = 'categoria'

    ID_CATEGORIA = db.Column(db.Integer, primary_key=True)
    NOME_CATEGORIA = db.Column(db.String(80))

class CategorieDiFilm(db.Model):
    __tablename__ = 'categorie_di_film'

    ID_CATEGORIA = db.Column(db.Integer, db.ForeignKey('categoria.ID_CATEGORIA'), primary_key=True)
    COD_FILM = db.Column(db.Integer, db.ForeignKey('film.COD_FILM'), primary_key=True)

class Recensioni(db.Model):
    __tablename__ = 'recensioni'

    COD_FILM = db.Column(db.Integer, db.ForeignKey('film.COD_FILM'), primary_key=True)
    USERNAME = db.Column(db.String(80), db.ForeignKey('utente.USERNAME'), primary_key=True)
    VALUTAZIONE = db.Column(db.Float, db.CheckConstraint('VALUTAZIONE IN (0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5)'))

@app.route('/test')
def index():
    utente_trovato = Utente.query.filter_by(USERNAME="Codino").first().USERNAME
    film_trovato = Film.query.filter_by(COD_FILM=1).first().COD_FILM

    if utente_trovato and film_trovato :
        cod_film = film_trovato
        return str(cod_film)  # Converti l'intero in una stringa prima di restituirlo
    else:
        return "Film non trovato"

@app.route('/inserimento', methods=['POST'])
def inserimento():
    data = request.get_json()

    # Esempio: salvare i dati ricevuti dal frontend nel modo desiderato
    username = data.get('username')
    nome = data.get('nome')
    cognome = data.get('cognome')
    email = data.get('email')
    password = data.get('password')
    date = data.get('date')
    #ruolo =data.get('ruolo')
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

     # Creazione di un nuovo utente
    nuovo_utente = Utente(
        USERNAME=username,
        NOME=nome,
        COGNOME=cognome,
        MAIL=email,
        PASSWORD=hashed_password,
        DATA=date,
        RUOLO="UTENTE"
    )

    # Aggiunta dell'utente al database e commit delle modifiche
    try:    
        db.session.add(nuovo_utente)
        db.session.commit()
        return jsonify(success=True)
    except Exception as e:  # 'Exception' dovrebbe essere minuscolo
        return jsonify(success=False, error=str(e))  # Ritorno di un messaggio d'errore come risposta JSON

@app.route('/film', methods=['POST'])
def inserimento_film():
    data = request.get_json()
    cod_film=data.get('cod_film')
    nome_film = data.get('nome_film')
    descrizione = data.get('descrizione')

    # Creazione di un nuovo film
    nuovo_film = Film(COD_FILM=cod_film,NOME_FILM=nome_film, DESCRIZIONE=descrizione)

    try:
        # Aggiunta del film al database e commit delle modifiche
        db.session.add(nuovo_film)
        db.session.commit()
        return jsonify(success=True)
    except Exception as e:  # 'Exception' dovrebbe essere minuscolo
        return jsonify(success=False, error=str(e))  # Ritorno di un messaggio d'errore come risposta JSON

@app.route('/categoria', methods=['POST'])
def inserimento_categoria():
    data = request.get_json()
    id_cat=data.get('id_cat')
    nome_categoria = data.get('nome_categoria')

    # Creazione di una nuova categoria
    nuova_categoria = Categoria(ID_CATEGORIA=id_cat,NOME_CATEGORIA=nome_categoria)

    # Aggiunta della categoria al database e commit delle modifiche
    try:
        db.session.add(nuova_categoria)
        db.session.commit()
        return jsonify(success=True)
    except Exception as e:  # 'Exception' dovrebbe essere minuscolo
        return jsonify(success=False, error=str(e))  # Ritorno di un messaggio d'errore come risposta JSON

@app.route('/recensione', methods=['POST'])
def inserimento_recensione():
    data = request.get_json()

    cod_film = data.get('cod_film')
    username = data.get('username')
    valutazione = data.get('valutazione')
    valutazione = float(valutazione)

    # Creazione di una nuova recensione
    nuova_recensione = Recensioni(COD_FILM=cod_film, USERNAME=username, VALUTAZIONE=valutazione)
    if Utente.query.filter_by(USERNAME=username).first().USERNAME and str(Film.query.filter_by(COD_FILM=cod_film).first().COD_FILM) and 0.5 <= valutazione <= 5:
    # Aggiunta della recensione al database e commit delle modifiche
        try:
            db.session.add(nuova_recensione)
            db.session.commit()
            return jsonify(success=True)
        except Exception as e:  # 'Exception' dovrebbe essere minuscolo
            return jsonify(success=False, error=str(e))  # Ritorno di un messaggio d'errore come risposta JSON
    else:
        return jsonify(success=False, error="Condizioni non soddisfatte")
    
@app.route('/categoria_film', methods=['POST'])
def inserimento_categoria_film():
    data = request.get_json()

    id_categoria = data.get('id_categoria')
    cod_film = data.get('cod_film')

    # Creazione di una nuova categoria di film
    nuova_categoria_film = CategorieDiFilm(ID_CATEGORIA=id_categoria, COD_FILM=cod_film)
    if str(Categoria.query.filter_by(ID_CATEGORIA=id_categoria).first) and str(Film.query.filter_by(COD_FILM=cod_film).first):
    # Aggiunta della categoria di film al database e commit delle modifiche
        try:
            db.session.add(nuova_categoria_film)
            db.session.commit()
            return jsonify(success=True)
        except Exception as e:  # 'Exception' dovrebbe essere minuscolo
            return jsonify(success=False, error=str(e))  # Ritorno di un messaggio d'errore come risposta JSON
    else:
        return jsonify(success=False, error="Condizioni non soddisfatte")

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()

        username = data.get('name')
        password = data.get('password')
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
            # Controlla se l'utente esiste nel database
        user = Utente.query.filter_by(USERNAME=username).first().USERNAME
        p = Utente.query.filter_by(USERNAME=username).first().PASSWORD
        if user==username and p==hashed_password:
            return jsonify({'user': user})
            #return render_template('nuovo.html', user=user)  # Passaggio di 'user' al template search.html
        else:
            # Se il login non è avvenuto con successo, potresti mostrare un messaggio di errore
            return jsonify(success=False, error="Condizioni non soddisfatte")
    except Exception as e:
        print(str(e))  # Stampare l'errore per debug
        return jsonify({'error': 'Si è verificato un errore interno'}), 500

@app.route('/search', methods=['GET'])
def search_movie():
    try:
        nome=request.args.get('nome')

        film=Film.query.filter_by(NOME_FILM=nome).first()
        #results = Film.query.filter(Film.NOME_FILM.like(f'%{nome}%')).all()
            # Se presente nel db allora presente anche nella cartella uploads
        if film:
            film_serialized = {'COD_FILM': film.COD_FILM, 'NOME_FILM': film.NOME_FILM,'DESCRIZIONE': film.DESCRIZIONE, 'ANNO': film.ANNO}  # Converti l'oggetto in un dizionario
            return jsonify({'film': film_serialized})
            #return render_template('search.html', film=film)  # Passaggio di 'film' al template search.html
        else:
            return jsonify({'film non trovato'})
    except Exception as e:
        print(str(e))  # Stampare l'errore per debug
        return jsonify({'error': 'Si è verificato un errore interno'}), 500


@app.route('/films', methods=['GET'])
def get_all_films():
    try:
        films = Film.query.all()  # Ottieni tutti i film dalla tabella

        # Serializza la lista dei film in un formato comprensibile per la risposta JSON
        serialized_films = [{
            'COD_FILM': film.COD_FILM,
            'NOME_FILM': film.NOME_FILM,
            'DESCRIZIONE': film.DESCRIZIONE,
            'ANNO': film.ANNO
        } for film in films]

        return jsonify({'films': serialized_films})  # Restituisci la lista di film in formato JSON
    except Exception as e:
        print(str(e))  # Stampa l'errore per il debug
        return jsonify({'error': 'Si è verificato un errore interno'}), 500
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=1200)