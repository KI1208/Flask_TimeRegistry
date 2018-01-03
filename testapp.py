from flask import Flask, current_app, request, flash,redirect,url_for,render_template
from flask_pymongo import PyMongo
from datetime import datetime, date, timedelta,timezone
from dateutil.parser import parse
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = 'secret'
app.config['MONGO_HOST'] = '192.168.99.100'
app.config['MONGO_PORT'] = 27017
app.config['MONGO_DBNAME'] = 'testdb'
mongo = PyMongo(app, config_prefix='MONGO')


@app.route('/', methods=['GET'])
def show_entry():
    # print(request.args.get('date'))  # For Debug
    if request.args.get('date') is not None :
        requesteddate = parse(request.args.get('date')).replace(tzinfo=timezone(timedelta(hours=+0)))
        # print(type(requesteddate), requesteddate, "A")  # For Debug
    else:
        requesteddate = datetime.utcnow()
        # print(type(requesteddate), requesteddate, "B")  # For Debug

    start = datetime(requesteddate.year, requesteddate.month, requesteddate.day, 0, 0, 0)
    end = start + timedelta(days=1)
    cur = mongo.db.work.find({'time': {'$lt': end, '$gte': start}})
    templist1 = []
    templist2 = []
    for row in cur:
        templist1.append(row['time'])
        templist2.append(row)

    # 以下のtry/exceptのやりかたは改善の余地あり
    dt = datetime(requesteddate.year, requesteddate.month, requesteddate.day, 0, 0, 0, tzinfo=timezone(timedelta(hours=+0)))
    output = []
    for i in range(30):
        try:
            index = templist1.index(dt)
            # print('A', index, dt) # ForDebug
            # print(templist2[index]) # For Debug
            # output.append(templist2[index])
        except:
            # print('B') # For Debug
            mongo.db.work.insert({"time": dt, "worktype": '', "comment": ''})
            # output.append({'time': dt, "worktype": None, "comment": None})

        dt = dt + timedelta(minutes=30)

    cur = mongo.db.work.find({'time': {'$lt': end, '$gte': start}}).sort('time',1)
    for row in cur:
        output.append({"_id": row['_id'], "time": row['time'] + timedelta(hours=+9), "worktype": row['worktype'], "comment": row['comment']})

    return render_template('toppage.html', entries=output, date=requesteddate)


@app.route('/changedate', methods=['POST'])
def change_date():
    date = parse(request.form['date']) # from str to datetime
    # print(type(date),date)  # For Debug

    return redirect(url_for('show_entry', date=date))


@app.route('/updatedata', methods=['POST','GET'])
def update_data():
    worktype = request.values.getlist('worktype[]')
    id = request.values.getlist('_id[]')
    comment = request.values.getlist('comment[]')

    requesteddate = mongo.db.work.find_one({'_id': ObjectId(id[0])})['time']

    for x,item in enumerate(worktype):
        if item is not '' or comment[x] is not '':
            mongo.db.work.update({"_id": ObjectId(id[x])}, {'$set': {"worktype": worktype[x], "comment": comment[x]}})

    return redirect(url_for('show_entry',date=requesteddate))


if __name__ == '__main__':
    app.run(host='0.0.0.0')

