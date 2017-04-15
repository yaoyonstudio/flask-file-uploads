from flask import jsonify, request, redirect, url_for, send_from_directory
from app import app
from app.common import common
from app.models import Photos
import time, os, random
from werkzeug import secure_filename


class Api():
    @app.route('/test')
    def test():
        return jsonify(common.trueReturn('aa', "提示"))


    @app.route('/upload', methods=['POST'])
    def upload():
        if request.method == 'POST':
            photo = request.files.get('photo')
            if not (photo):
                result = common.falseReturn('', '填写完整信息')
                return jsonify(result)
            else:
                filename = secure_filename(photo.filename)
                path = os.path.join(app.root_path + app.config['UPLOAD_FOLDER'], filename)
                # D:\xampp\htdocs\python\flask-file-uploads\app\img\22.png
                photo.save(path)

                print(path)

                timestamp = int(time.time())
                random_str = "".join(random.sample(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'], 6)).replace(" ", "")
        
                os.rename(path, 'aa')

                # filenameArr = path.split(".")
                # file_ext = filenameArr[1]
                # dest_path = filenameArr[0] + random_str + '_' + str(timestamp) + '.' + file_ext
                # dest_filename = filename + random_str + '_' + str(timestamp) + '.' + file_ext
                # os.rename(path, dest_filename)

                # print(dest_filename)

                base = 'http://' + app.config['HOST'] + ':' + str(app.config['PORT']) + ''
                result = common.trueReturn(base + url_for('img', filename=filename), '上传成功')
        else:
            result = common.falseReturn('', '非法请求')
        
        return jsonify(result)
                    


    @app.route('/img/<filename>')
    def img(filename):
        return send_from_directory('img', filename)


