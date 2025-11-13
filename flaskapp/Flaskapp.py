from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def data_to():
    some_str = "название страницы опца дрица"
    some_value = 42
    some_pars = {'user':'Ivan','color':'red'}
    return render_template('simple.html',
                           some_str=some_str,
                           some_value=some_value,
                           some_pars=some_pars)

if __name__ == '__main__':
    app.run(debug=True)