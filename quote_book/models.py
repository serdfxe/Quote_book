from flask import session
import secrets
from quote_book.init_db import quote_db, user_db
import smtplib
from quote_book.config import email_password, email_addres, main_url
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Quote_book_db():
    _connection = quote_db
    _cursor = _connection.cursor()


    def make_connection():
        '''make connection to DB'''
        return Quote_book_db._connection, Quote_book_db._cursor


    def make_message_from_list(list):
        connection, cursor = Quote_book_db.make_connection()

        message = []

        for cit_id in list:
            cursor.execute("""SELECT body, catID, ID FROM deals WHERE ID='%s'""" % cit_id)
            rec = cursor.fetchone()
            if rec!=None:
                body = rec[0]
                nameID = rec[1]
                citID = rec[2]

                cursor.execute("""SELECT catname FROM cat WHERE ID = '%s'""" % nameID)
                name = cursor.fetchone()
                
                message.append({'body':body,'author':name[0], 'id':citID})

        return message


    def get_quotes_from_user_list(name):
        """get quotes from user_list"""
    
        list = User_db.get_user_list(name)
        
        return Quote_book_db.make_message_from_list(list)


    def search_quotes(query):
        '''search quotes in quote_db'''
        connection, cursor = Quote_book_db.make_connection()
        
        mes = set()
        message = []
        s = query.strip()

        #поиск по name
        cursor.execute("""SELECT ID FROM cat WHERE catname LIKE '%s'""" % f'%{s}%')
        nameID_rec = cursor.fetchall()

        for i in nameID_rec:
            cursor.execute("""SELECT ID FROM deals WHERE catID = '%s'""" % i)
            for ii in cursor.fetchall():
                mes.add(ii)

        #поис по body
        cursor.execute("""SELECT ID FROM deals WHERE body LIKE '%s'""" % f'%{s}%')
        dealsID_rec = cursor.fetchall()

        mes = mes.union(dealsID_rec)
        
        connection, cursor = Quote_book_db.make_connection()

        message = []

        for cit_id in mes:
            cursor.execute("""SELECT body, catID, ID FROM deals WHERE ID='%s'""" % cit_id)
            rec = cursor.fetchone()
            if rec!=None:
                body = rec[0].replace(s, "<mark>"+s+"</mark>")
                nameID = rec[1]
                citID = rec[2]

                cursor.execute("""SELECT catname FROM cat WHERE ID = '%s'""" % nameID)
                name = cursor.fetchone()[0].replace(s, "<mark>"+s+"</mark>")
                
                message.append({'body':body,'author':name, 'id':citID})

        return message  


class User_db():
    _connection = user_db
    _cursor = _connection.cursor()


    def make_connection():
        '''make connection to DB'''

        return User_db._connection, User_db._cursor


    def get_user_list(name):
        if name == None: return []

        connection, cursor = User_db.make_connection()
        cursor.execute("""SELECT info FROM users WHERE name='%s'""" % name)
        info = eval(cursor.fetchone()[0])
        return info


    def is_in_db(name):
        '''is name in database'''

        connection, cursor = User_db.make_connection()

        cursor.execute("""SELECT userid FROM users WHERE name='%s'""" % name)

        if cursor.fetchall()==[]:
            return False

        return True


    def add_user_to_db(name, password, info):
        '''add new user to db'''

        if User_db.is_in_db(name): return False

        connection, cursor = User_db.make_connection()

        cursor.execute('''SELECT userid FROM users''')
        newid = len(cursor.fetchall())
        cursor.execute("""INSERT INTO users(userid, name, password, info, email) VALUES(?,?,?,?,?);""", (newid, name, password, str(info), None))

        cursor.execute("""INSERT INTO confirm_users(name, email, token) VALUES(?, ?, ?)""", (name, None, secrets.token_urlsafe()))
        connection.commit()
        return True


    def check_password(name, password):
        '''is password correct'''
        
        if not User_db.is_in_db(name): return False

        connection, cursor = User_db.make_connection()

        cursor.execute("""SELECT password FROM users WHERE name = '%s'""" % name)
        password_from_db = cursor.fetchone()[0]

        return password == password_from_db


    def login(name, password):
        access = User_db.check_password(name, password)
        if access: session['name'] = name
        return access


    def add_quote_to_user_list(name, quoteID):
        connection, cursor = User_db.make_connection()
        cursor.execute("""SELECT info FROM users WHERE name='%s'""" % name)
        info = cursor.fetchone()
        
        if info != None:
            info = eval(info[0])
            if str(quoteID) not in info: info.append(str(quoteID))
            
            cursor.execute("""UPDATE users set info = "%s" WHERE name='%s'""" % (str(info), name))
            connection.commit()


    def remove_quote_from_user_list(name, quoteID):
        connection, cursor = User_db.make_connection()
        cursor.execute("""SELECT info FROM users WHERE name='%s'""" % name)
        info = cursor.fetchone()
        
        if info != None:
            info = eval(info[0])
            if quoteID in info: info.remove(quoteID)
            
            cursor.execute("""UPDATE users set info = "%s" WHERE name='%s'""" % (str(info), name))
            connection.commit()


    def change_value(name, column, value):
        connection, cursor = User_db.make_connection()

        if column == "token":
            cursor.execute("""UPDATE users set token = "%s" WHERE name='%s'""" % (value, name))
            connection.commit()
            return

        cursor.execute("""UPDATE users set '%s' = "%s" WHERE name='%s'""" % (column, value, name))
        connection.commit()

        if column == 'email':
            cursor.execute("""UPDATE confirm_users set '%s' = "%s" WHERE name='%s'""" % (column, value, name))
            connection.commit()

 
    def get_user_info(name, *columns):
        connection, cursor = User_db.make_connection()
        cursor.execute("""SELECT %s FROM users WHERE name='%s'""" % (",".join(columns), name))
        res = cursor.fetchone()
        ans = {}
        try:
            for i in range(len(res)):
                ans[columns[i]] = res[i]
        except Exception:
            return ''
        return ans


    def get_info_from_confirm_users(col, val, *columns):
        connection, cursor = User_db.make_connection()
        cursor.execute("""SELECT %s FROM confirm_users WHERE %s='%s'""" % (",".join(columns), col, val))
        res = cursor.fetchone()
        print('get_info_from_confirm_users = ',res)
        ans = {}
        try:
            for i in range(len(res)):
                ans[columns[i]] = res[i]
        except Exception:
            return ''
        return ans


    def change_password(form, token):
        if form["password"] != form["rep_password"]: return False, 'Пароли не совпадают!'

        info = User_db.get_info_from_confirm_users('token', token, 'name')
        if info == '': return False, 'Что-то не так с ссылкой!'

        name = info['name']
        print(name)
        User_db.change_value(name, 'password', form["password"])

        return True, ''


class Email():
    _addres = email_addres
    _password = email_password

    def auth():
        smtp = smtplib.SMTP("smtp.timeweb.ru")
        print(smtp.login(Email._addres, Email._password, 'portable'))
        return smtp

    
    def send_message(to, sub, body):
        smtp = smtplib.SMTP("smtp.timeweb.ru")
        smtp.starttls() 
        print(f'addres = {Email._addres} password = {Email._password}')
        print(smtp.login(Email._addres.encode('ascii'), Email._password.encode('ascii')))
       
        msg = MIMEMultipart()
        message = body
        msg['From'] = Email._addres
        msg['To'] = to
        msg['Subject'] = sub
        msg.attach(MIMEText(message, 'plain'))
        
        smtp.sendmail(msg['From'], msg['To'], msg.as_string())
        
        smtp.quit()


    def send_token_to_user(form):
        print(form)

        if all([form[i] == '' for i in form]): return False, ''

        email = form['email']
        name = form['name']

        if email != '':
            info = User_db.get_info_from_confirm_users("email", email, 'token')
        else:
            if not User_db.is_in_db(name): return False, ''

            info = User_db.get_info_from_confirm_users("name", name, 'token','email')

        if info == '': return False, ''

        if email == '': email = info['email']

        token = info["token"]
        print(f'email={email} token={token}')
        Email.send_message(email, 'Восстановление пароля', f'Перейдите по ссылке для смены пароля:\n{main_url}/change_password/{token}')
        return True, email[:4]+"*"*len(email[4:-3])+email[-3:]
