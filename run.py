from quote_book import create_app
from quote_book.config import *

if __name__ == "__main__":
    app = create_app()
    
    app.run("0.0.0.0", port="80")
