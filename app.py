from flask import Flask, render_template, jsonify, request
app = Flask(__name__)


from bson.objectid import ObjectId
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbjungle

## HTML을 주는 부분
@app.route('/')
def home():
   return render_template('index.html')


@app.route('/memos', methods=['POST'])
def post_memos():
    # 1. 클라이언트로부터 데이터를 받기
    title_receive = request.form['title_give']  # 클라이언트로부터 url을 받는 부분
    desc_receive = request.form['content_give']  # 클라이언트로부터 comment를 받는 부분

    memos = {'title': title_receive, 'content': desc_receive, 'likes':0 }
    # 2. mongoDB에 데이터를 넣기
    inserted = db.memos.insert_one(memos)
    return jsonify({
        'result': 'success',
        'memo' : {
              '_id': str(inserted.inserted_id),
              'title': title_receive,
              'content': desc_receive,
              'likes': 0

            }
        })

@app.route('/memos', methods=['GET'])
def read_memos():
    # 1. 모든 document 찾기 & _id 값은 출력에서 제외하기
    result = list(db.memos.find({}))
    for memo in result : 
        memo['_id'] = str(memo['_id']);

    return jsonify({'result': 'success', 'memos': result})

@app.route('/memos/update', methods=['POST'] )
def update_memo():
    id_receive = request.form['id_give']
    title_receive = request.form['title_give']
    desc_receive = request.form['content_give']

    db.memos.update_one(
        {'_id': ObjectId(id_receive)},
        {'$set': {
            'title': title_receive,
            'content': desc_receive
        }}
    )
    return jsonify({'result': 'success'})

@app.route('/memos/delete', methods=['POST'])
def delete_memo():
    id_receive = request.form['id_give']
    db.memos.delete_one({'_id': ObjectId(id_receive)})
    return jsonify({'result': 'success'})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5050,debug=True)