from flask import Flask,url_for,render_template,redirect,request,g
import sqlite3
app=Flask(__name__)


@app.before_request
def before_request():
    # print('before_request()')
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    # print('teardown_request(exception)')
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login/',methods=['GET','POST'])
def user_login():
    users = query_users_from_db()
    for user in users:
        print(user.name,user.email)
    return render_template('user_login.html')


@app.route('/regist/',methods=['GET','POST'])
def user_regist():
    if request.method == 'POST':

        user=User()
        user.name=request.form.get('user_name')
        user.pwd = request.form.get('user_pwd')
        user.email = request.form.get('user_email')
        user.age = request.form.get('user_age')
        user.birthday = request.form.get('user_birthday')
        user.face = request.form.get('user_face')
        print(user.email)
        insert_user_to_db(user)

        return redirect(url_for('user_login',username=user.name))
    return render_template('user_regist.html')

if __name__ == '__main__':
    app.run()
