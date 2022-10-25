from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.krafton09


# HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/signup')
def signup_page():
    return render_template('signup.html')


# API 역할을 하는 부분
@app.route('/api/signup', methods=['POST'])
def signup_post():
    email_receive = request.form['email_give']
    pw_receive = request.form['pw_give']
    name_receive = request.form['name_give']

    user = {'email': email_receive, 'pw': pw_receive, 'name': name_receive}

    # 3. mongoDB에 데이터를 넣기
    db.users.insert_one(user)

    return jsonify({'result': 'success', 'comment': "회원가입이 완료되었습니다."})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
