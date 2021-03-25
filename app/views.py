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
        salt = '$2b$09$cVWp4XaNU8a4v1uMRum2SO'.encode()
        count = 0
        patient_list = list(Patient.objects())
        for old_id_str in data:
            for i in range(len(patient_list) - 1, -1, -1):
                patient = patient_list[i]
                if len(patient.patient_id) <= 32:
                    continue
                if bcrypt.checkpw(old_id_str.encode(), patient.patient_id.encode()):
                    new_hash_bytes = bcrypt.hashpw(old_id_str.encode(), salt)
                    new_hash = new_hash_bytes.decode('utf-8')
                    inner_count = 0
                    print("{}, {}".format(old_id_str, new_hash))
                    count += 1
                    for testdata in Testdata.objects(patient_id=patient.patient_id):
                        testdata.patient_id = new_hash
                        testdata.test['patient_info']['patient_id'] = new_hash
                        testdata.save()
                        inner_count += 1
                    # if inner_count:
                    #     print("{} testdata updated".format(inner_count))
                    new_patient = Patient()
                    for field in Patient._fields:
                        new_patient[field] = patient[field]
                    new_patient.patient_id = new_hash
                    new_patient.visit = patient.visit if patient.visit else 'baseline'
                    try:
                        new_patient.save(force_insert=True)
                    except NotUniqueError:
                        print("Failure Case!")
                    patient.delete()
                    patient_list.remove(patient)
                    break
        print("{} out of {} old hashes reverted".format(count, len(data)))

    return "OK", 200


@app.after_request
def after(response):
    if response.status_code >= 400:
        print(datetime.utcnow())
        print(response.status)
        print(response.headers)
        print(response.get_data())
    return response
