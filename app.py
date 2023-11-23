#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Flask, request, render_template, redirect, flash

app = Flask(__name__)
app.secret_key = 'une cle(token) : grain de sel(any random string)'

                                    ## à ajouter
from flask import session, g
import pymysql.cursors

def get_db():
    if 'db' not in g:
        g.db =  pymysql.connect(
            host="localhost",                 # à modifier
            user="audrick",                     # à modifier
            password="mdp",                # à modifier
            database="SAE",        # à modifier
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db

@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

app = Flask(__name__)    # instance de classe Flask (en paramètre le nom du module)

@app.route('/')
def show_index():
    return render_template('index.html')

#Example
"""
@app.route('/etudiant/show')
def show_etudiants():
    mycursor = get_db().cursor()
    sql=''' SELECT id_etudiant AS id, nom_etudiant AS nom, groupe_etudiant AS groupe
    FROM etudiant
    ORDER BY nom_etudiant;'''
    mycursor.execute(sql)
    liste_etudiants = mycursor.fetchall()
    return render_template('etudiant/show_etudiants.html', etudiants=liste_etudiants )


@app.route('/etudiant/add', methods=['GET'])
def add_etudiant():
    print('''affichage du formulaire pour saisir un étudiant''')
    return render_template('etudiant/add_etudiant.html')

@app.route('/etudiant/delete')
def delete_etudiant():
    print('''suppression d'un étudiant''')
    id=request.args.get('id',0)
    print(id)
    mycursor = get_db().cursor()
    tuple_param=(id)
    sql="DELETE FROM etudiant WHERE id_etudiant=%s;"
    mycursor.execute(sql,tuple_param)

    get_db().commit()
    print(request.args)
    print(request.args.get('id'))
    id=request.args.get('id',0)
    return redirect('/etudiant/show')

@app.route('/etudiant/edit', methods=['GET'])
def edit_etudiant():
    print('''affichage du formulaire pour modifier un étudiant''')
    print(request.args)
    print(request.args.get('id'))
    id=request.args.get('id')
    mycursor = get_db().cursor()
    sql=''' SELECT id_etudiant AS id, nom_etudiant AS nom, groupe_etudiant AS groupe
    FROM etudiant
    WHERE id_etudiant=%s;'''
    tuple_param=(id)
    mycursor.execute(sql,tuple_param)
    etudiant = mycursor.fetchone()
    return render_template('etudiant/edit_etudiant.html', etudiant=etudiant)


@app.route('/etudiant/add', methods=['POST'])
def valid_add_etudiant():
    print('''ajout de l'étudiant dans le tableau''')
    nom = request.form.get('nom')
    groupe = request.form.get('groupe')
    message = 'nom :' + nom + ' - groupe :' + groupe
    print(message)
    mycursor = get_db().cursor()
    tuple_param=(nom,groupe)
    sql="INSERT INTO etudiant(id_etudiant, nom_etudiant, groupe_etudiant) VALUES (NULL, %s, %s);"
    mycursor.execute(sql,tuple_param)
    get_db().commit()
    return redirect('/etudiant/show')

@app.route('/etudiant/edit', methods=['POST'])
def valid_edit_etudiant():
    print('''modification de l'étudiant dans le tableau''')
    id = request.form.get('id')
    nom = request.form.get('nom')
    groupe = request.form.get('groupe')
    message = 'nom :' + nom + ' - groupe :' + groupe + ' pour l etudiant d identifiant :' + id
    print(message)
    mycursor = get_db().cursor()
    tuple_param=(nom,groupe,id)
    sql="UPDATE etudiant SET nom_etudiant = %s, groupe_etudiant= %s WHERE id_etudiant=%s;"
    mycursor.execute(sql,tuple_param)
    get_db().commit()
    return redirect('/etudiant/show')"""

#Etudiant (Gaël)
@app.route('/etudiant/show')
def show_etudiants():
    mycursor = get_db().cursor()
    sql=''' SELECT Etudiant.id_etudiant AS idEtudiant, Etudiant.nom AS nomEtudiant, Etudiant.prenom AS prenomEtudiant, Etudiant.email, Etudiant.telephone
    FROM Etudiant
    ORDER BY id_etudiant;'''
    mycursor.execute(sql)
    liste_etudiants = mycursor.fetchall()
    return render_template('etudiant/show_etudiants.html', etudiants=liste_etudiants)

@app.route('/etudiant/delete')
def delete_etudiant():
    id=request.args.get('id',0)
    print('''suppression du contrat avec l'ID : ''' + id)
    mycursor = get_db().cursor()
    tuple_param=(id)
    sql="""DELETE FROM Contrat WHERE id_etudiant=%s;"""
    mycursor.execute(sql,tuple_param)
    get_db().commit()
    sql = """DELETE FROM Etudiant WHERE id_etudiant=%s;"""
    mycursor.execute(sql, tuple_param)
    get_db().commit()
    return redirect('/etudiant/show')

@app.route('/etudiant/add', methods=['GET'])
def add_etudiant():
    mycursor = get_db().cursor()
    sql='''SELECT id_etudiant AS id, nom, prenom
    FROM Etudiant
    ORDER BY id_etudiant;'''
    mycursor.execute(sql)
    liste_etudiants = mycursor.fetchall()
    print('''affichage du formulaire pour saisir un contrat''')
    return render_template('contrat/add_contrat.html', etudiants=liste_etudiants)

@app.route('/etudiant/add', methods=['POST'])
def valid_add_etudiant():
    print('''ajout du contrat dans le tableau''')
    idVelo = request.form.get('idVelo')
    idEtudiant = request.form.get('idEtudiant')
    dateDebut = request.form.get('dateDebut')
    dateFin = request.form.get('dateFin')
    #message = 'nom :' + nom + ' - groupe :' + groupe
    #print(message)
    mycursor = get_db().cursor()
    tuple_param=(dateDebut, dateFin,idEtudiant, idVelo)
    sql="INSERT INTO Etudiant (date_debut, date_fin, id_etudiant, id_velo) VALUES (%s, %s,%s,%s);"
    mycursor.execute(sql,tuple_param)
    get_db().commit()
    return redirect('/contrat/show')

#Contrat (Audrick)
@app.route('/contrat/show')
def show_contrats():
    mycursor = get_db().cursor()
    sql=''' SELECT Contrat.id_contrat AS idContrat, Contrat.id_velo AS idVelo, Contrat.id_etudiant AS idEtudiant, Contrat.date_debut AS dateDebut, Contrat.date_fin AS dateFin,
    Etudiant.nom as nomEtudiant, Etudiant.prenom as prenomEtudiant
    FROM Contrat JOIN Etudiant ON Contrat.id_etudiant = Etudiant.id_etudiant
    ORDER BY id_contrat;'''
    mycursor.execute(sql)
    liste_contrats = mycursor.fetchall()
    return render_template('contrat/show_contrats.html', contrats=liste_contrats)

@app.route('/contrat/delete')
def delete_contrat():
    id=request.args.get('id',0)
    print('''suppression du contrat avec l'ID : ''' + id)
    mycursor = get_db().cursor()
    tuple_param=(id)
    sql="DELETE FROM Contrat WHERE id_contrat=%s;"
    mycursor.execute(sql,tuple_param)
    get_db().commit()
    return redirect('/contrat/show')

@app.route('/contrat/add', methods=['GET'])
def add_contrat():
    mycursor = get_db().cursor()
    sql='''SELECT id_etudiant AS id, nom, prenom
    FROM Etudiant
    ORDER BY id_etudiant;'''
    mycursor.execute(sql)
    liste_etudiants = mycursor.fetchall()
    sql='''SELECT id_velo AS id
    FROM Velo
    ORDER BY id_velo;'''
    mycursor.execute(sql)
    liste_velos = mycursor.fetchall()
    print('''affichage du formulaire pour saisir un contrat''')
    return render_template('contrat/add_contrat.html', velos=liste_velos, etudiants=liste_etudiants)

@app.route('/contrat/add', methods=['POST'])
def valid_add_contrat():
    print('''ajout du contrat dans le tableau''')
    idVelo = request.form.get('idVelo')
    idEtudiant = request.form.get('idEtudiant')
    dateDebut = request.form.get('dateDebut')
    dateFin = request.form.get('dateFin')
    #message = 'nom :' + nom + ' - groupe :' + groupe
    #print(message)
    mycursor = get_db().cursor()
    tuple_param=(dateDebut, dateFin,idEtudiant, idVelo)
    sql="INSERT INTO Contrat (date_debut, date_fin, id_etudiant, id_velo) VALUES (%s, %s,%s,%s);"
    mycursor.execute(sql,tuple_param)
    get_db().commit()
    return redirect('/contrat/show')

@app.route('/contrat/edit', methods=['GET'])
def edit_contrat():
    print('''affichage du formulaire pour modifier un contrat''')
    print(request.args)
    print(request.args.get('id'))
    id=request.args.get('id')
    mycursor = get_db().cursor()
    sql='''SELECT id_contrat AS idContrat, id_etudiant AS idEtudiant, id_velo AS idVelo, date_debut as dateDebut, date_fin as dateFin
    FROM Contrat
    WHERE id_contrat=%s;'''
    tuple_param=(id)
    mycursor.execute(sql,tuple_param)
    contrat = mycursor.fetchone()
    sql='''SELECT id_etudiant AS id, nom, prenom
    FROM Etudiant
    ORDER BY id_etudiant;'''
    mycursor.execute(sql)
    liste_etudiants = mycursor.fetchall()
    sql='''SELECT id_velo AS id
    FROM Velo
    ORDER BY id_velo;'''
    mycursor.execute(sql)
    liste_velos = mycursor.fetchall()
    return render_template('contrat/edit_contrat.html', contrat=contrat, velos=liste_velos, etudiants=liste_etudiants)

@app.route('/contrat/edit', methods=['POST'])
def valid_edit_contrat():
    print('''modification du contrat dans le tableau''')
    id = int(request.form.get('idContrat'))
    idVelo = request.form.get('idVelo')
    idEtudiant = request.form.get('idEtudiant')
    dateDebut = request.form.get('dateDebut')
    dateFin = request.form.get('dateFin')
    #message = 'nom :' + nom + ' - groupe :' + groupe + ' pour l etudiant d identifiant :' + id
    #print(message)
    mycursor = get_db().cursor()
    tuple_param=(idVelo,idEtudiant,dateDebut,dateFin,id)
    sql="UPDATE Contrat SET id_velo = %s, id_etudiant= %s, date_debut = %s, date_fin = %s WHERE id_contrat=%s;"
    mycursor.execute(sql,tuple_param)
    get_db().commit()
    return redirect('/contrat/show')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
