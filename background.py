import numpy as np
from scipy import signal
from PIL import Image
import pybase64
from banco import Arquivos

def load_image(path):
    return np.asarray(Image.open(path)) /255.0  # transforma a imagem .png em array e dimensiona os valores de pixel
                                                # na faixa de 0-1
                                                # etapa de pre-processamento comum
def save(path, img):
    tmp = np.asarray(img*255.0, dtype=np.uint8)
    Image.fromarray(tmp).save(path)

def denoise_image(dir_temp, prefixo, inp):
    # estimativa da cor de fundo por um filtro mediano
    # com kernel de 11 pixels
    bg = signal.medfilt2d(inp, 11)
    arq_bg = dir_temp + 'background_' + prefixo + '.png'
    save(arq_bg, bg)

    # calcula a mascara 'primeiro plano' como qualquer coisa que seja significativamente mais escura
    # do que o plano de fundo
    mask = inp < bg - 0.1
    arq_mask = dir_temp + 'foreground_mask_' + prefixo + '.png'
    save(arq_mask, mask)

    # return the input value for all pixels in the mask or pure white otherwise
    return np.where(mask, inp, 1.0)

def Limpa_background(path, prefixo):
    # Carrega imagem com ruido em base64
    dir_temp = path + 'dataset/temp/'      # diretorio temporario para trabalhar com as imagens
    image = path + "dataset/ruido_base64/" + prefixo + ".txt" # le imagem em base64 a ser limpa,
    read_file = open(image, 'rb')
    data = read_file.read()  # data e a variavel com a imagem com ruido em base64
    read_file.close()   # nao foi colocado no git

    # decodifica arquivo para imagem png - transforma txt para png
    decode_b64 = pybase64.b64decode(data)

    # grava imagem decodificada no diretorio temp
    path_temp = dir_temp  + prefixo + '.png'
    out_file = open(path_temp, 'wb')
    out_file.write(decode_b64)
    out_file.close() # nao esta no git

    # mostra a imagen a ser limpa
    #image = Image.open(path_temp)
    #image.show()
    
    # carrega imagem salva como png, do diretorio temporario. Transformada em array e valores
    # de pixel entre 0-1
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

    # mostra a imagen  limpa
    image = Image.open(arq_limpa_decode)
    image.show()

    # adiciona no banco
    arquivo = Arquivos(nome= prefixo , caminho= arq_limpa_base64, img_origem =  data, img_limpa = encode_b64)
    return arquivo