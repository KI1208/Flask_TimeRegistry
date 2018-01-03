# 概要
Flaskを使用して、自分の仕事内容を記録するアプリケーションを作成する。 

# 想定の環境
メイン環境: Windows10(Python: 3.6.4)
MongoDB用コンテナ環境: DockerToolbox(17.10.0-ce)


# 前提条件
1. MongoDBを別途用意する。  
Docker Toolboxにて、以下のように準備をすれば、そのまま使用できる。  
databaseやcollectionをあらかじめ作成する必要はない。  

```
$ docker pull mongo:3.6.1-jessie
$ docker run --name my-mongo -d -p 27017:27017 mongo:3.6.1-jessie
```

異なるものを使う場合は、testapp.py内の以下を調整する。

```python
app = Flask(__name__)
app.secret_key = 'secret'
app.config['MONGO_HOST'] = '192.168.99.100' # DockerToolboxのホストのIPアドレスになっている
app.config['MONGO_PORT'] = 27017
app.config['MONGO_DBNAME'] = 'testdb' # データベース名は任意(なければ作成される)
mongo = PyMongo(app, config_prefix='MONGO')
```

# 使い方

1. git clone <URL>
2. pip install -r requirements.txt
2. python timerecord.py
3. ブラウザでhttp://localhost:5000にアクセス

