#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from turtle import *
from percursos import Waze

# add as seguintes bibliotecas
from utils import vector
from random import choice

class Agente:

    # inclui cor e tartaruta pro agente
    def __init__(self, id, tam_agente, cor=None):
        # add uma identificação única pro agente
        self._id = id
        self._tam_agente = tam_agente

        # add uma tartaruga específica pro agente
        self._turtle = Turtle()
        self._turtle.hideturtle()

        # define a cor do agente
        self._cor = cor
        # REQ
        # deve definir a cor do agente aleatoriamente (verde, vermelho, rosa, laranja e marrom)
        # se não for passado no construtor
        # é um gerador de percursos

        self._waze = None

        # add os seguintes comandos
        # TODO: Conferir estas direções
        # vector(1, 0) => direita
        # vector(-1, 0) => esquerda
        # vector(0, 1) => cima
        # vector(0, -1) => baixo
        self.direcao = vector(1,0) # este vector significa direita


    # adiciona um labirinto
    def add_labirinto(self, lab):
        self._labirinto = lab
        self._posicao = lab.cel_aleatoria()
        # REQ
        # Deve funcionar para passos menores que lab._tam_celula
        self.tam_passo = lab._tam_celula

    # Note que o nome do método mudou um pouco
    def desenhar_se(self, posicao=None):
        """ Leva a tartaruga até a posição (x,y) e desenha por exemplo um círculo
            para representar o agente (i.e., pacman, fantasmas)
        """
        self._turtle.clear()
        if (not posicao):
            posicao = self._posicao

        x, y = posicao.coord_turt_centralizada()
        self._turtle.up()
        self._turtle.goto(x , y)
        self._turtle.down()
        self._turtle.dot(self._tam_agente, self._cor)

    """ Métodos de percurso """

    def add_percurso(self):
        # Só na primeira vez que o agente não terá um _waze definido
        if (not self._waze):
            self._waze = Waze(self._labirinto) # Cria o objeto _waze passando uma referência do labirinto

    def percorrer(self):
        """ Percorrer significa seguir passar por todas as celulas do labirinto """
        pos_agente = self._posicao # Para melhorar a legibilidade

        self.add_percurso()
        if (self._waze.fim_percurso()): # Questiona se é fim de percurso
            self._waze = None # Se o percurso terminou, reinicializa o _waze
            return True # Se terminou, retorna indicando o término

        if (self._waze.esta_sem_coord()): # Se _waze está criado, mas sem coordenadas
            self._waze.gerar_percurso(pos_agente) # Gere um percurso

        if (not self._waze.esta_sem_coord()): # Se houver coordenadas a serem seguidas
            self._posicao = self._waze.obter_prox_coord() # Obtenha a próx e defina como a posição do agente
        self.desenhar_se() # Desenha o agente na posição em que se encontra

        return False # Se chegou até aqui é o porque não terminou o percurso e retorna False

    def vaguear(self):
        """ Vaguear significa continuar andando na mesma direção até que se
            encontre um obstáculo, quando se muda a direção aleatoriamente
        """
        lab = self._labirinto
        # REQ
        # Deve obter o passo (sem efetivamente dar o passo)
        passo = self.prox_passo()
        lin_p, col_p = passo
        alin, acol = self._posicao.coord_turtle()
        prox_pos_agente = lab.criar_celula(coord_turt=(alin + lin_p, acol + col_p))
        lin, col = prox_pos_agente.coord_matriz()
        id_ = self._id
        # REQ
        # Deve verificar:
        # Se der o passo, continua sendo caminho (lab.eh_caminho())
        if lab.eh_caminho(lin,col) and not(lab.eh_celula_ocupada((lin,col), id_)):
            self._posicao = prox_pos_agente
        else:
            prox_pos_agente = self._posicao
            self.direcao = self.mudar_direcao_aleatoriamente()
        # REQ
        # Deve verificar:
        # Se der o passo, a posição estará ocupada? (lab.eh_celula_ocupada())

        # REQ
        # Definir qual é a próxima posição do agente
        # Caso a posição não esteja ocupada ocupada e nem seja caminho:
        # Muda o agente para a posição do novo passo
        # Caso contrário
        # Escolhe a nova direção aleatoriamente

        #self.posicao = prox_pos_agente
        # Desenhar a posição na tela
        self.desenhar_se()
        return

    def prox_passo(self):
        """ Obtém o próximo passo do agente na direção em que se encontra """
        dir_x = self.direcao[0] * self.tam_passo
        dir_y = self.direcao[1] * self.tam_passo

        passo = vector(dir_x, dir_y)
        return passo

    def mudar_direcao_aleatoriamente(self):
        """ Escolhe alguma direção aleatoriamente que não seja a atual """
        # REQ implementar o método
        passo = [vector(1,0),vector(-1,0),vector(0,1),vector(0,-1)]
        random = choice(passo)

        return random

    """
    ROTA
    """
    def add_rota(self, destino):
        if (not self._waze):
            self._waze = Waze(self._labirinto)
            self._waze.add_destino(destino)

    def ir_a(self, destino):
        lab = self._labirinto # Para facilitar a leitura
        pos_agente = self._posicao

        self.add_rota(destino)
        waze = self._waze
        if (waze.chegou_ao_destino(pos_agente)):
            waze = None # Para uma próxima iteração, um novo destino
            return True

        if (waze.esta_sem_coord()):
            waze.gerar_rota(pos_agente)

        if (not waze.esta_sem_coord()):
            self._posicao = waze.obter_prox_coord()
            self.desenhar_se()
        return False