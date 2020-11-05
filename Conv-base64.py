import os
import pybase64
directory = os.listdir('/home/claudio/Atividade/Projeto/dataset/ruido/')
dir_path = '/home/claudio/Atividade/Projeto/dataset/ruido/'
dir_out = '/home/claudio/Atividade/Projeto/dataset/base64/'
for file in directory:
    nome_arquivo = os.path.splitext(file)[0]

    image = dir_path + file
    print(file, nome_arquivo, image)
    read_file = open(image, 'rb')
    data = read_file.read()

    b64 = pybase64.b64encode(data)

    path_saida = dir_out + nome_arquivo + '.txt'
    out_file = open(path_saida, 'wb')
    out_file.write(b64)

    # Save file
    #decode_b64 = base64.b64decode(b64)
    #out_file = open('/tmp/out_newgalax.png', 'wb')
    #out_file.write(decode_b64)