urls = {
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

urls_navbar = {
    "home": f"{main_url}/home",
    "search": f"{main_url}/search",
    "info": f"{main_url}/info",
    "saves": f"{main_url}/saves",
    "reg": f"{main_url}/reg",
    "log": f"{main_url}/log",
    "forgot_pssword": f"{main_url}/forgot_password"
}

navbar_style = """

<style>
    .sidenav {
        height: 100%;
        width: 70px;
        position: fixed;
        z-index: 1;
        top: 0;
        left: 0;
        background-color: #DBEFED;
        overflow-x: hidden;
        padding-top: 20px;
        transition: 0.5s;
    }

    .sidenav:hover{
        width: 100px;
    }

    .sidenav a {
        position: relative;
        padding: 7px 8px 6px 16px;
        text-decoration: none;
        font-size: 25px;
        display: block;
        color: hsl(169, 15%, 48%);
    }

    .sidenav a img{
        height: 40px;
        transition: 0.5s;
    }

    .sidenav a img:hover{
        height: 60px;
    }
</style>
"""

navbar_body = f"""
<div class="sidenav", id="navbar">
        <a href="{urls_navbar['home']}"><img src="https://s3.timeweb.com/cc41600-sheeesh-shearcher/static/account_nav.svg"></a>
        <a href="{urls_navbar['search']}"><img src="https://s3.timeweb.com/cc41600-sheeesh-shearcher/static/search_nav.svg"></a>
        <a href="{urls_navbar['info']}"><img src="https://s3.timeweb.com/cc41600-sheeesh-shearcher/static/info_nav.svg"></a> 
        <a href="{urls_navbar['saves']}"><img src="https://s3.timeweb.com/cc41600-sheeesh-shearcher/static/saves_nav.svg"></a> 
    </div>
"""

updates = ["Полностью обновлён дизайн", "Теперь можно выйти из своего аккаунта","Доработана функция сохранения цитат в личный список"]

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