import numpy as np
import random
from chrome_trex import DinoGame
from pygame import constants

CHANCE_MUT = .20
CHANCE_CROS = .25
NUM_INDIVIDOS = 45
NUM_MELHORES = 4

def populacaoAleatoria(n):
    populacao=[]
    for i in range(n):
        populacao.append(np.random.uniform(-10,10,(3,10)))
    return populacao

def valorDasAcoes(individuo,estado):
    return individuo@estado

def melhorJogada(individuo,estado):
    valores = valorDasAcoes(individuo,estado)
    return np.argmax(valores)

def mutacao(individuo):
    for i in range(3):
        for j in range(10):
            if np.random.uniform(0,1) < CHANCE_MUT:
                individuo[i][j] *= np.random.uniform(-1.5,1.5)

def Crossing_Over(individuo1,individuo2):
    filho = individuo1.copy()
    for i in range(3):
        for j in range(10):
            if np.random.uniform(0,1) < CHANCE_CROS:
                filho[i][j] = individuo2[i][j]
    return filho

def fitness(jogo,individuo):
    jogo.reset()
    while not jogo.game_over:
        estado= jogo.get_state()
        # print(jogo.get_state())
        acao = melhorJogada(individuo,estado)
        jogo.step(acao)
    return jogo.get_score()

def ordenar_lista(lista,ordenacao,decrescente=True):
    return [x for _, x in sorted(zip(ordenacao,lista), key=lambda p: p[0], reverse = decrescente)]
    
def proximaGeracao(populacao,fitness):
    ordenados = ordenar_lista(populacao,fitness)
    proxima_gen = ordenados[:NUM_MELHORES]
    while len(proxima_gen) < NUM_INDIVIDOS:
        ind1,ind2 = random.choices(populacao,k=2)
        filho = Crossing_Over(ind1,ind2)
        mutacao(filho)
        proxima_gen.append(filho)
    return proxima_gen

def main():
    num_geracao = 5
    jogo = DinoGame(fps=0)
    populacao = populacaoAleatoria(NUM_INDIVIDOS)

    print('ger | fitness\n------+-' + '-'*5*NUM_INDIVIDOS)
    for ger in range(num_geracao):
        fitnessL =[]
        for ind in populacao:
            fitnessL.append(fitness(jogo, ind))
        populacao = proximaGeracao(populacao,fitnessL)
        print('{:3} |'.format(ger),' '.join('{:4d}'.format(s) for s in sorted(fitnessL, reverse=True)))
    
    fitnessL=[]
    for ind in populacao:
        fitnessL.append(fitness(jogo,ind))
    jogo.fps = 100
    ordenados = ordenar_lista(populacao,fitnessL)
    melhor = ordenados[0]
    print('melhor:', melhor)
    fit = fitness(jogo,melhor)
    print('Fitness: {:4.1f}'.format(jogo.get_score()))

main()