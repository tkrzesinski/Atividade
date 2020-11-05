import numpy as np
from scipy import signal
from PIL import Image
import pybase64
from banco import Arquivos

def load_image(path):
    return np.asarray(Image.open(path))/255.0

def save(path, img):
    tmp = np.asarray(img*255.0, dtype=np.uint8)
    Image.fromarray(tmp).save(path)

def denoise_image(inp):
    # estimate 'background' color by a median filter
    bg = signal.medfilt2d(inp, 11)
    save('background.png', bg)

    # compute 'foreground' mask as anything that is significantly darker than
    # the background
    mask = inp < bg - 0.1
    save('foreground_mask.png', mask)

    # return the input value for all pixels in the mask or pure white otherwise
    return np.where(mask, inp, 1.0)

def Limpa_background(path, prefixo):
    # Carrega arquivo em base64
    image = path + "/dataset/ruido_base64/" + prefixo + ".txt"
    read_file = open(image, 'rb')
    data = read_file.read()

    # decodifica arquivo para imagem
    decode_b64 = pybase64.b64decode(data)

    
    # grava imagem
    path_saida = path  + 'temp.png'
    out_file = open(path_saida, 'wb')
    out_file.write(decode_b64)
    image=Image.open(path_saida)
    image.show()
    
    ## carrega imagem
    inp = load_image(path_saida)

    # limpa imagem
    out = denoise_image(inp)

    # salva imagem decodificada
    arq_limpa_decode = path + '/dataset/limpa_decode/' + prefixo  + '.png'
    save(arq_limpa_decode, out)
    #out_file = open(arq_limpa_decode, 'wb')
    #out_file.write(out)
    #out_file.close

    # codifica imagem
    read_file = open(arq_limpa_decode, 'rb')
    data_limpa = read_file.read()
    encode_b64 = pybase64.b64encode(data_limpa)

    # grava imagem em base64 e tambem a decodificada
    arq_limpa_base64 = path + '/dataset/limpa_base64/' + prefixo  + '.txt'
    #save(arq_limpa_base64, encode_b64)
    out_file = open(arq_limpa_base64, 'wb')
    out_file.write(encode_b64)
    out_file.close

    # adiciona no banco
    arquivo = Arquivos(nome= prefixo , caminho= path, img_origem =  data, img_limpa = encode_b64)
    return arquivo