from flask import render_template, request, redirect, url_for, send_file, flash
from app import app, db
from app.models import TagForm, Tag, File, FileForm, User, UserForm, Version, VersionForm, LoginForm
import os
from werkzeug.utils import secure_filename
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
# from werkzeug.routing import Rule
# app.url_map.add(Rule('/', endpoint='index'))

@app.route('/file', methods=['GET', 'POST'], endpoint='list_file')
@login_required
def list_file():
    files = File.query.all()
    return render_template("list_file.html", files=files)


@app.route('/file/form', endpoint='submit_file', methods=['GET', 'POST'])
@login_required
def submit_file():
    form = FileForm(meta={'csrf': False})
    if form.validate_on_submit():
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
        f = File(name=form.name._value(), user_id=form.user_id.data, type_id=form.type_id.data, file=file.filename)
        db.session.add(f)
        db.session.commit()
        return redirect(url_for('list_file'))
    return render_template("form_file.html", form=form)


@app.route('/file/dowload/<path:filename>', methods=['GET', 'POST'])
@login_required
def dowload_file(filename):
    return send_file("static/files/"+filename, as_attachment=True)



@app.route('/tag/form', endpoint='submit_tag11', methods=['GET', 'POST'])
@login_required
def submit_tag11():
    form = TagForm(meta={'csrf': False})
    if form.validate_on_submit():
        tag = Tag(
                tag=form.tag.data,
                number=form.number.data)
        db.session.add(tag)
        db.session.commit()
        return redirect(url_for('list_tag'))
    return render_template("form_tag1.html", form=form)

# app.add_url_rule("/", endpoint="index11", view_func=index11)
# app.add_url_rule("/tag/form", endpoint="submit_tag11", view_func=submit_tag11)


@app.route('/tag')
@login_required
def list_tag():
    tags = Tag.query.all()
    return render_template("list_tag.html", tags=tags)


@app.route('/user')
@login_required
def list_user():
    users = User.query.all()
    return render_template("list_user.html", users=users)


@app.route('/user/form', endpoint='form_user', methods=['GET', 'POST'])
def form_user():
    form = UserForm(meta={'csrf': False})
    if form.validate_on_submit():
        user = User(name=form.name.data,
                email=form.email.data,
                user_type_id=form.user_type_id.data,
                password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('list_user'))
    return render_template("form_user.html", form=form)


@app.route('/version')
@login_required
def list_version():
    vrs = Version.query.all()
    return render_template("list_version.html", versions=vrs)


@app.route('/version/form', endpoint='form_version', methods=['GET', 'POST'])
@login_required
def form_version():
    form = VersionForm(meta={'csrf': False})
    if form.validate_on_submit():
        vr = Version(version=form.version.data)
        db.session.add(vr)
        db.session.commit()
        return redirect(url_for('list_version'))
    return render_template("form_version.html", form=form)

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('list_file'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('list_file')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('list_file'))

if __name__ == "__main__":
    app.run(debug=True)
