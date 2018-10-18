from flask import Flask,render_template,url_for,flash,redirect
from form import RegistrationForm,LoginForm

app=Flask(__name__)
active=True
app.config["SECRET_KEY"]="9876fvb076fth867ftvb76f"


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html",active=active)

@app.route("/contest")
def contest():
    return render_template("contest.html",active=active)

@app.route("/upload")
def upload():
    return render_template("upload.html",active=active)

@app.route("/profile")
def profile():
    return render_template("profile.html",active=active)

@app.route("/login",methods=["GET","POST"])
def login():
    loginform=LoginForm()
    if loginform.validate_on_submit():
        if loginform.email.data=="rahi@gmail.com" and loginform.password.data=="rahi":
            flash("login hass success","success")
            return redirect(url_for('home'))
        else:
            flash("Please check your email and password.And Try Again!","danger")
    return render_template("login.html",loginform=loginform)

@app.route("/register",methods=["GET","POST"])
def register():
    registrationform=RegistrationForm()
    if registrationform.validate_on_submit():
        flash("Account successfully create for %s"%(registrationform.username.data),"success")
        return redirect(url_for('home'))
    return render_template("register.html",registrationform=registrationform)


if __name__=="__main__":
    app.run(debug=True)
