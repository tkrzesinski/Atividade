from flask import Flask, request
from flask_restful import Resource, Api
from banco import Arquivos
from background import Limpa_background
from io import BytesIO   #  trabalha com buffer
from PIL import Image    #   recursos para edicao de imagens
import pybase64

import werkzeug, os
from werkzeug.utils import secure_filename  # valida o nome do arquivo para nao executar um bash

dir_path = os.path.dirname(os.path.realpath(__file__)) + '/'

app = Flask(__name__)

api = Api(app)
UPLOAD_FOLDER = dir_path + 'dataset/ruido_base64/'  # nao esta sendo usado pois grava no temp

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_EXTENSIONS'] = ['.png','.txt']
ALLOWED_EXTENSIONS = set(['png','txt'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_image(stream):
    header = stream.read(512)  # 512 bytes should be enough for a header check
    stream.seek(0)  # reset stream pointer
    format = imghdr.what(None, header)
    if not format:
        return None

class UploadFile(Resource):
    decorators = []

    def post(self):
        # verifica se foi informado um arquivo
        if 'file' not in request.files:
            response = {'mensagem': 'Nenhum arquivo informado'}
            return response
        file = request.files['file']
        if file.filename == '':
            response = {'mensagem': 'Nao ha arquivo para upload'}
            return response
        if file and allowed_file(file.filename):  # file_ext = os.path.splitext(filename)[1]
                                                  # if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
                                                  #                 file_ext != validate_image(uploaded_file.stream)
            filename = secure_filename(file.filename)
            prefixo = os.path.splitext(filename)[0]

            arquivo = Limpa_background(dir_path, prefixo)

            arquivo.save()

            response = {'mensagem': 'Arquivo carregado com sucesso'}
            return response
        else:
            response = {'mensagem': 'Somente permitido as extensoes txt, png'}
            return response

class Consulta(Resource):
    def post(self, nome):
        arquivo = Arquivos.query.filter_by(nome=nome).first()
        try:
            im_bytes = pybase64.b64decode(arquivo.img_limpa)
            im_file = BytesIO(im_bytes)
            img = Image.open(im_file)
            img.show()

        except AttributeError:
            response = {
              'status': 'erro',
              'mensagem': 'Arquivo nao encontrado'
                       }
            return response

class ListaArquivos(Resource):
    def get(self):
        arquivos = Arquivos.query.all()
        response = [{'nome': i.nome, 'caminho': i.caminho} for i in arquivos]
        return response

api.add_resource(UploadFile, '/upload/')
api.add_resource(ListaArquivos, '/lista/')
api.add_resource(Consulta, '/consulta/<string:nome>')

if __name__ == '__main__':
    app.run(debug=True)