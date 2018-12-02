from flask import Flask, render_template, request, redirect, jsonify
from io import BytesIO, open
from qiniu import Auth, put_data
import time

app = Flask(__name__)

# this is qiniu ak
access_key = 'KvfHxiYHsC6FWJFMNbmhYv9R5DOy1TvWgT2u4Np1'
# tiis is qiniu sk
secret_key = 'q_ABwrQBBqiE83y6nJuMSrqQKzoZrWD85rY_sypC'

bucket_name = 'test-demo'


@app.route("/uptoken")
def tocken():
    """js 需要的tocken"""
    q = Auth(access_key,secret_key)

    token = q.upload_token(bucket_name)

    return jsonify({'uptoken':token})



@app.route("/j")
def j_index():
    return render_template("jsfileupload2qiniu.html")


@app.route("/f")
def f_index():
    return render_template("flaskfileupload2qiniu.html")


@app.route("/upload", methods=["GET", "POST"])
def upload():
    file = request.files["file"]
    file_type = file.filename.split(".")[1]
    print(file_type)
    # file 对象save到io流中
    buffer = BytesIO()
    file.save(buffer)
    buffer.seek(0)
    print(buffer.read())
    q = Auth(access_key, secret_key)
    new_filename = str(int(time.time())) + "." + file_type
    token = q.upload_token(bucket_name)
    ret, info = put_data(token, new_filename, buffer.read())
    print(ret)
    print(info.status_code)
    return redirect(request.referrer)


if __name__ == "__main__":
    app.run(debug=True)
