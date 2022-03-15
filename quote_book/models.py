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

        cursor.execute("""INSERT INTO confirm_users(name, email, token, email_status) VALUES(?, ?, ?, ?)""", (name, None, secrets.token_urlsafe(), 0))
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
        for i in range(len(res)):
            ans[columns[i]] = res[i]
        return ans


    def get_info_from_confirm_users_by_name(name, *columns):
        connection, cursor = User_db.make_connection()
        cursor.execute("""SELECT %s FROM confirm_users WHERE name='%s'""" % (",".join(columns), name))
        res = cursor.fetchone()
        print(res)
        ans = {}
        for i in range(len(res)):
            ans[columns[i]] = res[i]
        return ans


    def get_info_from_confirm_users_by_email(email, *columns):
        connection, cursor = User_db.make_connection()
        cursor.execute("""SELECT %s FROM confirm_users WHERE email='%s'""" % (",".join(columns), email))
        res = cursor.fetchone()
        print(res)
        ans = {}
        for i in range(len(res)):
            ans[columns[i]] = res[i]
        return ans


class Email():
    _addres = email_addres
    _password = email_password

    def auth():
        smtp = smtplib.SMTP("smtp.timeweb.ru")
        print(smtp.login(Email._addres, Email._password))
        return smtp

    
    def send_message(to, sub, body):
        smtp = smtplib.SMTP("smtp.timeweb.ru")
        print(smtp.login(Email._addres, Email._password))

        msg = MIMEMultipart()
        message = body
        msg['From'] = Email._addres
        msg['To'] = to
        msg['Subject'] = sub
        msg.attach(MIMEText(message, 'plain'))
        
        smtp.starttls()
        
        smtp.sendmail(msg['From'], msg['To'], msg.as_string())
        
        smtp.quit()


    def send_token_to_user(form):
        print(form)
        if all([form[i] == '' for i in form]): False
        email = form['email']
        name = form['name']
        if email != '':
            token = User_db.get_info_from_confirm_users_by_email(email, 'token')['token']
        else:
            if not User_db.is_in_db(name): return False
            info = User_db.get_info_from_confirm_users_by_name(name, 'token','email')
            token = info["token"]
            email = info["email"]
        if token == None: return False
        print(f'email={email} token={token}')
        Email.send_message(email, 'Восстановление пароля', f'Перейдите по ссылке для смены пароля:\n{main_url}/change_password/{token}')
        return True
