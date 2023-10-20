from CarDealz_app import app
from CarDealz_app.models.user import User
from CarDealz_app.models.car import Car
from flask import render_template, redirect, request, session
from flask_bcrypt import Bcrypt
from flask import flash
bcrypt = Bcrypt(app) 

@app.route("/", methods = ['GET','POST'])
@app.route("/signup", methods = ['GET','POST'])
def signup():
    if request.method == "POST":
        if request.form['pswrd'] == request.form['pswrd_confirm']:
            data=dict(request.form)
            print("password", request.form['pswrd'])
            if request.form['pswrd'] == "" :
                flash("Input a Password")
                return redirect ('/')
            data['pswrd'] = bcrypt.generate_password_hash(request.form['pswrd'])
            if User.getAll() == None:
                data ['id']=1
            else:
                data ['id']=len(User.getAll()) + 1
            print (data)
            if User.user_validations(request.form):
                print("Super con las validaciones")
                user=User.save(data)
                session['id']=user.id
                return redirect ('/dashboard')
        else:
            flash("Password must be the same")
    return render_template('index.html')

@app.route("/signin", methods = ['GET','POST'])
def signin():
    if request.method == "POST":
        data=dict(request.form)
        db_user=User.getEmail(data.get('email'))
        print(db_user)
        if  db_user is None or not bcrypt.check_password_hash(db_user.password , data.get('pswrd')) :
            flash ("Invalid Email/Password")
            return redirect ('/')
        session["id"]=db_user.id
        return redirect ("/dashboard")
    else:
        return render_template('index.html')

@app.route("/dashboard")
def dashboard():
    if session.get('id') == None:
        return redirect ('/')
    else:
        user = User.getId(session.get('id'))
        all_cars=Car.getAll()
        all_purchased_cars=Car.getPurchased()
        owners_info=Car.getOwnersInfo()
        return render_template('dashboard.html', user=user, all_cars=all_cars, all_purchased_cars=all_purchased_cars, owners_info=owners_info)
@app.route ('/show/<int:car_id>')
def show(car_id):
    if session.get('id') == None:
        return redirect ('/')
    else:
        car=Car.getId(car_id)
        car_owner_info=Car.getCarOwnerInfo(car_id)
        return render_template('show_car.html',car=car, car_owner_info=car_owner_info)
@app.route('/delete/<int:car_id>')
def delete(car_id):
    if session.get('id') == None:
        return redirect ('/')
    car=Car.getId(car_id)
    data={}
    if session.get('id') == car.user_owner_id:
        data['id']=car.id
        data['user_owner_id']=car.user_owner_id
        Car.delete(data)
        return redirect ('/dashboard')
    else:
        return redirect ('/dashboard')

@app.route ('/new' , methods=['GET','POST'])
def new():
    if session.get('id') == None:
        return redirect ('/')
    if request.method == "POST":
        data=dict(request.form)
        if Car.validations(data):
            print('Super con car validations')
            if Car.getAll() == []:
                data ['id']=1
            else:
                data ['id']=len(Car.getAll())+1
            data ['user_owner_id'] = session.get('id')
            print(data)
            Car.save(data)
            return redirect ('/dashboard')
        else:
            return redirect ('/dashboard')
    else:
        return render_template('new.html')

@app.route ('/edit/<int:car_id>' , methods=['GET','POST'])
def edit(car_id):
    if session.get('id') == None:
        return redirect ('/')
    if request.method == "POST":
        data=dict(request.form)
        if Car.validations(data):
            print('Super con car validations')
            data ['id']=session.get('id')
            Car.edit(data)
            return redirect ('/dashboard')
        else:
            return redirect ('/dashboard')
    else:
        car=Car.getId(car_id)
        return render_template('edit.html', car=car)


@app.route ('/user_purchases')
def user_purchases():
    if session.get('id') == None:
        return redirect ('/')
    else:
        user=User.getId(session.get('id'))
        all_user_purchases=User.get_purchased_cars_by_user(session.get('id')).purchased_cars
        return render_template ('user_purchases.html', user=user, all_user_purchases=all_user_purchases)
@app.route('/purchase/<int:car_id>')
def purchase(car_id):
    if session.get('id') == None:
        return redirect ('/')
    else:
        user_buyer_id=session.get('id')
        data={
            'user_buyer_id':user_buyer_id,
            'car_id':car_id
        }
        User.purchase_car(data)
        return redirect ('/dashboard')

@app.route("/logout")
def logout():
    if session.get('id') == None:
        return redirect ('/')
    session.clear()
    return redirect ('/')