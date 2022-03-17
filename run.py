from quote_book import create_app
from quote_book.config import *

if __name__ == "__main__":
    app = create_app()
    
    app.run("127.0.0.1", port="80")
