from flask import Flask, render_template, request, redirect,  Response, url_for
import sqlite3
from pony import orm

app = Flask(__name__)

DB = orm.Database()

class Koktel(DB.Entity):
    naziv = orm.Required(str)
    velicina = orm.Required(str)
    cijena = orm.Required(float)


class Alkohol(DB.Entity):
    naziv_alkohola = orm.Required(str)
    postotak_alkohola = orm.Required(float)


DB.bind(provider="sqlite", filename="database.sqlite", create_db=True)
DB.generate_mapping(create_tables=True)

import sqlite3

connection = sqlite3.connect('database.db')
with open('create_koktel.sql') as f:
    connection.executescript(f.read())
connection.commit()
connection.close()


@app.route('/')
def index():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    koktel = connection.execute('SELECT * FROM koktel').fetchall()
    alkohol = connection.execute('SELECT * FROM alkohol').fetchall()
    connection.close()
    return render_template ('index.html', koktel=koktel, alkohol=alkohol) 



@app.route('/koktel/delete/<int:idx>', methods=('POST',))
def delete_koktel(idx): 
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    connection.execute('DELETE FROM koktel WHERE id=?', (idx,))
    connection.commit()
    connection.close()
    return redirect('/')


@app.route('/alkohol/delete/<int:idy>', methods=('POST',))
def delete_alkohol(idy): 
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    connection.execute('DELETE FROM alkohol WHERE id=?', (idy,))
    connection.commit()
    connection.close()
    return redirect('/')


@app.route('/createkoktel', methods=('GET', 'POST'))
def create_koktel():
    if request.method == 'POST':
        titolo_kok = request.form['titolo_kok']
        sastojci_kok = request.form['sastojci_kok']
        info_kok = request.form['info_kok']
        connection = sqlite3.connect('database.db')
        connection.row_factory = sqlite3.Row
        connection.execute(
            'INSERT INTO koktel (naslov, sastojci, info) VALUES (?, ?, ?)',
            (titolo_kok, sastojci_kok, info_kok)
        )
        connection.commit()
        connection.close()
        return redirect('/')
    return render_template('createkoktel.html')


@app.route('/createalkohol', methods=('GET', 'POST'))
def create_alkohol():
    if request.method == 'POST':
        titolo_alk = request.form['titolo_alk']
        info_alk = request.form['info_alk']
        connection = sqlite3.connect('database.db')
        connection.row_factory = sqlite3.Row
        connection.execute(
            'INSERT INTO alkohol (naslov, vrste) VALUES (?, ?)',
            (titolo_alk, info_alk)
        )
        connection.commit()
        connection.close()
        return redirect('/')
    return render_template('createalkohol.html')




@app.route('/updatekoktel/<int:id>', methods=['GET', 'POST'])
def update_koktel(id):
    if request.method == 'POST':
        titolo_kok = request.form['titolo_kok']
        sastojci_kok = request.form['sastojci_kok']
        info_kok = request.form['info_kok']

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        cursor.execute('UPDATE koktel SET naslov = ?, sastojci = ?, info = ? WHERE id = ?', (titolo_kok, sastojci_kok, info_kok, id))
        connection.commit()
        connection.close()

        return redirect('/')
    
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM koktel WHERE id = ?', (id,))
    koktel = cursor.fetchone()
    connection.close()

    if koktel:
        return render_template('updatekoktel.html', koktel=koktel, id=id)
    else:
        return "Koktel nije pronađen"


@app.route('/updatealkohol/<int:id>', methods=['GET', 'POST'])
def update_alkohol(id):
    if request.method == 'POST':
        titolo_alk = request.form['titolo_alk']
        info_alk = request.form['info_alk']

        connection = sqlite3.connect('database.db')
        connection.row_factory = sqlite3.Row
        connection.execute('UPDATE alkohol SET naslov = ?, vrste = ? WHERE id = ?', (titolo_alk, info_alk, id))
        connection.commit()
        connection.close()

        return redirect('/')

    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM alkohol WHERE id = ?', (id,))
    alkohol = cursor.fetchone()
    connection.close()

    if alkohol:
        return render_template('updatealkohol.html', alkohol=alkohol, id=id)
    else:
        return "Alkohol nije pronađen"




if __name__ == '__main__':
    app.run()
