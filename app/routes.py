from flask import  render_template, redirect, url_for, flash, request , abort,current_app
from app import app, db, bcrypt , mail, Mail
from app.forms import registerForm, LoginForm , PostForm, UpdateAccountForm , ResetPasswordForm , RequestRestForm
from app.models import User, Post
from flask_login import login_user, current_user , logout_user , login_required    
import secrets
import os
from PIL import Image #pil = to make picture size small
from flask_mail import Message




# posts = [
#     {
#         'author': 'YASSINE RAHHOU',
#         'title': 'Blog Post 1',
#         'content': 'First post content',
#         'date_posted': 'April 20, 2018'
#     },
#     {
#         'author': 'Jane Doe',
#         'title': 'Blog Post 2',
#         'content': 'Second post content',
#         'date_posted': 'April 21, 2018'
#     }
# ]


@app.route('/')
@app.route('/home')
def home():
       # this how will mak pagination to make our app reload fast 
    page=request.args.get('page',1, type=int)
    # + post ibano mn jdad qdim 
    posts= Post.query.order_by(Post.date_posted.desc()).paginate(page=page ,per_page=5)
    return render_template('index.html', title='HOME PAGE' , posts=posts)


@app.route('/public_sctr')
def public_sctr():
    return render_template('sctr_public.html' , title='public seture')


@app.route('/private')
def private_sctr():
    return render_template('sctr_prvt.html', test='PRIVATE PAGE' , title='Private secteur')


@app.route('/companies')
def companies():
    return render_template('Companies.html',title='companies')


@app.route('/Conta')
def conta():
    return render_template('Conta.html')


@app.route('/contact',  methods=['GET',  'POST'])
def contact():
    return render_template('contact.html')


@app.route("/register", methods=['GET',  'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = registerForm()
    if form.validate_on_submit():
        flash(f"ACCOUNT CREATED FOR{form.username.data}!, 'success")
        return redirect(url_for('home'))
    return render_template("register.html", form=form)


@app.route('/login',  methods=['GET',  'POST'])
def login():
    form = LoginForm()
    return render_template('sign_in.html', form='form')


@app.route('/test_login',  methods=['GET',  'POST'])
def test_login():
    form = LoginForm()

    if form.validate_on_submit():

        if form.email.data == 'admin@blog.com' and form.password.data == 'password':

            flash("You have been logged in !", 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('test_login.html', title='Login', form=form)

# start 12/6

@app.route('/login_3', methods=['GET', 'POST'])
def test_login_3():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()

    if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password,form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))
            else:

                flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('test_login_3.html', title='Login', form=form , legend='LOGIN PAGE')
@app.route("/register_3", methods=['GET',  'POST'])
def register_3():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = registerForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('test_login_3'))
    return render_template("register_3.html", form=form, title='register')


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


#  this function will take profile picture as a function 

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn
# randef save_pictureom picture name they ploas ; import secrets
    # _ = filename
  


@app.route('/account', methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form )


@app.route('/about')
def about():
    return render_template ('about.html',title='ABOUT US')
@app.route('/faq')
def faq():
    return render_template ('faq.html',title='faq')
@app.route('/Features')
def features():
    return render_template('Features.html',title='FEATURES')


@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        image_file = 'default.jpg'  # Default image if no file is provided
        if form.image.data:
            image_file = save_post_image(form.image.data)
        # db nazido posts database 
        category = form.category.data

        post = Post(title=form.title.data, content=form.content.data, author= current_user, image_file=image_file, category=category )
        db.session.add(post)
        db.session.commit()
        flash('Your post has been creates !', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form, legend='Update Post')

def save_post_image(form_image):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_image.filename)
    image_fn = random_hex + f_ext
    image_path = os.path.join(current_app.root_path, 'static/post_images', image_fn)

    output_size = (700, 500)
    i = Image.open(form_image)  # Use the file object, not the filename string
    i.thumbnail(output_size)
    i.save(image_path)

    return image_fn


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    
    if form.validate_on_submit():
        
        post.title = form.title.data
        post.content = form.content.data
        # change poste page 
        if form.image.data:
            # Save the new image and update the post's image field
            image_filename = save_post_image(form.image.data)
            post.image_file = image_filename
      
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
       
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')



@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted', 'success')
    return redirect(url_for('home'))
@app.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html',  posts=posts, user=user)

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestRestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('test_login_3'))
    return render_template('reset_request.html',
                                                   title='Reset Password', form=form , legend='REST PASSWORD')

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
     # mn b3d ma checkina bli ando token s7i7
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('test_login_3'))
    return render_template('reset_token.html', title='Reset Password', form=form , legend='RESET PASSWORD')

app.app_context().push()
