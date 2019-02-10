from livereload import Server
from src import app 

def main():
    server = Server(app.wsgi_app)
    server.watch('.')
    server.serve()

if __name__ == '__main__':
    main()