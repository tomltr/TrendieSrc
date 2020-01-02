from flask import render_template, url_for, redirect, flash, request, abort
from TrendieSrc import app, db
from TrendieSrc.models import Post, User
from TrendieSrc.forms import PostForm, RegistrationForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user, login_required

#Home Page
@app.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(private=False).order_by(Post.date_posted.desc()).paginate(page=page, per_page=10)
    return render_template('home.html', posts=posts)


#Creating a new post
@app.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, category=form.category.data, reference=form.reference.data, content=form.content.data, private=form.private.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post created', 'success')
        return redirect(url_for('home'))
    return render_template('new_post.html', title='New Post', form=form)

#Getting a single post by its id
@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post, content=post.content.split('\n'))

#Edit a single post by its id
@app.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user != post.author:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.category = form.category.data
        post.reference = form.reference.data
        post.content = form.content.data
        post.private = form.private.data
        db.session.add(post)
        db.session.commit()
        flash('Post updated', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.category.data = post.category
        form.reference.data = post.reference
        form.content.data = post.content
        form.private.data = post.private
    return render_template('new_post.html', title='Edit Post', form=form)

#Delete a single post by its id
@app.route('/post/<int:post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user != post.author:
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash('Post removed', 'success')
    return redirect(url_for('home'))

#Register a new user
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Registration success!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Registration', form=form)

#Logging in
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if (user and check_password_hash(user.password, form.password.data)):
            login_user(user)
            next_page = request.args.get('next')

            flash('Logged in', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Invalid email or password. Please try again', 'danger')
    return render_template('login.html', title='Login', form=form)

#Logging out
@app.route("/logout")
def logout():
    logout_user()
    flash('Logged out', 'success')
    return redirect(url_for('home'))

#Access user's account posts
@app.route('/account')
@login_required
def account():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(author=current_user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=10)
    return render_template('account.html', title='Account', posts=posts)