from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('sign_in.html')


@app.route('/public_sctr')
def public_sctr():
    return render_template('sctr_public.html')


@app.route('/private')
def private_sctr():
    return render_template('sctr_prvt.html', test='AAA')


@app.route('/companies')
def companies():
    return render_template('Companies.html')


@app.route('/Conta')
def conta():
    return render_template('Conta.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(debug=True, port=9000)
