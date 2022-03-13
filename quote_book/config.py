from distutils.command import config
import os
from dotenv import dotenv_values


urls_to_files = {
    "search": "search.html",
    "reg": "registration.html",
    "home": "home.html",
    "log": "login.html",
    "forgot_password": '',
    "saves": "saves.html",
    "info": "info.html"
}

main_url = 'http://sheeesh.ru'
main_url = "http://127.0.0.1"

urls = {
    "home": f"{main_url}/home",
    "search": f"{main_url}/search",
    "info": f"{main_url}/info",
    "saves": f"{main_url}/saves",
    "reg": f"{main_url}/reg",
    "log": f"{main_url}/log",
    "forgot_password": f"{main_url}/forgot_password"
}

navbar_body = f"""
<div class="sidenav", id="navbar">
        <a href="{urls['home']}"><img src="https://s3.timeweb.com/cc41600-sheeesh-shearcher/static/account_nav.svg"></a>
        <a href="{urls['search']}"><img src="https://s3.timeweb.com/cc41600-sheeesh-shearcher/static/search_nav.svg"></a>
        <a href="{urls['info']}"><img src="https://s3.timeweb.com/cc41600-sheeesh-shearcher/static/info_nav.svg"></a> 
        <a href="{urls['saves']}"><img src="https://s3.timeweb.com/cc41600-sheeesh-shearcher/static/saves_nav.svg"></a> 
    </div>
"""

updates = ["Полностью обновлён дизайн", "Теперь можно выйти из своего аккаунта","Доработана функция сохранения цитат в личный список", "Теперь при поиске выделяются совпадения", "Теперь можно добавить плчту к аккаунту"]

paths = {
    'data':'/Users/pasha/Desktop/крутая папка/проги/projects/Quote_book/quote_book/data.sqlite',
    'users':'/Users/pasha/Desktop/крутая папка/проги/projects/Quote_book/quote_book/users_data.db'
}

paths = {
    'data':'/Users/pavel/Desktop/pr/Quote_book/quote_book/data.sqlite',
    'users':'/Users/pavel/Desktop/pr/Quote_book/quote_book/users_data.db'
}

'''
paths = {
    'data':'/root/Quote_book/quote_book/data.sqlite',
    'users':'/root/Quote_book/quote_book/users_data.db'
}
'''

conf = dotenv_values(".gitignore\.env")

email_addres = 'info@sheeesh.ru'
email_password = conf['EMAIL_PASSWORD']