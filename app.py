from flask import Flask,Request,render_template,session,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
import models
import csv
import requests



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'

db = SQLAlchemy(app)


class Contact(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50))
    number = db.Column(db.String(11))
    mail = db.Column(db.String)
    message = db.Column(db.String(10))

    def __repr__(self):
        return f"register('{self.name}')"


@app.route("/")
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact',methods=["GET","POST"])
def contact():
    return render_template('contact.html')

@app.route('/contacts',methods=['GET','POST'])
def contacts():
    if request.method == 'POST':
        name = request.form['name']
        number = request.form['number']
        mail = request.form['mail']
        message = request.form['message']
        entry = Contact(name=name,number=number,mail=mail,message=message)
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('contact'))




    
@app.route('/books')
def books():
    return render_template('Books.html')

@app.route('/details',methods=['GET','POST'])
def details():
    if request.method == 'GET':
        return render_template('review.html')
    elif request.method == 'POST':
        res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "TQZvfyF3DlIkCm9e7PWFxw", "isbns": "0553803700",})
        return res.json()



    
@app.route('/csv',methods=['GET','POST'])
def csvv(): 
    if request.method == 'GET':
        return render_template('csv.html')
    elif request.method == 'POST':
        results = []
        
        user_csv = request.form.get('user_csv').split('\n')
        reader = csv.DictReader(user_csv)
        
        for row in reader:
            results.append(dict(row))

        fieldnames = [key for key in results[0].keys()]

        return render_template('csv.html', results=results, fieldnames=fieldnames, len=len)

@app.route('/search',methods=['GET','POST'])
def search():
    if request.method == 'GET':
        return render_template('search.html')
    else:
        query = request.form.get('search-input')
        if query is None:
            return('Please Put something there')
        try:
            result = db.session.execute("SELECT isbn,title,author FROM book WHERE (isbn) LIKE :query OR (title) LIKE :query OR (author) LIKE :query", {"query": "%" + query.lower() + "%"}).fetchall()
        except Exception:
            return ('Error in query')

        if not result:
            return ('Not Found')
        return render_template('list.html',result=result)

@app.route()


    
    


if __name__ == "__main__":
    app.run(debug=True)