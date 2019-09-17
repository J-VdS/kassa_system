# -*- coding: utf-8 -*-
import sqlite3
import pickle
#import time
#import func

def update_dict(oud, nieuw):
    for key in nieuw:
        if key in oud:
            oud[key] += nieuw[key]
        else:
            oud[key] = nieuw[key]    
    return oud


def CloseIO(db_io):
    ''' Deze functie wordt opgeroepen als het scherm gesloten wordt en/of een error optreedt'''
    db_io[1].close() #conn
    db_io[0].close() #cursor

def OpenIO(db):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    return (conn, c)

def InitProduct(db):
    ''' Maakt de producten tabel en zorgt voor db_io '''
    pass

def InitTabels(db_io):
    conn, c = db_io
    #tables_check aanwezig
    #producten tabel
    c.execute("CREATE TABLE IF NOT EXISTS producten(id INTEGER PRIMARY KEY, type TEXT, naam TEXT, prijs REAL, active INTEGER)")
    c.execute("CREATE TABLE IF NOT EXISTS bestellingen(id INTEGER, bestelling BLOB, open INTEGER, prijs REAL, naam TEXT, betaalwijze TEXT)")
    #print("---Product Table Loaded ---")
    conn.commit()
   
    
def AddProduct(db_io, type, naam, prijs, active):
    ''' 
        voegt een product toe aan de producten tabel
        return values:
            0: succes
            -1: reeds aanwezig
            -2: error
    '''
    conn, c  = db_io
    c.execute("SELECT naam FROM producten")
    try:
        if naam in [row[0] for row in c.fetchall()]:
            #REEDS AANWEZIG
            return -1
        else:
            c.execute("INSERT INTO producten (naam, type, prijs, active) VALUES(?,?,?,?)",(naam, type, prijs, active))
            conn.commit()
            return 0
    except Exception as e:
        print("\n\n --- AddProduct error ---\n\n" + str(e))
        return -2
    

def getAllProduct(db_io):
    conn, c = db_io
    c.execute("SELECT type, naam, prijs, active FROM producten ORDER BY naam COLLATE NOCASE ASC")
    data = c.fetchall()
    return data


def getAllProductClient(db_io):
    conn, c = db_io
    c.execute("SELECT type, naam FROM producten WHERE active = ?", ('1'),)
    data = c.fetchall()
    return data


def getAllProductKassa(db_io):
    conn, c = db_io
    c.execute("SELECT type, naam, prijs FROM producten WHERE active = 1 OR active = 2 ORDER BY naam COLLATE NOCASE ASC")
    data = c.fetchall()
    return data #lijst bestaande uit tuples


def getTypes(db_io):
    conn, c = db_io
    c.execute("SELECT DISTINCT type FROM producten")
    data = c.fetchall()
    return data


def editProduct(db_io, naam, type, prijs, active):
    conn, c = db_io
    c.execute("SELECT * FROM producten WHERE naam = ?", (naam,))
    if not c.fetchone():
        return -1 #product niet in db
    else:
        c.execute("UPDATE producten SET type = ?, prijs = ?, active = ? WHERE naam = ?", (type, prijs, active, naam))
        conn.commit()
        return 0
    

def deleteProduct(db_io, naam):
    conn, c = db_io
    c.execute("SELECT * FROM producten WHERE naam = ?", (naam,))
    if not c.fetchone():
        return -1 #product niet in db
    else:
        c.execute("DELETE FROM producten WHERE naam = ?", (naam,))
        conn.commit()
        return 0
    
    
def zichtProduct(db_io, naam, active):
    conn, c = db_io
    c.execute("SELECT * FROM producten WHERE naam = ?", (naam,))
    if not c.fetchone():
        return -1
    else:
        c.execute("UPDATE producten SET active = ? WHERE naam = ?", (active, naam))
        conn.commit()
        return 0
    
#bestellingen
def addBestelling(db_io, info, bestelling):
    '''
        db_io (tuple): connectie met db
        info (dict): die info bevat over de klant en de verkoper
        bestelling (dict): nieuwe bestelling
        
        return:
            1 - nieuwe rekening wordt geopend
            0 - bestelling wordt toegevoegd
    '''
    conn, c = db_io
    c.execute("SELECT bestelling FROM bestellingen WHERE id = ?", (info["id"],))
    data = c.fetchone()
    if not data:
        #maak een nieuw ID aan
        bst = pickle.dumps(bestelling)
        c.execute("INSERT INTO bestellingen (id, naam, bestelling, open) VALUES (?,?,?,?)", (info["id"], str(info["naam"]), bst, 1))
        conn.commit()
        return 1
    else:
        bst = pickle.dumps(update_dict(pickle.loads(data[0]), bestelling))
        c.execute("UPDATE bestellingen SET bestelling = ? WHERE id = ?", (bst, info["id"]))
        conn.commit()
        return 0


def addBestellingID(db_io, ID, naam):
    conn, c = db_io
    c.execute("SELECT bestelling FROM bestellingen WHERE id = ?", (ID,))
    data = c.fetchone()
    if not data:
        c.execute("INSERT INTO bestellingen (id, naam, bestelling, open) VALUES (?,?,?,?)", (ID, naam, pickle.dumps({}), 1))
        conn.commit()
        return 1
    else:
        #err ID was al in de DB
        return -1
      

def getBestelling(db_io, ID):
    conn, c = db_io
    c.execute("SELECT bestelling FROM bestellingen WHERE id = ?", (ID,))
    data = c.fetchone()
    if not data:
        #er was geen bestelling met dit ID!
        return -1
    else:
        return pickle.loads(data[0]) #{product:aantal}


def getIDs(db_io):
    conn, c = db_io
    c.execute("SELECT id FROM bestellingen WHERE open = 1 ORDER BY id COLLATE NOCASE ASC")
    data = c.fetchall()
    return data  


def getInfoByID(db_io, ID):
    conn, c = db_io
    c.execute("SELECT naam, open FROM bestellingen WHERE id = ?", (ID,))
    data = c.fetchone()
    if not data:
        return ("ERROR", "---")
    else:
        return data
    

def delByID(db_io, ID):
    conn, c = db_io
    c.execute("DELETE FROM bestellingen WHERE id = ?", (ID,))
    conn.commit()


def sluitById(db_io, ID, prijs, bw):
    conn, c = db_io
    c.execute("UPDATE bestellingen SET open = 0, prijs = ? , betaalwijze = ? WHERE id = ?", (prijs, bw, ID))
    conn.commit()
    
        
