from flask import Flask, render_template, abort, redirect, request, url_for, flash, session
from flask_migrate import Migrate
from flask_login import login_user, login_required, logout_user, current_user
from forms import *
from models import db, login_manager, User, Ppay, Hpay
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['SECRET_KEY'] = 'supersecretkeydonthack'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/digitalpayment'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://8NxFFu2fxx:LOMVTDxNtg@remotemysql.com/8NxFFu2fxx'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'pratikshaprojectmail@gmail.com'
app.config['MAIL_PASSWORD'] = 'Digital@8600'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

db.init_app(app)
Migrate(app, db)

login_manager.init_app(app)

login_manager.login_view = "login"

@app.errorhandler(404)
@login_required
def page_not_found(e):
    user = session['user']
    return render_template('404.html', user=user), 404


@app.route('/')
def index():
    return redirect(url_for('register'))


@app.route('/addadmin', methods=['GET', 'POST'])
def addadmin():
    form = RegistrationForm()
    if form.validate_on_submit():
        email = User.query.filter_by(email=form.email.data).first()
        if email is None:
            username = User.query.filter_by(username=form.username.data).first()
            if username is None:
                register = User(firstname=form.firstname.data, lastname=form.lastname.data,
                                email=form.email.data, username=form.username.data, password=form.password.data,
                                is_admin=True)
                db.session.add(register)
                db.session.commit()
                flash('Congrats you have registered successfully!, Please check your inbox')
                welcome = form.firstname.data + ' ' + form.lastname.data + ' Welcome to Digital Payment Book'
                msg = Message(
                    'Welcome',
                    sender='pratikshaprojectmail@gmail.com',
                    recipients=[form.email.data]
                )
                msg.body = welcome
                mail.send(msg)

                return redirect(url_for('login'))
            else:
                flash('Username already exists, please try again!')
                return redirect(url_for('addadmin'))
        else:
            flash('Email already exists, please try logging in!')
            return redirect(url_for('addadmin'))

    return render_template('addadmin.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        email = User.query.filter_by(email=form.email.data).first()
        if email is None:
            username = User.query.filter_by(username=form.username.data).first()
            if username is None:
                register = User(firstname=form.firstname.data, lastname=form.lastname.data,
                                email=form.email.data, username=form.username.data, password=form.password.data,
                                is_admin=False)
                db.session.add(register)
                db.session.commit()
                flash('Congrats you have registered successfully!, Please check your inbox')
                welcome = form.firstname.data + ' ' + form.lastname.data + ' Welcome to Digital Payment Book'
                msg = Message(
                    'Welcome',
                    sender='pratikshaprojectmail@gmail.com',
                    recipients=[form.email.data]
                )
                msg.body = welcome
                mail.send(msg)

                return redirect(url_for('register'))
            else:
                flash('Username already exists, please try again!')
                return redirect(url_for('register'))
        else:
            flash('Email already exists, please try logging in!')
            return redirect(url_for('register'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None:
            if user.check_password(form.password.data):
                # session['user'] = form.username.data
                login_user(user)
                if user.is_admin == True:
                    return redirect(url_for('customers'))
                else:
                    next = request.args.get('next')
                    if next == None or not next[0] == '/':
                        next = url_for('userpending')
                    return redirect(next)
        flash('Username/password not found!')
        return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route('/customers', methods=['GET', 'POST'])
@login_required
def customers():
    user = current_user.username
    if current_user.is_admin == True:
        view_customers = User.query.filter_by(is_admin=False)
        return render_template('customers.html', view_customers=view_customers, user=user)
    else:
        return abort(404)


@app.route('/addpayment/<string:id>', methods=['GET', 'POST'])
@login_required
def addpayment(id):
    user = current_user.username
    user_email = db.session.query(User.email).filter(User.id == id).first()
    uemail = user_email[0]
    payments = Ppay.query.filter_by(user_id=id).first()
    if payments:
        flash('Previous Amount Pending!')
        return redirect(url_for('pending'))
    else:    
        form = AddPaymentForm()
        if form.validate_on_submit():
            product = form.product.data
            total_amount = form.total_amount.data
            paid_amount = form.paid_amount.data
            pending_amount = total_amount - paid_amount
            if pending_amount == 0:
                pass
            else:
                payment = Ppay(product=product, total_amount=total_amount, paid_amount=paid_amount,
                               pending_amount=pending_amount, user_id=id)
                welcome ='We hope you loved shopping with us. Please pay your Pending amount as soon as possible.'
                msg = Message(
                    'Alert',
                    sender='pratikshaprojectmail@gmail.com',
                    recipients=[uemail]
                )
                msg.body = welcome
                mail.send(msg)
                db.session.add(payment)
                db.session.commit()
                flash('Payment added successfuly')

                return redirect(url_for('customers'))
        return render_template('addpayment.html', form=form, user=user)


@app.route('/pending')
@login_required
def pending():
    user = current_user.username
    if current_user.is_admin == True:
        pending = Ppay.query.all()
        return render_template('pending.html', pending=pending, user=user)
    else:
        return abort(404)

@app.route('/history')
@login_required
def history():
    user = current_user.username
    if current_user.is_admin == True:
        history = Hpay.query.all()
        return render_template('history.html', history=history, user=user)
    else:
        return abort(404)


@app.route('/close/<string:id>', methods=['GET', 'POST'])
@login_required
def close(id):
    if current_user.is_admin == True:
        customer_email = db.session.query(User.email).filter(User.id == id).first()
        total = db.session.query(Ppay.total_amount).filter(Ppay.user_id == id).first()
        product = db.session.query(Ppay.product).filter(Ppay.user_id == id).first()
        close = Hpay(customer_email=customer_email[0], product=product[0], amount=total[0], user_id=id)
        db.session.add(close)
        Ppay.query.filter_by(user_id=id).delete()
        db.session.commit()
        flash('Payment Closed!')
        return redirect(url_for('customers'))
    else:
        return abort(404)


@app.route('/userpending')
@login_required
def userpending():
    if current_user.is_admin == False:
        user = current_user.username
        user_id = db.session.query(User.id).filter(User.username == user).first()
        payments = Ppay.query.filter_by(user_id=user_id.id)
        return render_template('userpending.html', payments=payments, user=user)
    else:
        return abort(404)


@app.route('/userhistory')
@login_required
def userhistory():
    if current_user.is_admin == False:
        user = current_user.username
        user_id = db.session.query(User.id).filter(User.username == user).first()
        payments = Hpay.query.filter_by(user_id=user_id.id)
        return render_template('userhistory.html', payments=payments, user=user)
    else:
        return abort(404)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/messages', methods=['GET', 'POST'])
@login_required
def messages():
    if current_user.is_admin == False:
        user = current_user.username
        form = MessageForm()
        admin = db.session.query(User.email).filter(User.is_admin == True).first()
        admine = admin[0]
        if form.validate_on_submit():
            user = current_user.email
            issue = 'From: ' + user + 'Message: ' + form.messages.data
            msg = Message(
                'Issue',
                sender='pratikshaprojectmail@gmail.com',
                recipients=[admine]
            )
            msg.body = issue
            mail.send(msg)
            flash('Issue sent Successfully')
            return redirect(url_for('messages'))
        return render_template('messages.html', form=form, user=user)
    else:
        return abort(404)


if __name__ == "__main__":
    app.run(debug=True)