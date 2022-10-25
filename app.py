from flask import Flask, render_template, jsonify, request, make_response
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.krafton09


# HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login')
def login_page():
    return render_template('login.html')


@app.route('/signup')
def signup_page():
    return render_template('signup.html')


@app.route('/api/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email_receive = request.form['email_give']
        pw_receive = request.form['pw_give']
        signin_user = db.users.find_one({'email': email_receive})

        if signin_user:
            if (signin_user['pw'] == pw_receive):
                resp = make_response({'result': 'success'})
                resp.set_cookie('user_email', email_receive)
                resp.set_cookie('user_name', signin_user['name'])
                return resp
            else:
                return jsonify({'result': 'fail'})
        else:
            return jsonify({'result': 'fail'})
    else:
        return jsonify({'result': 'fail'})


@app.route('/mypage')
def mypage_page():
    table_infos = [
        {"idx": 1, "title": "Jinja제목1", "name": "Jinja이름1", "post-date": "22-10-14", "join-num": 3},
        {"idx": 2, "title": "Jinja제목2", "name": "Jinja이름2", "post-date": "22-10-11", "join-num": 5}
    ]
    return render_template('mypage.html', name1="형기", tableInfoList=table_infos)


# API 역할을 하는 부분
@app.route('/api/signUp', methods=['POST'])
def signup_post():
    email_receive = request.form['email_give']
    pw_receive = request.form['pw_give']
    name_receive = request.form['name_give']

    user = {'email': email_receive, 'pw': pw_receive, 'name': name_receive}

    # 3. mongoDB에 데이터를 넣기
    db.users.insert_one(user)

    return jsonify({'result': 'success', 'comment': "회원가입이 완료되었습니다."})


@app.route('/api/addData', methods=['GET'])
def add_data():
    tempdata = {
        "idx": 1,
        "writer_email": "aaa@naver.com",
        "writer_name": "길동",
        "title": "제목",
        "description": "내용",
        "participants": [("bbb@naver.com", "동길")],
        "reg_time": "22-10-15",
        "status": "모집중"
    }

    # 3. mongoDB에 데이터를 넣기
    db.posts.insert_one(tempdata)

    return jsonify({'result': 'success', 'comment': "data 추가가 완료되었습니다."})


@app.route('/api/closePurchase', methods=['POST'])
def closepurchase_post():
    # request.cookies.get("")
    account_receive = request.form['account_give']
    idx_receive = int(request.form['idx_give'])

    finded_post = db.posts.find_one({'idx': idx_receive}, {'_id': False})
    if finded_post is None:
        return jsonify({'result': 'error', 'comment': "해당하는 idx post가 없습니다."})

    account_email = account_receive.split("/")[0]
    account_name = account_receive.split("/")[1]

    if finded_post["writer_email"] != account_email or finded_post["writer_name"] != account_name:
        return jsonify({'result': 'error', 'comment': "잘못된 사용자의 요청입니다."})

    # 3. mongoDB에 데이터를 넣기
    db.posts.update_one({'idx': idx_receive}, {'$set': {'status': "마감"}})

    return jsonify({'result': 'success', 'comment': "정상적으로 처리되었습니다."})


@app.route('/api/joinPurchase', methods=['POST'])
def joinpurchase_post():
    account_receive = request.form['account_give']
    idx_receive = int(request.form['idx_give'])

    finded_post = db.posts.find_one({'idx': idx_receive}, {'_id': False})
    if finded_post is None:
        return jsonify({'result': 'error', 'comment': "해당하는 idx post가 없습니다."})

    my_list = finded_post["participants"]
    account_email = account_receive.split("/")[0]
    account_name = account_receive.split("/")[1]
    account_list = [account_email, account_name]
    my_list.append(account_list)

    # 3. mongoDB에 데이터를 넣기
    db.posts.update_one({'idx': idx_receive}, {'$set': {'participants': my_list}})

    return jsonify({'result': 'success', 'comment': "정상적으로 처리되었습니다."})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
