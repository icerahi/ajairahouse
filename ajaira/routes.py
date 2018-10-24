from flask import Flask,render_template,url_for,flash,redirect,request
from ajaira import app,db,bcrypt,login_manager
from ajaira.form import RegistrationForm,LoginForm,UpdateForm
from ajaira.models import User,Post
from flask_login import login_user,current_user,logout_user,login_required

active=True

@app.route("/")

@app.route("/home")
@login_required
def home():
    return render_template("home.html",active=active)

@app.route("/contest")
@login_required
def contest():
    user=User.query.all()
    return render_template("network.html",active=active,user=user)

@app.route("/upload")
@login_required
def upload():
    return render_template("upload.html",active=active)


@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateForm()
    if form.validate_on_submit():

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='img/' + current_user.image_file)
    return render_template('profile.html', title='Account',image_file=image_file, form=form,active=active)



@app.route("/login",methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    loginform=LoginForm()
    if loginform.validate_on_submit():
        user=User.query.filter_by(email=loginform.email.data).first()
        if user and bcrypt.check_password_hash(user.password,loginform.password.data):
            login_user(user,remember=loginform.remember.data)
            flash("Hello %s you login has successfull"%(user.username),"success")
            next_page=request.args.get('next')

            return redirect(next_page) if next_page else redirect(url_for('home'))

        else:
            flash("Please check your email and password.And Try Again!","danger")
    return render_template("login.html",loginform=loginform)



@app.route("/register",methods=["GET","POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    registrationform=RegistrationForm()
    if registrationform.validate_on_submit():
        hash_password=bcrypt.generate_password_hash(registrationform.password.data).decode('utf-8')
        user=User(username=registrationform.username.data,email=registrationform.email.data,password=hash_password)
        db.session.add(user)
        db.session.commit()

        flash("Account successfully create for %s now you may login "%(registrationform.username.data),"success")
        return redirect(url_for('login'))
    return render_template("register.html",registrationform=registrationform)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))
if __name__=="__main__":
    app.run(debug=True)
