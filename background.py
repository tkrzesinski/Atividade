import numpy as np
from scipy import signal
from PIL import Image
import pybase64
from banco import Arquivos

def load_image(path):
    return np.asarray(Image.open(path)) /255.0

def save(path, img):
    tmp = np.asarray(img*255.0, dtype=np.uint8)
    Image.fromarray(tmp).save(path)

def denoise_image(dir_temp, prefixo, inp):
    # estimate 'background' color by a median filter
    bg = signal.medfilt2d(inp, 11)
    arq_bg = dir_temp + 'background_' + prefixo + '.png'
    save(arq_bg, bg)

    # compute 'foreground' mask as anything that is significantly darker than
    # the background
    mask = inp < bg - 0.1
    arq_mask = dir_temp + 'foreground_mask_' + prefixo + '.png'
    save(arq_mask, mask)

    # return the input value for all pixels in the mask or pure white otherwise
    return np.where(mask, inp, 1.0)

def Limpa_background(path, prefixo):
    # Carrega imagem com ruido em base64
    dir_temp = path + 'dataset/temp/'
    image = path + "dataset/ruido_base64/" + prefixo + ".txt" # le imagem a ser limpa
    read_file = open(image, 'rb')
    data = read_file.read()   # data e a imagem com ruido em base64

    # decodifica arquivo para imagem png
    decode_b64 = pybase64.b64decode(data)

    # grava imagem decodificada no diretorio temp
    path_temp = dir_temp  + prefixo + '.png'
    out_file = open(path_temp, 'wb')
    out_file.write(decode_b64)

    image = Image.open(path_temp)
    image.show()
    
    # carrega imagem salva como png
    inp = load_image(path_temp)

    # limpa imagem
    out = denoise_image(dir_temp, prefixo, inp)

    # salva imagem limpa decodificada
    arq_limpa_decode = path + 'dataset/limpa_decode/' + prefixo  + '.png'
    save(arq_limpa_decode, out)
    #out_file = open(arq_limpa_decode, 'wb')
    #out_file.write(out)

    # codifica imagem
    read_file = open(arq_limpa_decode, 'rb')
    data_limpa = read_file.read()
    encode_b64 = pybase64.b64encode(data_limpa)

    # grava imagem em base64
    arq_limpa_base64 = path + 'dataset/limpa_base64/' + prefixo  + '.txt'
    out_file = open(arq_limpa_base64, 'wb')
    out_file.write(encode_b64)

    # adiciona no banco
    arquivo = Arquivos(nome= prefixo , caminho= arq_limpa_base64, img_origem =  data, img_limpa = encode_b64)
    return arquivo