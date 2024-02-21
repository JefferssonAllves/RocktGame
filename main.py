import pygame
import sys
from os.path import join
import multiprocessing
from time import sleep
from random import randint

pygame.init()
pygame.display.init()
window = pygame.display.set_mode() #Vai receber o tamanho atual da tela
WINDOW_SIZE = window.get_size()

#Carrega imagens
subir_ondas = True
CONST_POS_ONDAS = 0.6
CONST_VELO_ONDAS = 0.0005

indice_pos_ondas = CONST_POS_ONDAS

ondaGrande = pygame.image.load(join('img/ondas', 'ondasGrandes.svg'))

def mov_ondas(indice_pos_ondas, subir_ondas, valor_compartilhado):
    try:
        while True:
            if indice_pos_ondas >= CONST_POS_ONDAS + 0.03 or subir_ondas:
                subir_ondas = True
                indice_pos_ondas-=CONST_VELO_ONDAS

            if indice_pos_ondas <= CONST_POS_ONDAS or not subir_ondas:
                if indice_pos_ondas <= CONST_POS_ONDAS:
                    sleep(randint(0,10))

                subir_ondas = False
                indice_pos_ondas+=CONST_VELO_ONDAS

            sleep(0.009)
            valor_compartilhado.value = indice_pos_ondas
    except KeyboardInterrupt:
        print(">>> PROCESSO INTERROMPIDO: MOV_ONDAS <<<")

indice_pos_atual = multiprocessing.Value('f', CONST_POS_ONDAS)

process = multiprocessing.Process(target=mov_ondas, args=(indice_pos_ondas, subir_ondas, indice_pos_atual))
process.start()

barco = pygame.image.load(join('img', 'barco.svg'))
POSX_BARCO = (randint(0, WINDOW_SIZE[0] - barco.get_size()[0]))
POSY_BARCO = barco.get_size()[1] + 26

imagem_foguete = pygame.image.load(join('img', 'foguete.svg'))
foguete = pygame.transform.scale(imagem_foguete, (300, 300))

foguete_rotacionado = foguete
TAM_FOGUETE_X, TAM_FOGUETE_Y = foguete.get_size()

rotacao_foguete = 0
posx_foguete = POSX_BARCO + 35
posy_foguete = POSY_BARCO + 220

POSICAO_INICIAL = posy_foguete

aceleracao_foguete = 0.5
desacelerar_foguete = 3
aumento_gravidade = 0.12


fogo_foguete = pygame.image.load(join('img', 'fogo.png'))
fogo_foguete = pygame.transform.scale(fogo_foguete, (25, 120))
fogo_rotacionado = fogo_foguete

# nuvens = [
#     pygame.image.load(join('img/nuvens', 'nuvem1.svg')),
#     pygame.image.load(join('img/nuvens', 'nuvem2.svg')),
# ]
def atualizar_tela():
    window.fill((0, 103, 238, 0.74))
    pos_ondas = [
                (0, WINDOW_SIZE[1] - ondaGrande.get_size()[1] * indice_pos_atual.value),
                (0, WINDOW_SIZE[1] - (ondaGrande.get_size()[1] - 85) * indice_pos_atual.value),
            ]

    window.blit(ondaGrande, pos_ondas[0])
    window.blit(barco, (POSX_BARCO,  WINDOW_SIZE[1] - POSY_BARCO))
    window.blit(ondaGrande, pos_ondas[1])
    window.blit(foguete_rotacionado, (posx_foguete * 0.5, posy_foguete - 300))


atualizar_tela()

while(True):
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            print(">>> O JOGO FOI ENCERRADO <<<")
            pygame.quit()
            sys.exit()

    atualizar_tela()

    print(foguete_rotacionado.get_rect())

    if pygame.key.get_pressed()[pygame.K_SPACE]:
        posy_foguete -= aceleracao_foguete
        aceleracao_foguete += aumento_gravidade
        desacelerar_foguete -= aumento_gravidade
        # window.blit(fogo_rotacionado, (posx_foguete + foguete.get_size()[0] * 0.45 + rotacao_foguete, posy_foguete + 273 + rotacao_foguete))
    else:
        posy_foguete += desacelerar_foguete
        aceleracao_foguete -= aumento_gravidade
        desacelerar_foguete += aumento_gravidade


    # AJEITAR ESSE BLOCO DE CODIGO, LOGICA TA RUIM
    if pygame.key.get_pressed()[pygame.K_RIGHT]:
        rotacao_foguete -= 0.25
    elif pygame.key.get_pressed()[pygame.K_LEFT]:
        rotacao_foguete += 0.25

    print(rotacao_foguete, posy_foguete)
    posx_foguete -= rotacao_foguete // 3
    # AJEITAR ESSE BLOCO DE CODIGO, LOGICA TA RUIM


    foguete_rotacionado = pygame.transform.rotate(foguete, rotacao_foguete)
    fogo_rotacionado = pygame.transform.rotate(fogo_foguete, rotacao_foguete)

    pygame.display.update()