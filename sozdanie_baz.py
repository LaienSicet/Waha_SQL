import sqlite3 as sql

#with sql.connect('baza_Waha_1.db') as con:
#    cur = con.cursor()
#    cur.execute(''' CREATE TABLE IF NOT EXISTS Astra_Militarum (
#        razdel INT,
#        nazv_ynita TEXT,
#        prais_1 INT,
#        prim_1 INT,
#        prais_2 INT,
#        prim_2 INT,
#        ynikaln BOOL
#        ) ''')



def nov_frak_baza (nazvanie, razmer=2):
    stroka = f''' CREATE TABLE IF NOT EXISTS {nazvanie} (
        razdel INT,
        nazv_ynita TEXT,
        prais_1 INT,
        prim_1 INT,
        prais_2 INT,
        prim_2 INT,
        ynikaln BOOL'''
    if razmer >= 3:
        stroka += ','\
                  'prais_3 INT,'\
                  'prim_3 INT'
    if razmer >= 4:
        stroka += ','\
                  'prais_4 INT,'\
                  'prim_4 INT'

    stroka += ')'
    with sql.connect('baza_Waha_1.db') as con:
        cur = con.cursor()
        cur.execute(f'DROP TABLE IF EXISTS {nazvanie}')
        cur.execute(stroka)

nov_frak_baza ('Adeptus_Custodes', razmer=4)