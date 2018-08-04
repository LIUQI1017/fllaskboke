from flask import Flask, url_for, render_template, redirect, request, g, flash, get_flashed_messages, session,make_response
import sqlite3, os
from model import User

app = Flask(__name__)
app.config['DATABASE'] = 'database.db'
app.config['SECRET_KEY'] = os.urandom(24)


def connect_db():
    """Connects to the specific database."""
    db = sqlite3.connect(app.config['DATABASE'])
    return db


def init_db():
    with app.app_context():
        db = connect_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def insert_user_to_db(user):
    # sql_insert = 'INSERT INTO users (name, pwd, email, age, birthday, face) VALUES (?, ?, ?, ?, ?, ?)'
    user_attrs = user.getAttrs()
    values = " VALUES ("
    last_attr = user_attrs[-1]
    for attr in user_attrs:
        if attr != last_attr:
            values = values + ' ?,'
        else:
            values = values + ' ?'
    values += " )"
    sql_insert = "INSERT INTO users" + str(user_attrs) + values
    print(sql_insert)

    args = user.toList()
    g.db.execute(sql_insert, args)
    g.db.commit()


def query_users_from_db():
    users = []
    sql_select = 'SELECT * FROM users'
    args = []
    cur = g.db.execute(sql_select, args)
    for item in cur.fetchall():
        user = User()
        user.fromList(item[1:])
        # user.name = item[1]
        # user.pwd = item[2]
        # user.email = item[3]
        # user.age = item[4]
        # user.birthday = item[5]
        # user.face = item[6]
        users.append(user)
        # print(user.name, user.email, user.age)
    return users


def query_user_by_name(user_name):
    sql_select = 'SELECT * FROM users where name=?'
    args = [user_name]
    cur = g.db.execute(sql_select, args)
    items = cur.fetchall()
    if len(items) < 1:
        return None
    first_item = items[0]
    user = User()
    user.fromList(first_item[1:])
    # user.name = first_item[1]
    # user.pwd = first_item[2]
    # user.email = first_item[3]
    # user.age = first_item[4]
    # user.birthday = first_item[5]
    # user.face = first_item[6]
    return user


def delete_user_by_name(user_name):
    delete_sql = 'DELETE FROM users WHERE name=?'
    args = [user_name]
    g.db.execute(delete_sql, args)
    g.db.commit()


def update_user_by_name(old_name, user):
    update_str = ""
    user_attrs = user.getAttrs()
    last_attr = user_attrs[-1]
    for attr in user_attrs:
        if attr != last_attr:
            update_str += attr + "= ?,"
        else:
            update_str += attr + "= ?"
    sql_update = 'UPDATE users SET ' + update_str + ' WHERE name = ?'
    args = user.toList()
    args.append(old_name)
    print(sql_update)
    print(args)
    print('------------------->')
    g.db.execute(sql_update, args)
    g.db.commit()


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
    users = query_users_from_db()
    for user in users:
        print(user.toList())
    #
    # print('=================================>')
    # print(session)
    resp = make_response(render_template('index.html'))
    resp.set_cookie('四大名著', '西游记')
    return resp


@app.route('/login/', methods=['GET', 'POST'])
def user_login():
    # users = query_users_from_db()
    # for user in users:
    #     print(user.toList())
    # print('=================================================>')
    # user = query_user_by_name('刘奇')
    # if user:
    #     print(user.toList())
    # else:
    #     print('查无此人')
    # user = delete_user_by_name('刘昕荷')
    #
    # print('=======================================================================================>')
    # user = query_user_by_name('刘奇')
    # print(user.toList())
    # print('=============>')
    # print('修改张三丰的信息')
    # user = query_user_by_name('张三丰')
    #
    # user.pwd=123456
    # user.age=12
    # user.name='刘昕荷'
    # update_user_by_name('张三丰',user)
    # user=query_user_by_name(user.name)
    # if user:
    #     print(user.toList())
    if request.method == 'POST':
        username = request.form['user_name']
        userpwd = request.form['user_pwd']
        user_x = query_user_by_name(username)
        if not user_x:
            flash('用户名不存在！', category='err')
            return render_template('user_login.html')
        else:

            if str(user_x.pwd) != str(userpwd):
                flash('密码错误，请重新输入！', category='err')
                return render_template('user_login.html')
            else:
                session['user_name'] = user_x.name
                return render_template('index.html')
    return render_template('user_login.html')
    return render_template('user_login.html')

@app.route('/logout')
def user_logout():
    # remove the username from the session if it's there
    session.pop('user_name', None)
    return redirect(url_for('index'))


@app.route('/regist/', methods=['GET', 'POST'])
def user_regist():
    if request.method == 'POST':
        user = User()
        user.name = request.form.get('user_name')
        user.pwd = request.form.get('user_pwd')
        user.email = request.form.get('user_email')
        user.age = request.form.get('user_age')
        user.birthday = request.form.get('user_birthday')
        user.face = request.form.get('user_face')
        user_x = query_user_by_name(user.name)
        if user_x:
            flash('用户名已经存在，请更换用户名注册', category='err')

            return render_template('user_regist.html')

        insert_user_to_db(user)
        flash('恭喜您注册成功', category='ok')
        return redirect(url_for('user_login', username=user.name))
    return render_template('user_regist.html')

@app.errorhandler(404)
def page_not_found(error):
    resp = make_response(render_template('page_not_found.html'), 404)
    # resp.headers['X-Something'] = 'A value'
    return resp

if __name__ == '__main__':
    app.run()

