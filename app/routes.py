#coding: utf-8
from flask import jsonify, request, redirect, url_for, send_from_directory
from app import app
from app.common import common
from app.models import Photos
import time, os, random, datetime
from werkzeug import secure_filename
from PIL import Image


class Api():
    @app.route('/upload', methods=['POST'])
    def upload():
        if request.method == 'POST':
            photo = request.files.get('photo')
            if not (photo):
                return jsonify(common.falseReturn('', '填写完整信息'))
            else:
                # encode解决中文问题
                filename = photo.filename.encode('utf8')
                path = os.path.join(app.root_path + app.config['UPLOAD_FOLDER'], filename.decode('utf8'))
                # D:\xampp\htdocs\python\flask-file-uploads\app\img\22.png
                # 保存图片
                photo.save(path)
                # 解构文件名，取得文件名和扩展名
                file_name, file_ext = os.path.splitext(filename)
                file_ext = file_ext.decode('utf8')

                # 判断今天日期的文件夹是否存在，如果不存在就创建
                dateDir = datetime.datetime.now().strftime('%Y%m%d')
                sub_img_directory = os.path.join(app.root_path + app.config['UPLOAD_FOLDER'], dateDir)
                if not os.path.exists(sub_img_directory):
                    os.makedirs(sub_img_directory)

                # 取得当前的时间戳并生成一个随机字符串，拼接生成新的文件名
                timestamp = int(time.time())
                random_str = "".join(random.sample(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', '8i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'], 6)).replace(" ", "")
                new_filename = random_str + '_' + str(timestamp)

                # 得到新的文件路径
                new_path = os.path.join(sub_img_directory, new_filename + file_ext)

                # 重命名文件
                os.rename(path, new_path)

                # 返回图片路径
                base = 'http://' + app.config['HOST'] + ':' + str(app.config['PORT']) + ''

                try:
                    # 生成并保存缩略图
                    im = Image.open(new_path)
                    size = (60, 60)
                    thumbnail_filename = new_filename + '_thumb'
                    thumbnailPath = os.path.join(sub_img_directory, thumbnail_filename + file_ext)
                    im.thumbnail(size)
                    im.save(thumbnailPath, 'JPEG')

                    photo = Photos(photo_name=new_filename,
                                   photo_source=base + url_for('img', dir=dateDir, filename=new_filename + file_ext),
                                   photo_thumb=base + url_for('img', dir=dateDir,
                                                              filename=thumbnail_filename + file_ext))
                    addRst = Photos.add(Photos, photo)

                    if photo.id:
                        photoInfo = {
                            'id': photo.id,
                            'photo_name': photo.photo_name,
                            'photo_source': photo.photo_source,
                            'photo_thumb': photo.photo_thumb
                        }
                        return jsonify(common.trueReturn(photoInfo, "图片保存成功"))
                    else:
                        return jsonify(common.falseReturn('', '图片保存失败'))
                except:
                    # 上传失败判断是否存在刚刚上传的图片，有就删除
                    if (os.path.exists(new_path)):
                        os.remove(new_path)
                    if (os.path.exists(thumbnailPath)):
                        os.remove(thumbnailPath)
                    return jsonify(common.falseReturn('', '无法生成图片缩略图，保存失败.'))

        else:
            return jsonify(common.falseReturn('', '非法请求'))


    @app.route('/img/<dir>/<filename>')
    def img(dir, filename):
        return send_from_directory(os.path.join('img', dir), filename)


