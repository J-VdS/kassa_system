# -*- coding: utf-8 -*-
import sqlite3
from pickle import loads, dumps
#import time
import func


def CloseIO(db_io):
    ''' Deze functie wordt opgeroepen als het scherm gesloten wordt en/of een error optreedt'''
    db_io[1].close() #conn
    db_io[0].close() #cursor


def InitProduct(db):
    ''' Maakt de producten tabel en zorgt voor db_io '''
    conn = sqlite3.connect(db)
    c = conn.cursor()
    #tables_check aanwezig
    #producten tabel
    c.execute("CREATE TABLE IF NOT EXISTS producten(id INTEGER PRIMARY KEY, type TEXT, naam TEXT, prijs REAL, active INTEGER)")
    print("---Product Table Loaded ---")
    conn.commit()
    return (conn, c) #geef tuple met (connectie, cursor) terug
   
    
def InitBestelling(db):
    pass

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
            print("commit")
            return 0
    except Exception as e:
        print("\n\n --- AddProduct error ---\n\n" + str(e))
        return -2

def getAllProduct(db_io):
    conn, c = db_io
    c.execute("SELECT type, naam, prijs, active FROM producten ORDER BY naam COLLATE NOCASE ASC")
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
#old
def loadTables(db):
	conn = sqlite3.connect(db)
	c = conn.cursor()
	#tables
	c.execute("CREATE TABLE IF NOT EXISTS items(type TEXT, naam TEXT, prijs REAL, active INTEGER, locatie INTEGER)")
	c.execute("CREATE TABLE IF NOT EXISTS bestellingen(id INTEGER PRIMARY KEY, tafel INTEGER, totaal INTEGER, items BLOB)")
	conn.commit()
	c.close()
	conn.close()
	print("succes")
	return 0
		
def editGerecht(db, naam, type, prijs, active=0, locatie=0):
	conn = sqlite3.connect(db)
	c = conn.cursor()
	c.execute("SELECT * FROM items WHERE naam = ?", (naam,))
	if not c.fetchone():
		c.close()
		conn.close()
		return -1 #product niet in db
	else:
		c.execute("UPDATE items SET type = ?, prijs = ?, active = ? WHERE naam = ?", (type, prijs, active, naam))
		conn.commit()
		c.close()
		conn.close()
		return 0 #succes
		

def getAlles(db):
	conn = sqlite3.connect(db)
	c = conn.cursor()
	c.execute("SELECT * FROM items")
	data = c.fetchall()
	c.close()
	conn.close()
	return data

def deleteGerecht(db, naam):
	conn = sqlite3.connect(db)
	c = conn.cursor()
	c.execute("SELECT * FROM items WHERE naam = ?", (naam,))
	if not c.fetchone():
		c.close()
		conn.close()
		return -1 #product niet in db
	else:
		c.execute("DELETE FROM items WHERE naam = ?", (naam,))
		conn.commit()
		c.close()
		conn.close()
		return 0

def HSGerecht(db, naam, active):
	conn = sqlite3.connect(db)
	c = conn.cursor()
	c.execute("SELECT * FROM items WHERE naam = ?", (naam,))
	if not c.fetchone():
		c.close()
		conn.close()
		return -1 #product niet in db
	else:
		c.execute("UPDATE items SET active = ? WHERE naam = ?", (active,naam))
		conn.commit()
		c.close()
		conn.close()
		return 0

def getTypeItem(db):
	conn = sqlite3.connect(db)
	c = conn.cursor()
	c.execute("SELECT type, naam FROM items WHERE active = 1")
	a = sorted(c.fetchall(),key=lambda x:x[1]) #enige manier om het te sorteren
	data = ''.join([f'{item[0]}.{item[1]},' for item in a])[:-1] #type.naam, verwijdert laatste komma
	c.close()
	conn.close()
	return data

#++++++++++++++++++ bestellingen ++++++++++++++++++

def bestelling(db, id, bestelling, tafel=None):
	'''
		db :: type string, name or path db
		id :: type int, number order
		bestelling :: type dict
		tafel :: type int, number table
	'''
	print(db, id, bestelling, tafel)
	#check voor id, als id er reeds is dan moet ik
	conn = sqlite3.connect(db)
	c = conn.cursor()
	c.execute("SELECT items FROM bestellingen WHERE id = ?", (id,))
	data = c.fetchone()
	if not data:
		try:
			c.execute("INSERT INTO bestellingen(id, tafel, items) VALUES(?,?,?)",(id, tafel, dumps(bestelling)))
		except:
			print("insert error")
			return -1
	else:
		try:
			data = loads(data[0])
			for key in bestelling:
				data[key] = data.get(key,0) + bestelling[key]
			print('\n\n'+str(data)+'\n\n')
			c.execute("UPDATE bestellingen SET items = ? WHERE id = ?", (dumps(data), id))
		except:
			print("update error")
			return -1
	conn.commit()
	c.close()
	conn.close()
	return 0
	
def getBestelling(db, id=None):
	conn = sqlite3.connect(db)
	c = conn.cursor()
	if id:
		c.execute("SELECT * FROM bestellingen WHERE id = ?", (id,))
	else:
		c.execute("SELECT * FROM bestellingen")
	data = {i[0]:(i[0], i[1], i[2], loads(i[3])) for i in [i for i in c.fetchall()]}
	conn.commit()
	c.close()
	conn.close()
	return data

def editBestelling(db, id, bestelling):
	#verandert bestelling volledig - gevaarlijk
	return 0

		
if __name__ == "__main__":
	#bestelling("test.db", 3, dumps({i:i**2 for i in range(10)}))
	#bestelling("test.db", 3, dumps({i:1 for i in range(2,8)}))
	pass
