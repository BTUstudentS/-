from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy

# thronesdb.sqlite ( ცხრილი - Characters )

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mini-project'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///thronesdb.sqlite'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String)
    password = db.Column(db.String)

class Throne(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    fullname = db.Column(db.String(80), nullable=False)
    title = db.Column(db.String(80), nullable=False)
    family = db.Column(db.String(80), nullable=False)
    image = db.Column(db.String(80))
    imageUrl = db.Column(db.String(200))

    def __str__(self):
        return f'სრული სახელი: {self.fullname}, თანამდებობა: {self.title}, ოჯახი: {self.family}, ფოტო: {self.image}, ფოტოს Url {self.imageUrl}'


with app.app_context():
    db.create_all()
    T2 = Throne.query.all()
    for i in T2:
        print(i)

@app.route('/')
def home():
    all_characters = Throne.query.all()
    return render_template('index.html', all_characters=all_characters)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
    return render_template('login.html')


@app.route('/resourses')
def resourses():
    return redirect('https://thronesapi.com/')


@app.route('/user', methods=['POST', 'GET'])
def user():
    if request.method == 'POST':
        characters = Throne.query.all()
        names = request.form['name']
        lastnames = request.form['lastname']
        titles = request.form['title']
        familys = request.form['family']
        if lastnames == '' and titles == '' and familys == '':
            all_names = Throne.query.filter_by(name=names).all()
            flash('პერსონაჟი მოძებნილია', 'info')
            return all_names
        elif names == '' and titles == '' and familys == '':
            all_lastnames = Throne.query.filter_by(lastname=lastnames).all()
            flash('პერსონაჟი მოძებნილია', 'info')
            return all_lastnames
        elif names == '' and lastnames == '' and familys == '':
            all_titles = Throne.query.filter_by(title=titles).all()
            flash('პერსონაჟი მოძებნილია', 'info')
            return all_titles
        elif names == '' and lastnames == '' and titles == '':
            all_familys = Throne.query.filter_by(family=familys).all()
            flash('პერსონაჟი მოძებნილია', 'info')
            return all_familys
        elif titles == '' and familys == '':
            fullnames = names + lastnames
            all_fullnames = Throne.query.filter_by(fullname=fullnames).all()
            flash('პერსონაჟი მოძებნილია', 'info')
            return all_fullnames
        else:
            return 'თუ შეიძლება მონაცემები შეიყვანეთ სწორად'
        return render_template('user.html')
    if request.method == 'GET':
        pass
    return render_template('user.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return 'you are logged out'


@app.route('/thrones', methods=['GET', 'POST'])
def thrones():
    if request.method == 'POST':
        na = request.form['name']
        las = request.form['lastname']
        n_l = request.form['fullname']
        tit = request.form['title']
        fam = request.form['family']
        img = request.form['image']
        imgUrl = request.form['imageUrl']
        if na == '' or las == '' or n_l == '' or tit == '' or fam == '' or img == '' or imgUrl == '':
            flash('შეავსეთ ყველა ველი', 'error')
        else:
            T1 = Throne(name=na, lastname=las,  fullname=n_l, title=tit, family=fam, image=img, imageUrl=imgUrl )
            db.session.add(T1)
            db.session.commit()
            flash('პერსონაჟი დამატებულია', 'info')
    return render_template('characters.html')


if __name__ == "__main__":
    app.run(debug=True)