import sqlite3
import tkinter.ttk as ttk
from pathlib import Path
from sqlite3 import Error
from tkinter import *
from tkinter.messagebox import *

def init(base):
    global cur, db
    # Tester si la base de donnée existe
    fichierdb = Path(base)
    if not fichierdb.is_file():
        creationDb(base)
    try:
        db = sqlite3.connect(base)
        cur = db.cursor()
    except Error as e:
        print(e)
    return None

def creationDb(base):
    global cur, db
    db = sqlite3.connect(base)
    # récupére le curseur ( pointeur sur la db)
    cur = db.cursor()
    # création d'une table
    # cur.execute("CREATE TABLE IF NOT EXISTS parent (ref INTEGER PRIMARY KEY AUTOINCREMENT , nom TEXT, email TEXT, gsm REAL, classe text, ecole TEXT, motdepasse TEXT)")
    # cur.execute("CREATE TABLE IF NOT EXISTS auteurs (ref INTEGER PRIMARY KEY, nom TEXT, prenom TEXT)")
    cur.execute(
        "CREATE TABLE IF NOT EXISTS livres (ref INTEGER PRIMARY KEY AUTOINCREMENT , titre TEXT, auteur TEXT, code TEXT)")
    cur.execute(
        "CREATE TABLE IF NOT EXISTS disponibilites (ref INTEGER PRIMARY KEY AUTOINCREMENT , nom TEXT, email TEXT, gsm TEXT,classe TEXT, ecole TEXT,livre_ref INTEGER REFERENCES livres(ref) ON DELETE RESTRICT )")
    db.commit()
    # ajout()
    ajoutL()
    # ajoutA()
    # ajoutD()

def ajout():
    query = '''
                INSERT INTO parent (nom, email, gsm, classe, ecole, motdepasse)
                           VALUES (?,?,?,?,?,?)
                '''
    cur.execute(query, ("Pierreux", "pierreu@gmail.com", 0, "1C", "athénée waterloo", 0))
    cur.execute(query, ("De pape", "depape@gmail.com", 0, "1B", "athénée waterloo", 0))
    cur.execute(query, ("Herris", "herris@gmail.com", 0, "1F", "athénee waterloo", 0))
    cur.execute(query, ("De prince", "deprince@gmail.com", 0, "1E", "athénée waterloo", 0))
    cur.execute(query, ("Decosta", "decosta@gmail.com", 0, "1A", "athénée waterloo", 0))
    cur.execute(query, ("Gilot", "gilot@hotmail.com", 0, "1B", "athénée waterloo", 0))
    cur.execute(query, ("Moreau", "moreau@hotmail.com", 0, "1B", "athénée waterloo", 0))
    db.commit()

def ajoutA():
    query = '''
                    INSERT INTO auteurs (nom, prenom)
                           VALUES (?,?)
                '''
    cur.execute(query, ("Beorn", "Paul"))
    cur.execute(query, ("Rigal-Goulard", "Sophie"))
    cur.execute(query, ("Petit", "Xavier-Laurent"))
    cur.execute(query, ("Rachmuhl", "Françoise"))
    cur.execute(query, ("Desplat-Duc", "Anne-Marie"))
    cur.execute(query, ("Vittori", "Jean-Pierre"))
    db.commit()

def ajoutL():
    query = '''
                    INSERT INTO livres (titre, auteur, code)
                        VALUES (?,?,?)
            '''
    cur.execute(query, ("14-14", "Beorn Paul", 123))
    cur.execute(query, ("15 jours sans réseaux", "Rigal Sophie", 234))
    cur.execute(query, ("153 jours en hiver", "Petit Xavier-Laurent", 455))
    cur.execute(query, ("16 métamorphoses d'Ovide", "Rachmuhl Françoise", 567))
    cur.execute(query, ("1943 l'espoir du retour", "Desplat anne", 789))
    cur.execute(query, ("1944-1945 Les sabots", "Vittori Jean", 367))
    db.commit()
# Premiere fenetre livres-> crud
# ref, titre, auteur, codeISBN
# Bt - Ajouter un livre commande ajoute
#    - Voir dispo commande windispo
#    - Supprimer commande supprime
#    - Quitter commande destroy
def fenetre():
    global tables, root
    # créer la premiere fenêtre
    root = Tk()
    root.title("Livres")
    tables = ttk.Treeview(root)
    tables.grid(row=0, columnspan=4, sticky=N + E + S + W, padx=10, pady=10)
    # Déclaration des colonnes
    tables["columns"] = ("col1", "col2", "col3", "col4")
    # Taille des colonnes
    tables.column("#1", width=30, minwidth=30)
    tables.column("#2", width=200, minwidth=200)
    tables.column("#3", width=200, minwidth=200)
    tables.column("#4", width=200, minwidth=200)
    # Noms des colonnes
    tables.heading("col1", text="Réf", anchor=W)
    tables.heading("col2", text="Titre", anchor=W)
    tables.heading("col3", text="Auteur", anchor=W)
    tables.heading("col4", text="code ISBN", anchor=W)
    # Paramètrer la scrollbar
    ascenseurY = ttk.Scrollbar(root, orient=VERTICAL, command=tables.yview)
    # Positionner la scrollbar
    ascenseurY.grid(row=0, column=6)
    # Configurer notre treeview
    tables.config(show="headings", height=5, selectmode="browse", yscrollcommand=ascenseurY.set)
    remplissage()
    # Boutons
    Button(root, text="Ajouter un livre", command=ajoute).grid(row=1, column=0, padx=10, pady=10, sticky=E + W)
    Button(root, text="Voir les disponibilités", command=windisp).grid(row=1, column=1, padx=10, sticky=E + W)
    Button(root, text="Supprimer", command=supprime).grid(row=1, column=2, padx=10, sticky=E + W)
    Button(root, text="Quitter", command=root.destroy).grid(row=1, column=3, padx=10, sticky=E + W)

# Fenêtre qui repond au bouton ajouter un livre
def ajoute():
    global win
    # Création d'une fenêtre modal
    win = Toplevel(root)
    win.title("Ajout d'un livre")
    # Déclaration des variables du formulaire
    titre = StringVar()
    auteur = StringVar()
    code = StringVar()
    # Etiquettes
    Label(win, text="Titre").grid(row=0, column=0, pady=5, padx=5)
    Label(win, text="Auteur").grid(row=1, column=0, pady=5, padx=5)
    Label(win, text="code ISBN").grid(row=2, column=0, pady=5, padx=5)
    # Les entrys
    Entry(win, textvariable=titre, width=30).grid(row=0, column=1, columnspan=2, padx=5)
    Entry(win, textvariable=auteur, width=30).grid(row=1, column=1, columnspan=2, padx=5)
    Entry(win, textvariable=code, width=30).grid(row=2, column=1, columnspan=2, padx=5)
    # Boutons
    Button(win, text="Ajouter", command=lambda: ajoutDb(titre.get(), auteur.get(), code.get())).grid(row=4, column=1,
                                                                                                     padx=5,
                                                                                                     sticky=E + W)
    Button(win, text="Annuler", command=win.destroy).grid(row=4, column=2, padx=5, pady=10, sticky=E + W)

# Permet d'ajouter des  nouvelles données
def ajoutDb(titre, auteur, code):
    global win
    win.destroy()
    if titre != "" and auteur != "":
        query = '''
            INSERT INTO livres (titre, Auteur, code)
                    VALUES (?, ?, ?)
        '''
        cur.execute(query, (titre, auteur, code))
        db.commit()
        remplissage()

# Permet de vider, récuperer et ajouter des livres ds la fenêtre
def remplissage():
    global tables
    # Vider la liste
    tables.delete(*tables.get_children())
    # Récupérer la liste de la db
    cur.execute("SELECT * FROM livres")
    livres = cur.fetchall()
    # Ajouter les livres dans le treeview
    for livre in livres:
        tables.insert('', 'end', values=(livre[0], livre[1], livre[2], livre[3]))
# Permet de supprimer
def supprime():
    global tables
    if (tables.focus()):
        titre = tables.item(tables.focus())["values"][1]
        auteur = tables.item(tables.focus())["values"][2]
        idAsupprimer = tables.item(tables.focus())["values"][0]
        confirm = askokcancel("Ok ou annuler", "Suppression de " + titre + " " + auteur + " ?")
        if confirm:
            # supprimer le record
            cur.execute("DELETE FROM livres WHERE ref = ?", (idAsupprimer,))
            db.commit()
            remplissage()
    else:
        showinfo("Attention", "Veuillez sélectionner \nune ligne avant de \nsupprimer")

# Nouvelle fenetre diponibilité-> crud
# Bt ajouter une dispo commande voirdispo
#    modifier une dispo commande modifiedispo
#    supprimer une dispo commande supprimedispo
#    quitter commande destroy

def windisp():
    global tabledisp, fendisp
    fendisp = Tk()
    fendisp.title("Disponibilité")
    tabledisp = ttk.Treeview(root)
    tabledisp.grid(row=0, columnspan=5, sticky=N + E + S + W, padx=10, pady=10)
    tabledisp ["columns"] = ("col1", "col2", "col3", "col4", "col5", "col6")
    tabledisp.column("#1", width=30, minwidth=30)
    tabledisp.column("#2", width=150, minwidth=150)
    tabledisp.column("#3", width=150, minwidth=150)
    tabledisp.column("#4", width=150, minwidth=150)
    tabledisp.column("#5", width=150, minwidth=150)
    tabledisp.column("#6", width=150, minwidth=150)
    tabledisp.heading("col1", text="Réf", anchor=W)
    tabledisp.heading("col2", text="nom", anchor=W)
    tabledisp.heading("col3", text="mail", anchor=W)
    tabledisp.heading("col4", text="gsm", anchor=W)
    tabledisp.heading("col5", text="classe", anchor=W)
    tabledisp.heading("col6", text="ecole", anchor=W)
    ascenseurY = ttk.Scrollbar(fendisp, orient=VERTICAL, command=tabledisp.yview)
    ascenseurY.grid(row=0,column=5)
    tabledisp.config(show="headings", height=5, selectmode="browse", yscrollcommand=ascenseurY.set)

    Button(fendisp, text="ajouter une dispo", command=voirdispo).grid(row=1,column=0,padx=10,sticky=E+W)
    Button(fendisp, text="modifier une dispo", command=modifiedispo).grid(row=1,column=1,padx=10,sticky=E+W)
    Button(fendisp, text="supprimer une dispo", command=supprimedispo).grid(row=1,column=2,padx=10,sticky=E+W)
    Button(fendisp, text="Quitter", command=fendisp.destroy).grid(row=1,column=3,padx=10,sticky=E+W)
    db.commit()
    remplissage()


def remplissagedisp():
    global tabledisp
    # Vider la liste
    tabledisp.delete(*tabledisp.get_children())
    # Récupérer la liste de la db
    ref = tabledisp.item(tabledisp.focus())["values"][0]
    cur.execute("SELECT * FROM disponibilites WHERE livre_ref =?", (ref,))
    dispos = cur.fetchall()
    # Ajouter les livres dans le treeview
    for dispo in dispos:
        tabledisp.insert('', 'end', values=(dispo[0], dispo[1], dispo[2], dispo[3], dispo[4], dispo[5]))


# Nouvelle fenetre disponibilités
def voirdispo():
        global windispo
        windispo = Toplevel(root)
        windispo.title("Disponibilité du livre selectionner")
        # Déclaration des variables du formulaire
        nom = StringVar()
        email = StringVar()
        gsm = StringVar()
        classe = StringVar()
        ecole = StringVar()
        # Etiquette
        Label(windispo, text="Nom").grid(row=0, column=0, pady=5, padx=5)
        Label(windispo, text="Email").grid(row=1, column=0, pady=5, padx=5)
        Label(windispo, text="Gsm").grid(row=2, column=0, pady=5, padx=5)
        Label(windispo, text="Classe").grid(row=3, column=0, pady=5, padx=5)
        Label(windispo, text="Ecole").grid(row=4, column=0, pady=5, padx=5)
        # Les entrys
        Entry(windispo, text=nom, width=30).grid(row=0, column=1, columnspan=2, padx=5)
        Entry(windispo, text=email, width=30).grid(row=1, column=1, columnspan=2, padx=5)
        Entry(windispo, text=gsm, width=30).grid(row=2, column=1, columnspan=2, padx=5)
        Entry(windispo, text=classe, width=30).grid(row=3, column=1, columnspan=2, padx=5)
        Entry(windispo, text=ecole, width=30).grid(row=4, column=1, columnspan=2, padx=5)
        # Boutons
        Button(windispo, text="Ajouter", command=ajoutedispo).grid(row=7, column=0, padx=5, sticky=E + W)
        Button(windispo, text="Quitter", command=windispo.destroy).grid(row=7, column=3, padx=5, pady=10, sticky=E + W)
        remplissage()

def modifiedispo():
    pass
def supprimedispo():
    global tabledisp
    if (tabledisp.focus()):
        nom = tabledisp.item(tabledisp.focus())["values"][1]
        email = tabledisp.item(tabledisp.focus())["values"][2]
        livre_ref = tabledisp.item(tabledisp.focus())["values"][0]
        confirm = askokcancel("Ok ou annuler", "Suppression de " + nom + " " + email + " ?")
        if confirm:
            # supprimer le record
            cur.execute("DELETE FROM disponibilites WHERE livre_ref = ?", (livre_ref,))
            db.commit()
            remplissagedisp()
    else:
        showinfo("Attention", "Veuillez sélectionner \nune ligne avant de \nsupprimer")

def ajoutedispo():

    ref = tabledisp.item(tabledisp.selection())["values"][0]
    nom = tabledisp.item(tabledisp.selection())["values"][1]
    email= tabledisp.item(tabledisp.selection())["values"][2]
    gsm = tabledisp.item(tabledisp.selection())["values"][3]
    classe = tabledisp.item(tabledisp.selection())["values"][4]
    ecole = tabledisp.item(tabledisp.selection())["values"][5]

    cur.execute("INSERT INTO disponibilites(nom, email,gsm,classe, ecole, livre_ref)VALUES (?,?,?,?,?,?)",
                (nom.get(), email.get(), gsm.get(), classe.get(), ecole.get(),ref))
    db.commit()
def ajoutedispodb(ref,nom,email,gsm,classe,ecole):
    global tabledisp
    tabledisp.destroy()
    ref = tabledisp.item(tabledisp.focus())["values"][0]
    cur.execute("SELECT*disponibilites WHERE livre_ref= ?", (ref))
    db.commit()


if __name__ == '__main__':
    init("Gooris/data.sqlite")
    fenetre()
    mainloop()
