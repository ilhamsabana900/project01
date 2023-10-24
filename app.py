from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime

connection_string = 'mongodb+srv://ilham123:ilham123@cluster0.z5oy8if.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(connection_string)
db = client.dbsparta
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/diary', methods=['GET'])
def show_diary():
    articles = list(db.diary.find({},{'_id':False}))
    return jsonify({'articles':articles})

@app.route('/diary', methods=['POST'])
def save_diary():
    title_receive = request.form.get('title_give')
    content_receive = request.form.get('content_give')

    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')


    file = request.files['file_give']
    extension = file.filename.split('.')[-1]
    save_to = f'static/post-{mytime}.{extension}'
    file.save(save_to)

    profile = request.files['profile_give']
    extension = profile.filename.split('.')[-1]
    profile_filename = f'static/profile-{mytime}.{extension}'
    profile.save(profile_filename)

    time = today.strftime('%Y-%m-%d')

    doc = {
        'file' : save_to,
        'profile' : profile_filename,
        'title' : title_receive,
        'content': content_receive,
        'time' : time
    }
    db.diary.insert_one(doc)

    return jsonify({'message':'selamat data berhasil dipost'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)