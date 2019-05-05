#!/usr/bin/env python

from flask import Flask, render_template, request, redirect
from flask import jsonify, url_for, flash, g
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Hero, Power, User
from flask import session as login_session
from functools import wraps
import random
import string
import oauth2client
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests


app = Flask(__name__)
CLIENT_ID = json.loads(
    open('client_varun.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog Application"

engine = create_engine('sqlite:///superhero.db',
                       connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

""" To show the heros name
and the new hero button
and delete hero button """
@app.route('/')
@app.route('/heros/')
def show():
    hero = session.query(Hero).all()
    return render_template('hero.html', hero=hero)


""" To show the hero name
and the delete button
and cancel """
@app.route('/heros/<int:hero_id>/<int:power_id>/delete',
           methods=['GET', 'POST'])
def deletePower(hero_id, power_id):
    hero = session.query(Hero).filter_by(id=hero_id).one()
    powToDelete = session.query(Power).filter_by(id=power_id).one()
    if 'username' not in login_session:
        return redirect('/login')

        user_id = login_session['user_id']

    hero = session.query(Hero).filter_by(id=hero_id).one()

    if hero.user_id != login_session['user_id']:
        flash("""Hero was created by another user and can only
                delete power""")
        return redirect(url_for('heroPower', hero_id=hero_id))

    elif request.method == 'POST':
        session.delete(powToDelete)
        session.commit()
        flash('Power Successfully Deleted')
        return redirect(url_for('heroPower',
                                hero_id=hero_id))
    else:
        return render_template('deletepower.html',
                               power=powToDelete, power_id=power_id,
                               hero=hero, hero_id=hero_id)


""" To show the heros powers
and the add power button
and delete power button
and edit power button
and edit hero button"""
@app.route('/heros/<int:hero_id>/heroPower', methods=['GET'])
def heroPower(hero_id):
    power = session.query(Power).filter_by(hero_id=hero_id).all()
    hero = session.query(Hero).filter_by(id=hero_id).one()
    return render_template(
                           'heropower.html',
                           hero_id=hero_id, power=power, hero=hero)


""" To show the form
to add the new power"""
@app.route('/heros/<int:hero_id>/newPower', methods=['GET', 'POST'])
def newPower(hero_id):

    if 'username' not in login_session:
        return redirect('/login')

    user_id = login_session['user_id']

    hero = session.query(Hero).filter_by(id=hero_id).one()

    if hero.user_id != login_session['user_id']:
        flash("""Hero was created by another user and can only
                add powers""")
        return redirect(url_for('heroPower', hero_id=hero_id))

    elif request.method == 'POST':
        power = Power(powers=request.form['powers'], hero_id=hero_id)
        session.add(power)
        session.commit()
        return redirect(url_for('heroPower', hero_id=hero_id))

    else:
        return render_template('newpower.html', hero_id=hero_id)


""" To show the form to
add the new hero """
@app.route('/heros/addHero', methods=['GET', 'POST'])
def newHero():

    if 'username' not in login_session:
        return redirect('/login')

    elif request.method == 'POST':
        hero = Hero(name=request.form['name'])
        session.add(hero)
        session.commit()
        return redirect(url_for('show'))

    else:
        return render_template('newhero.html')


""" To show the power
and the delete button
and cancel """
@app.route('/heros/<int:hero_id>/delete',
           methods=['GET', 'POST'])
def deleteHero(hero_id):
    hero = session.query(Hero).filter_by(id=hero_id).one()
    if 'username' not in login_session:
        return redirect('/login')

        user_id = login_session['user_id']

    hero = session.query(Hero).filter_by(id=hero_id).one()

    if hero.user_id != login_session['user_id']:
        flash("""Hero was created by another user and can only
                be deleted by creator""")
        return redirect(url_for('show'))

    elif request.method == 'POST':
        session.delete(hero)
        session.commit()
        flash('Hero Successfully Deleted')
        return redirect(url_for('show'))
    else:
        return render_template('deletehero.html', hero=hero, hero_id=hero_id)


""" To show the login page """
@app.route('/login')
def showLogin():
    if 'username' not in login_session:
        state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                        for x in range(32))
        login_session['state'] = state
        return render_template('login.html', STATE=state)

    if 'username' in login_session:
        return redirect(url_for('show'))


""" To show the form
to edit the hero
and cancel """
@app.route('/heros/<int:hero_id>/edit', methods=['GET', 'POST'])
def editHero(hero_id):
    editedhero = session.query(Hero).filter_by(id=hero_id).one()
    if 'username' not in login_session:
        return redirect('/login')

    user_id = login_session['user_id']

    hero = session.query(Hero).filter_by(id=hero_id).one()

    if hero.user_id != login_session['user_id']:
        flash("""Hero was created by another user and can only
                be edited by creator""")
        return redirect(url_for('heroPower', hero_id=hero_id))

    elif request.method == 'POST':
        if request.form['name']:
            editedhero.name = request.form['name']
            session.commit()
            return redirect(url_for('show'))
    else:
        return render_template(
            'editHero.html',
            Hero=editedhero, hero_id=hero_id)


""" To show the form
to edit the power
and cancel """
@app.route('/heros/<int:hero_id>/<int:power_id>/edit', methods=['GET', 'POST'])
def editPower(hero_id, power_id):
    hero = session.query(Hero).filter_by(id=hero_id).one()
    powToEdit = session.query(Power).filter_by(id=power_id).one()
    if 'username' not in login_session:
        return redirect('/login')

    user_id = login_session['user_id']

    hero = session.query(Hero).filter_by(id=hero_id).one()

    if hero.user_id != login_session['user_id']:
        flash("""Hero was created by another user and can only
                be edited by creator""")
        return redirect(url_for('heroPower', hero_id=hero_id))

    elif request.method == 'POST':
        powToEdit.powers = request.form['powers']
        session.commit()
        return redirect(url_for('heroPower', hero_id=hero_id))
    else:
        return render_template(
                               'editPower.html', Hero=hero,
                               hero_id=hero_id, powers=powToEdit,
                               power_id=power_id)


"""GOOGLE CONNECT"""
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code, now compatible with Python3
    request.get_data()
    code = request.data.decode('utf-8')

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_varun.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    # Submit request, parse response - Python3 compatible
    h = httplib2.Http()
    response = h.request(url, 'GET')[1]
    str_response = response.decode('utf-8')
    result = json.loads(str_response)

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    print data['email']
    if session.query(User).filter_by(email=data['email']).count() != 0:
        current_user = session.query(User).filter_by(email=data['email']).one()
    else:
        newUser = User(name=data['name'],
                       email=data['email'])
        session.add(newUser)
        session.commit()
        current_user = newUser

    login_session['user_id'] = current_user.id
    print current_user.id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;\
    border-radius: 150px;-webkit-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    return output


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


"""def getUserID(email):
    user = session.query(User).filter_by(email=email).one()
    return user.id"""


"""GOOGLE DISCONNECT"""
@app.route('/disconnect')
def disconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    del login_session['access_token']
    del login_session['gplus_id']
    del login_session['username']
    del login_session['email']
    del login_session['picture']

    response = redirect(url_for('show'))
    flash("You are now logged out.")
    return response


"""JSON to show heros"""
@app.route('/heros/JSON')
def herosJSON():
    hero = session.query(Hero).all()
    return jsonify(hero=[c.serialize for c in hero])


"""JSON to show pwers"""
@app.route('/heros/<int:hero_id>/JSON')
def heroPowerJSON(hero_id):
    hero = session.query(Hero).filter_by(id=hero_id).one()
    powers = session.query(Power).filter_by(hero_id=hero_id).all()
    return jsonify(powers=[c.serialize for c in powers])


"""JSON to show powers of hero"""
@app.route('/heros/<int:hero_id>/<int:power_id>/JSON')
def powerJSON(hero_id, power_id):
    powers = session.query(Power).filter_by(id=power_id).one()
    return jsonify(powers=powers.serialize)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
