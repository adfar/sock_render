import os
from flask import Flask, render_template, request, url_for, redirect
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
socketio = SocketIO(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    price = db.Column(db.String(10), nullable=False)
    status = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'{self.name}'

@app.route('/')
def index():
    fudge = ['Fudge', 'Fudge Special, 6 pc.']
    fudges = [Item.query.filter_by(name=name).one() for name in fudge]
    chocolate = ['Chocolate Dipped Oreo', 'Chocolate Dipped Oreo 3-pack', 'Chocolate Dipped Pretzel Rod', 'Chocolate Dipped Pretzel Rod 3-pack', 'Chocolate Dipped Strawberry']
    chocolates = [Item.query.filter_by(name=name).one() for name in chocolate]
    apple = ['Caramel Apple', 'Candy Apple']
    apples = [Item.query.filter_by(name=name).one() for name in apple]
    candy = ['Cotton Candy', 'Cotton Candy 2-bag Deal', 'Salt Water Taffy 1/2 lb.', 'Salt Water Taffy 1 lb.', 'Rock Candy']
    candies = [Item.query.filter_by(name=name).one() for name in candy]
    drink = ['Small', 'Medium', 'Large', 'Souvenir Cup', 'Bottled Water']
    drinks = [Item.query.filter_by(name=name).one() for name in drink]
    bev = ['Pepsi', 'Diet Pepsi', 'Dr Pepper', 'Mountain Dew', 'Orange Crush', 'Sierra Mist', 'Brisk Iced Tea', 'Sobe Lifewater']
    bevs = [Item.query.filter_by(name=name).one() for name in bev]
    return render_template('index.html', items=Item.query.all(), fudges=fudges, chocolates=chocolates, apples=apples, candies=candies, drinks=drinks, bevs=bevs)

@app.route('/click', methods=['GET', 'POST'])
def click():    
    if request.method == "POST":
        item = str(request.form['item'])
        menu_item = Item.query.filter_by(name=item).first()
        menu_item.status = not menu_item.status
        status = menu_item.status
        price = menu_item.price
        db.session.commit()
        socketio.emit('out', {'name':item, 'status':status, 'price':price})
    return render_template('click.html', items=Item.query.all())

if __name__ == '__main__':
    socketio.run(app, port=8080, host='0.0.0.0')