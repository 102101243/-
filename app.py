from flask import Flask, request,jsonify
from flask_cors import CORS
from math import *
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:\\PycharmProjects\\flaskProject1\\calData.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class calData(db.Model):
    __tablename__ = 'calData'
    id = db.Column(db.Integer, primary_key=True)
    equation = db.Column(db.String(120), unique=False)
    result = db.Column(db.Float, unique=False)
app.app_context().push()


class depositRate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    current = db.Column(db.String(120), unique=False)
    rate = db.Column(db.String(10), unique=False)

class loanRate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timeLimit = db.Column(db.String(120), unique=False)
    rate = db.Column(db.String(10), unique=False)

db.create_all()

@app.route('/data', methods=['POST'])
def get_data():
    # Retrieve data from the server
    json_data = request.json
    print(json_data)
    try:
        result = eval(json_data['data'])
    except:
        result = 'Error'
    print(result)
    if result != 'Error':
        len_data = calData.query.count()
        if len_data == 10:
            calData.query.filter(calData.id == 1).delete()
        cal = calData(equation=json_data['data'], result=result)
        db.session.add(cal)
        db.session.commit()
    data = {'result': result}

    #return jsonify({'message': 'Data received successfully'})
    return jsonify(data)

@app.route('/ans', methods=['GET'])
def get_ans():
    lne = calData.query.count()
    rd = calData.query.filter(calData.id == lne)
    ans = rd.result()
    return jsonify({'ans': ans})


@app.route('/hisData', methods=['GET'])
def get_HisData():
    # 获取历史记录
    ghd = calData.query.all()

    list_data = []
    for i in ghd:
        dic_data = {}
        dic_data['equation'] = i.equation
        dic_data['result'] = i.result
        list_data.append(dic_data)

    data = {'total': len(ghd), 'datas':list_data}
    print(data)
    return jsonify(data)

@app.route('/delete', methods=['GET'])
def data_delData():
    calData.query.filter(calData.id >= 1).delete()
    db.session.commit()
    return jsonify({'data': 'Delete over!'})

@app.route('/current', methods=['GET'])
def getDeposit():
    # 获取历史记录
    ghd = depositRate.query.all()

    list_data = []
    for i in ghd:
        dic_data = {}
        dic_data['current'] = i.current
        dic_data['rate'] = i.rate
        list_data.append(dic_data)

    data = {'total': len(ghd), 'datas':list_data}
    print(data)
    return jsonify(data)

@app.route('/loan', methods=['GET'])
def getLone():
    # 获取历史记录
    ghd = loanRate.query.all()

    list_data = []
    for i in ghd:
        dic_data = {}
        dic_data['timeLimit'] = i.timeLimit
        dic_data['rate'] = i.rate
        list_data.append(dic_data)

    data = {'total': len(ghd), 'datas':list_data}
    print(data)
    return jsonify(data)

@app.route('/intloan', methods=['POST'])
def getintloan():
    # 获取历史记录

    money_years = request.json
    money = float(money_years['money'])
    years = float(money_years['years'])

    if years == 0.5:
        lr = loanRate.query.get(1)
    elif years == 1:
        lr = loanRate.query.get(2)
    elif years > 1 and years <=3:
        lr = loanRate.query.get(3)
    elif years > 3 and years <5:
        lr = loanRate.query.get(4)
    else:
        lr = loanRate.query.get(5)
    rate = float(lr.rate)

    interest = rate*money*years/100

    return jsonify({'interest': interest})


@app.route('/intcurrent', methods=['POST'])
def getintcurrent():
    # 获取历史记录
    money_years = request.json
    money = float(money_years['money'])
    years = float(money_years['years'])

    if years == 0.5:
        lr = loanRate.query.get(1)
    elif years == 1:
        lr = loanRate.query.get(2)
    elif years > 1 and years <= 3:
        lr = loanRate.query.get(3)
    elif years > 3 and years < 5:
        lr = loanRate.query.get(4)
    else:
        lr = loanRate.query.get(5)
    rate = float(lr.rate)
    interest = rate * money * years/100
    return jsonify({'interest': interest})



if __name__ == '__main__':
    app.run(debug=True)
