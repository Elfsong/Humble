import os

from flask import Flask, request
from flask_restplus import Api, Resource
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './image'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
api = Api(app,
          version='0.1',
          title='Humble',
          description='Postera Crescam Laude')
parser = api.parser()
parser.add_argument('file', type=FileStorage, location='files', required=True)


@api.route('/upload_image')
class ImagePredicate(Resource):
    @api.response(200, "Success to get the image.")
    @api.response(404, "The upload image may be invalid!")
    @api.doc(params={'file': 'the upload image'})
    @api.expect(parser, validate=True)
    def post(self):
        image_name = request.files['file']

        if image_name:
            return self.process_image(image_name), 200
        else:
            return "Invalid image!", 404

    def process_image(self, image_file):
        if image_file:
            filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return "Success!"
        else:
            return "Invalid image!"


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=80)
