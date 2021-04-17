from website import create_app  # __init__.py allow to import 'create_app'


app = create_app()


if __name__ == '__main__':
    app.run(host='localhost', debug=True)
