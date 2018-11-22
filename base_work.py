import sqlite3

def init_user(id, name_r, nickname, phone):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO users (id, name_r, nickname, phone, VIP) VALUES (?, ?, ? , ?, 0)',
        (id, name_r,nickname, phone))
    conn.commit()
    cursor.close()
    conn.close()

def all_id():
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users')
    f = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    e = []
    for  i in f:
        e.append(i[0])
    return e

def create_lot(id, image ,description, first_price, anonim):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name_r FROM users WHERE id =id',{'id':id})
    f = cursor.fetchone()[0]
    cursor.execute(
        'INSERT INTO lots (id, name_r,image, description, first_price, last_price, name_r_lp,id_lp, anonim, is_open, premium) VALUES (?, ?, ? , ?, ?,?,?,?,?,?,?)',
        (id, f,image, description, first_price, None, None,None, anonim, True, False))
    conn.commit()
    cursor.close()
    conn.close()

def all_lots():
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute('SELECT num ,name_r, image, description, first_price, last_price,is_open, premium, name_r_lp,id_lp, anonim FROM lots')
    f = cursor.fetchall()
    final = []
    for i in f:
        if i[6] == 1:
            final.append(i)
    conn.commit()
    cursor.close()
    conn.close()
    return final

def update_lot(num, last_price, id_lp):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name_r FROM users WHERE id =id', {'id': id_lp})
    f = cursor.fetchone()[0]
    cursor.execute('UPDATE lots SET last_price=?, id_lp=?, name_r_lp=? WHERE num=?', (last_price,id_lp,f,num))
    conn.commit()
    cursor.close()
    conn.close()


def close_lot(num, id):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE lots SET is_open=? WHERE num=? and id=?', (False,num,id))

    conn.commit()
    cursor.close()
    conn.close()
close_lot(10, 286077227)