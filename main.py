import os
import sqlite3

def db_init():
    global conn
    global cursor
    conn = sqlite3.connect('phonebookpy.db')  
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS names (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS phones (
                    id integer PRIMARY KEY AUTOINCREMENT,
                    phone TEXT NOT NULL UNIQUE,
                    name_id INTEGER NOT NULL,
                    CONSTRAINT fk_names
                    	FOREIGN KEY (name_id)
                    	REFERENCES names(id)
                    	ON UPDATE CASCADE
                    	ON DELETE CASCADE)''')
    cursor.execute('PRAGMA foreign_keys=ON')

def db_load():
    global conn
    conn.commit()
    global names
    global phones
    cursor.execute("SELECT * FROM names")
    names = dict(cursor.fetchall())
    cursor.execute("SELECT * FROM phones")
    phones = cursor.fetchall()

def print_menu():  
    print ('\033[34m','\nPlease select an action:','\033[0m')   
    print('1. Display contacts')
    print('2. Add new contact') 
    print('3. Find contacts')  
    print('4. Edit contacts')  
    print('5. Delete contacts')
    print('0. Exit the program')

def print_edit_menu():  
    print ('\033[34m','\nPlease select an action:','\033[0m')   
    print('1. Edit Name'.ljust(15), '2. Add phone'.ljust(15), '0. Exit & Save'.ljust(15))

def print_contact(cnt):
    print('id=', cnt, '|', names[cnt].rjust(25, '.'), end='|')
    for j in phones:
        if j[2] == cnt:
            print(j[1].ljust(12), end='|')

def find_contact():
    fstr = input('\033[34mEnter search string: \033[0m')
    if fstr.isdigit():
        for i in phones:
            if i[1] == fstr:
                print('\033[32mContact foud: \033[0m', end = ' ')
                print_contact(i[2]) # печатаем контакт используя поле phones.name_id
                return
    else:
        for i in names:
            if fstr.lower() in names[i].lower():
                print('\033[32mContact foud: \033[0m', end = ' ')
                print_contact(i) # при итерации словаря итератор является ключом
                return
    print('\033[31mContact NOT foud \033[0m')

def display_contacts2():
    print('\033[34mList of contacts\033[0m')
    for i in names:
        print_contact(i)    # печатаем контакт используя ключ словаря как аргумент
        print()

def new_contact():
    print('Creating new contact:')
    newphone = input('Enter new phone number -> ')
    if not newphone.isdigit():
        print('\033[31m','ERROR: entered not a number','\033[0m')
        return
    cursor.execute('SELECT id FROM phones where phone = ?', (newphone,))
    if cursor.fetchone() != None:
        print('\033[31m','ERROR: this phone already exists','\033[0m')
        return
    newname = input('Enter new name -> ')
    cursor.execute('SELECT id FROM names where name = ?', (newname,))
    if cursor.fetchone() != None:
        print('\033[31m','ERROR: this name already exists','\033[0m')
        return
    cursor.execute('INSERT INTO names VALUES(NULL, ?)', (newname,))
    last_row_id = cursor.lastrowid
    cursor.execute('INSERT INTO phones VALUES(NULL, ?, ?)', (newphone, last_row_id,))
    db_load()
    print('\033[32m','SUCCESS: contact added','\033[0m')

def delete_contact():
    delid = int(input('\033[34mEnter contact "id" to delete: \033[0m'))
    if delid in names:
        print_contact(delid)
        print()
        print('\033[34m Are you sure? (y/n): \033[0m')
        if input().lower() == 'y':
            cursor.execute('DELETE FROM names WHERE id=?', (delid,))
            # когда узнал что в sqlite по-умолчанию отключена поддержка foreign_keys
            # cursor.execute('DELETE FROM phones WHERE name_id=?', (delid,))
            db_load()
            print('\033[32m','SUCCESS: contact deleted','\033[0m')
    else:
        print('\033[31m','ERROR: \'id\' not found','\033[0m')

def edit_name(updid):
    newname = input('Enter new name -> ')
    cursor.execute('SELECT id FROM names where name = ?', (newname,))
    if cursor.fetchone() != None:
        print('\033[31m','ERROR: this name already exists','\033[0m')
        return
    cursor.execute('UPDATE names SET name = ? WHERE id = ?', (newname, updid))

def add_phone(addid):
    newphone = input('Enter new phone number -> ')
    if not newphone.isdigit():
        print('\033[31m','ERROR: entered not a number','\033[0m')
        return
    cursor.execute('SELECT id FROM phones where phone = ?', (newphone,))
    if cursor.fetchone() != None:
        print('\033[31m','ERROR: this phone already exists','\033[0m')
        return
    cursor.execute('INSERT INTO phones VALUES(NULL, ?, ?)', (newphone, addid))

def edit_contact():
   edid = int(input('\033[34mEnter contact "id" to edit: \033[0m'))
   if edid in names:
        print_contact(edid)
        action1 = None
        while action1 != '0':
            print_edit_menu()
            action1 = input('-> ').lower()
            if action1 == '1':
                edit_name(edid)
            elif action1 == '2':
                add_phone(edid)
        db_load()
        print('\033[32m','SUCCESS: contact updated','\033[0m')

os.chdir("PhoneBookPy")
db_init()
names = dict()  # имена будут храниться в словаре
phones = list() # а телефоны в списке
db_load()       # загружаем базу справочника в память
action = None
while action != '0':
    print_menu()
    action = input('-> ').lower()
    if action == '1':
       display_contacts2()
    elif action == '2':
        new_contact()
    elif action == '3':
        find_contact()
    elif action == '4':
        edit_contact()
    elif action == '5':
        delete_contact()
conn.close()
