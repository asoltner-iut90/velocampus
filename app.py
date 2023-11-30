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
    sql='''SELECT E.nom_etablissement, F.nom_formation, C.id_composante, Etudiant.id_etudiant AS idEtudiant, Etudiant.nom AS nomEtudiant, Etudiant.prenom AS prenomEtudiant, Etudiant.email AS emailEtudiant, Etudiant.telephone AS telephoneEtudiant
FROM Etudiant
JOIN Composante C on Etudiant.id_composante = C.id_composante
JOIN Etablissement E on C.id_etablissement = E.id_etablissement
JOIN Formation F on C.id_formation = F.id_formation
ORDER BY idEtudiant;'''
    mycursor.execute(sql)
    liste_etudiants = mycursor.fetchall()
    return render_template('etudiant/show_etudiants.html', etudiants=liste_etudiants)

@app.route('/etudiant/delete')
def delete_etudiant():
    id = request.args.get('id', 0)
    print('''suppression du contrat avec l'ID : ''' + id)
    mycursor = get_db().cursor()

    # Use a tuple with a single element
    tuple_param = (id,)

    sql = """SELECT id_contrat, id_etudiant
             FROM Contrat 
             WHERE id_etudiant=%s;"""
    mycursor.execute(sql, tuple_param)
    contrats = mycursor.fetchall()
    print(contrats)

    if len(contrats) == 0:
        mycursor = get_db().cursor()

        # Use a tuple with a single element
        tuple_param = (id,)

        sql = """DELETE FROM Etudiant WHERE id_etudiant=%s"""
        mycursor.execute(sql, tuple_param)
        get_db().commit()
    else:
        mycursor = get_db().cursor()

        # Use a tuple with a single element
        tuple_param = (id,)

        sql = '''SELECT id_contrat, date_debut, date_fin, id_etudiant
                 FROM Contrat
                 WHERE id_etudiant = %s;'''
        mycursor.execute(sql, tuple_param)
        contrats = mycursor.fetchall()

        sql = '''SELECT E.nom_etablissement, F.nom_formation, C.id_composante, Etudiant.id_etudiant AS idEtudiant, Etudiant.nom AS nomEtudiant, Etudiant.prenom AS prenomEtudiant, Etudiant.email AS emailEtudiant, Etudiant.telephone AS telephoneEtudiant
                 FROM Etudiant
                 JOIN Composante C on Etudiant.id_composante = C.id_composante
                 JOIN Etablissement E on C.id_etablissement = E.id_etablissement
                 JOIN Formation F on C.id_formation = F.id_formation
                 WHERE Etudiant.id_etudiant = %s
                 ORDER BY idEtudiant;'''

        mycursor.execute(sql, tuple_param)
        etudiants = mycursor.fetchall()
        return render_template('etudiant/delete_etudiant.html', contrats=contrats, etudiants=etudiants)

    return redirect('/etudiant/show')


@app.route('/etudiant/add', methods=['GET'])
def add_etudiant():
    mycursor = get_db().cursor()
    sql='''SELECT id_etudiant AS id, nom, prenom
    FROM Etudiant
    ORDER BY id_etudiant;'''
    mycursor.execute(sql)
    liste_etudiants = mycursor.fetchall()
    mycursor = get_db().cursor()
    sql = '''SELECT nom_formation, id_formation
       FROM Formation
       ORDER BY id_formation;'''
    mycursor.execute(sql)
    composantes = mycursor.fetchall()
    sql = """SELECT id_etablissement AS id_etablissement, nom_etablissement
    FROM Etablissement"""
    mycursor.execute(sql)
    etablissements = mycursor.fetchall()
    print('''affichage du formulaire pour saisir un contrat''')
    return render_template('etudiant/add_etudiant.html', etudiants=liste_etudiants, composantes=composantes, etablissements=etablissements)

@app.route('/etudiant/add', methods=['POST'])
def valid_add_etudiant():
    print('''ajout du contrat dans le tableau''')
    idEtudiant = request.form.get('idEtudiant')
    nomEtudiant = request.form.get('nomEtudiant')
    prenomEtudiant = request.form.get('prenomEtudiant')
    emailEtudiant = request.form.get('emailEtudiant')
    telephoneEtudiant = request.form.get('telephoneEtudiant')
    idComposante = request.form.get('idComposante')
    #message = 'nom :' + nom + ' - groupe :' + groupe
    #print(message)
    mycursor = get_db().cursor()
    tuple_param=(nomEtudiant, prenomEtudiant, emailEtudiant, telephoneEtudiant, idEtudiant, idComposante)
    sql="INSERT INTO Etudiant (nom, prenom, email, telephone, id_etudiant, id_composante ) VALUES (%s,%s,%s,%s,%s,%s);"
    mycursor.execute(sql,tuple_param)
    get_db().commit()
    return redirect('/etudiant/show')

@app.route('/etudiant/edit', methods=['GET'])
def edit_etudiant():
    print('''affichage du formulaire pour modifier un étudiant''')
    print(request.args)
    print(request.args.get('id'))
    id = request.args.get('id')
    mycursor = get_db().cursor()
    sql = ''' SELECT id_etudiant AS id, nom, prenom, email, telephone, id_composante
        FROM Etudiant
        WHERE id_etudiant=%s;'''
    tuple_param = (id)
    mycursor.execute(sql, tuple_param)
    etudiant = mycursor.fetchone()
    sql = ''' SELECT Formation.id_formation AS id_formation, Formation.nom_formation AS nom_formation, C.id_etablissement AS id_etablissement, nom_etablissement
    FROM Formation
    JOIN Composante C on Formation.id_formation = C.id_formation
    JOIN Etablissement E on E.id_etablissement = C.id_etablissement;'''
    mycursor.execute(sql)
    formations = mycursor.fetchall()
    print(formations)
    sql =  """SELECT id_etablissement AS id_etablissement, nom_etablissement
    FROM Etablissement"""
    mycursor.execute(sql)
    etablissements = mycursor.fetchall()
    return render_template('etudiant/edit_etudiant.html', etudiant=etudiant, formations=formations, etablissements=etablissements)

@app.route('/etudiant/edit', methods=['POST'])
def valid_edit_etudiant():
    print('''modification de l'étudiant dans le tableau''')
    idEtudiant = request.form.get('idEtudiant')
    print(idEtudiant)
    nomEtudiant = request.form.get('nomEtudiant')
    print(nomEtudiant)
    prenomEtudiant = request.form.get('prenomEtudiant')
    print(prenomEtudiant)
    emailEtudiant = request.form.get('emailEtudiant')
    print(emailEtudiant)
    telephoneEtudiant = request.form.get('telephoneEtudiant')
    print(telephoneEtudiant)
    composante = request.form.get('composante')
    print(composante)
    etablissement = request.form.get('etablissement')
    print(etablissement)
    #message = 'nom :' + nom + ' - groupe :' + groupe + ' pour l etudiant d identifiant :' + id
    #print(message)
    mycursor = get_db().cursor()
    tuple_param = (nomEtudiant, prenomEtudiant, emailEtudiant, telephoneEtudiant, composante, idEtudiant)
    sql = """UPDATE Etudiant SET nom=%s, prenom=%s, email=%s, telephone=%s, id_composante=%s WHERE id_etudiant=%s;"""
    mycursor.execute(sql, tuple_param)
    get_db().commit()
    return redirect('/etudiant/show')

@app.route('/etudiant/etat', methods=['GET', 'POST'])
def etat_etudiant():
    if request.method == 'POST':
        etudiant_id = request.form.get('etudiant_id')

        # Vous pouvez ajouter d'autres filtres ici en fonction de vos besoins

        # Exécutez la requête en fonction des filtres fournis
        mycursor = get_db().cursor()
        sql = '''SELECT E.nom_etablissement, F.nom_formation, C.id_composante, Etudiant.id_etudiant AS idEtudiant, Etudiant.nom AS nomEtudiant, Etudiant.prenom AS prenomEtudiant, Etudiant.email AS emailEtudiant, Etudiant.telephone AS telephoneEtudiant
                 FROM Etudiant
                 JOIN Composante C on Etudiant.id_composante = C.id_composante
                 JOIN Etablissement E on C.id_etablissement = E.id_etablissement
                 JOIN Formation F on C.id_formation = F.id_formation
                 WHERE Etudiant.id_etudiant = %s
                 ORDER BY idEtudiant;'''
        mycursor.execute(sql, (etudiant_id,))
        etudiants = mycursor.fetchall()

        return render_template('etudiant/etat_etudiant.html', etudiants=etudiants)

    # Si la méthode est GET (accès initial à la page), affichez la page avec le formulaire
    return render_template('etudiant/etat_etudiant.html')
  
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

@app.route('/contrat/etat')
def view_contrat():
    sql="""SELECT Contrat.id_contrat AS idContrat, Contrat.date_debut as dateDebut, Contrat.date_fin AS dateFin, Contrat.id_etudiant AS idEtudiant,
       E.nom AS nom, E.prenom AS prenom, E.email AS email, E.telephone as telephone,
       Tv.caution AS caution, Tv.nom_type_velo AS type_velo,
       Etablissement.nom_etablissement AS etablissement, F.nom_formation AS formation
        FROM Contrat
        JOIN Etudiant E ON Contrat.id_etudiant = E.id_etudiant
        JOIN Velo V ON Contrat.id_velo = V.id_velo
        JOIN Type_velo Tv on V.id_type_velo = Tv.id_type_velo
        JOIN Composante C on E.id_composante = C.id_composante
        JOIN Etablissement on C.id_etablissement = Etablissement.id_etablissement
        JOIN Formation F on C.id_formation = F.id_formation"""
    mycursor = get_db().cursor()
    tuple_param=()
    mycursor.execute(sql,tuple_param)
    contrat = mycursor.fetchone()
    return render_template('contrat/view_contrat.html', contrat=contrat)

#Répatation(Mattéo)
@app.route('/reparation/show')
def show_reparation():
    mycursor = get_db().cursor()
    sql = ''' SELECT Reparation.id_reparation AS idReparation, Reparation.date_reparation AS dateReparation, Reparation.descriptif AS descriptif, 
        Velo.id_velo as idVelo
        FROM Reparation JOIN Velo ON Reparation.id_velo = Velo.id_velo
        ORDER BY id_reparation;'''
    mycursor.execute(sql)
    liste_reparations = mycursor.fetchall()
    return render_template('reparation/show_reparation.html', reparations=liste_reparations)
@app.route('/reparation/delete')
def delete_reparation():
    id=request.args.get('id',0)
    print('''suppression de la réparation avec l'ID : ''' + id)
    mycursor = get_db().cursor()
    tuple_param=(id)
    sql="DELETE FROM Reparation WHERE id_reparation=%s;"
    mycursor.execute(sql,tuple_param)
    get_db().commit()
    return redirect('/reparation/show')

@app.route('/reparation/add', methods=['GET'])
def add_reparation():
    mycursor = get_db().cursor()
    sql='''SELECT Reparation.id_reparation AS idReparation, Reparation.date_reparation AS dateReparation, Reparation.descriptif AS descriptif, 
        Velo.id_velo as idVelo
        FROM Reparation JOIN Velo ON Reparation.id_velo = Velo.id_velo
        ORDER BY id_reparation;'''
    mycursor.execute(sql)
    reparations = mycursor.fetchall()
    sql = '''SELECT Velo.id_velo as idVelo
            FROM Velo
            ORDER BY id_velo;'''
    mycursor.execute(sql)
    velos = mycursor.fetchall()
    print('''affichage du formulaire pour saisir une réparation''')
    return render_template('reparation/add_reparation.html', reparations=reparations,velos = velos)


@app.route('/reparation/add', methods=['POST'])
def valid_add_reparation():
    print('''ajout de la réparation dans le tableau''')
    idVelo = request.form.get('idVelo')
    dateReparation = request.form.get('dateReparation')
    descriptif = request.form.get('descriptif')
    mycursor = get_db().cursor()
    tuple_param = (dateReparation, descriptif, idVelo)
    sql = "INSERT INTO Reparation (dateReparation, descriptif, id_velo) VALUES (%s, %s,%s);"
    mycursor.execute(sql, tuple_param)
    get_db().commit()
    return redirect('/contrat/show')



#Run
if __name__ == '__main__':
    app.run(debug=True, port=5000)
