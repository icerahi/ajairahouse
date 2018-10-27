from flask import Flask,render_template,url_for,flash,redirect,request,abort
from ajaira import app,db,bcrypt,login_manager
from ajaira.form import RegistrationForm,LoginForm,UpdateForm,PostForm
from ajaira.models import User,Post
from flask_login import login_user,current_user,logout_user,login_required
import secrets
import os
from PIL import Image

active=True

@app.route("/")

@app.route("/home")
@login_required
def home():
    posts=Post.query.all()
    return render_template("home.html",posts=posts,active=active)

@app.route("/contest")
@login_required
def contest():
    user=User.query.all()

    return render_template("network.html",active=active,user=user )


def save_picture(form_picture):
    random_hex=secrets.token_hex(8)
    _, f_ext=os.path.splitext(form_picture.filename)
    picture_fn=random_hex+f_ext
    picture_path=os.path.join(app.root_path,"static/img",picture_fn)
    form_picture.save(picture_path)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn



@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file=save_picture(form.picture.data)
            current_user.image_file=picture_file
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


@app.route("/upload",methods=["GET","POST"])
@login_required
def upload():
    form=PostForm()
    if form.validate_on_submit():
        post=Post(title=form.title.data,content=form.content.data,author=current_user)

        db.session.add(post)
        db.session.commit()
        flash("YOur post has been created!","success")
        return redirect(url_for('home'))

    return render_template("upload.html",active=active,form=form,legend="New Post")


@app.route("/post/<int:post_id>")
def post(post_id):
    post=Post.query.get_or_404(post_id)
    return render_template('post.html',post=post,active=active)


@app.route("/post/<int:post_id>/update",methods=["GET","POST"])
@login_required
def update_post(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form=PostForm()
    if form.validate_on_submit():
        post.title=form.title.data
        post.content=form.content.data
        db.session.commit()
        flash("Your post has been update!","success")
        return redirect(url_for('post',post_id=post.id))
    elif request.method=="GET":
        form.title.data=post.title
        form.content.data=post.content
    return render_template('upload.html',post=post,form=form,legend="Update post",active=active)


@app.route("/post/<int:post_id>/delete",methods=["POST"])
@login_required
def delete_post(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("YOur post has delete successfully","success")
    return redirect("home")
