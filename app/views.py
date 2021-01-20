from datetime import datetime

from flask import render_template, request, redirect, make_response
from flask_babelex import lazy_gettext
from flask_login import login_required, login_user, logout_user

from Documents.testdata import Testdata
from app.forms.login import LoginForm
from app import app
from app.services.imageprocessing import render_test_result
from app.user.models import User


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html', form=form, page_title=lazy_gettext(u'Log in'),
        get_text=lazy_gettext)
    elif request.method == 'POST':
        if form.validate_on_submit():
            user = User.objects(username=form.username.data).first()
            if user:
                if user.password == form.password.data:
                    login_user(user)
                    return redirect('/admin')
                else:
                    form.password.errors.append("Wrong Password")
            else:
                form.username.errors.append("user doesn't exist")
        return render_template('login.html', form=form, page_title=lazy_gettext(u'Log in'),
                               get_text=lazy_gettext)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")


@app.route("/testimage/<test_id>")
@login_required
def get_test_image(test_id):
    # from timeit import default_timer as timer
    # start = timer()
    # encoded_img = render_test_result_interactive(test_id)
    # end = timer()
    # print(end - start)
    # response = make_response(encoded_img.tobytes())
    # response.headers['Content-Type'] = 'image/png'
    # return response
    return render_template("admin/testresult.html", test_id=test_id)


# Data migration
@app.route("/data_migration")
def data_migration():
    from Documents.patient import PatientIdSeed
    seed = PatientIdSeed.objects.first()
    if not seed:
        seed = PatientIdSeed()
        seed.save()
    return "OK", 200


@app.after_request
def after(response):
    if response.status_code >= 400:
        print(datetime.utcnow())
        print(response.status)
        print(response.headers)
        print(response.get_data())
    return response
