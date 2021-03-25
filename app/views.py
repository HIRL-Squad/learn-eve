import json
from datetime import datetime

from flask import render_template, request, redirect, make_response
from flask_babelex import lazy_gettext
from flask_login import login_required, login_user, logout_user
from mongoengine import NotUniqueError

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
    return render_template("admin/testresult.html", test_id=test_id)


@app.route("/label/<test_id>")
@login_required
def get_manual_label_page(test_id):
    return render_template("admin/testresult.html", test_id=test_id)


# Data migration
@app.route("/data_migration")
def data_migration():
    from Documents.patient import Patient
    import bcrypt
    with open('data.txt') as json_file:
        data = json.load(json_file)
        count = 0
        testdata_delete = []
        patient_list = list(Patient.objects())
        ids_to_keep = []
        ids_to_keep_original = []
        for old_id_str in data:
            for i in range(len(patient_list) - 1, -1, -1):
                patient = patient_list[i]
                if len(patient.patient_id) <= 32:
                    continue
                if bcrypt.checkpw(old_id_str.encode(), patient.patient_id.encode()):
                    print("{}, {}".format(old_id_str, patient.patient_id))
                    count += 1
                    for testdata in Testdata.objects(patient_id=patient.patient_id):
                        testdata_delete.append(testdata)
                    patient_list.remove(patient)
                    ids_to_keep.append(patient.patient_id)
                    ids_to_keep_original.append(old_id_str)
                    break
        print("{} out of {} IDs found".format(count, len(data)))
        print(set(data) - set(ids_to_keep_original))

    return "OK", 200


@app.after_request
def after(response):
    if response.status_code >= 400:
        print(datetime.utcnow())
        print(response.status)
        print(response.headers)
        print(response.get_data())
    return response
