from flask import Flask

app = Flask(__name__)

@app.route('/taxis', methods=['GET'])
def get_taxis():
    return 'Hola Mundo'

if __name__ == '__main__':
    app.run(debug=True)
