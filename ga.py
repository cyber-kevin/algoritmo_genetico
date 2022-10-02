###########################################
# Universidade Federal Rural de Pernambuco#
# Autor: Kevin VinÍcius Ferreira de Lima  #
# Data: 28/09/2022                        #
# e-mail: oficialkevinferreira@gmailcom   #
###########################################

from random import randint, shuffle, random, seed
from math import factorial
from time import time

#============ CONFIGURAÇÕES DA MATRIZ DE ENTRADA ============#

def obterCoordenadas(matriz): # Obtém as coordenadas de cada ponto de entrega na matriz
    coordenadas = dict()

    for linha in range(len(matriz)):
        for coluna in range (len(matriz[linha])):
            if matriz[linha][coluna] != '0':
                coordenadas[matriz[linha][coluna]] = [linha, coluna]
    
    return coordenadas


def calcularDistancia(rota, coordenadas): # Calcula distância total da rota
    distancia = 0
    linha_partida, coluna_partida = coordenadas['R']

    for i in range(len(rota[0])):
        if i == 0:
            #Calcula a distância entre o ponto de partida e o primeiro local de entrega e soma à distância entre o primeiro ponto de entrega e o segundo ponto de entrega
            linha_atual, coluna_atual = coordenadas[rota[0][i]]
            linha_destino, coluna_destino = coordenadas[rota[0][i+1]]

            distancia += abs(linha_atual - linha_partida) + abs(coluna_atual - coluna_partida) + abs(linha_destino - linha_atual) + abs(coluna_destino - coluna_atual)

        elif i == len(rota[0]) - 1: 
            #Calcula a distância entre o último local de entrega e o ponto de partida (representando a "volta" para o ponto de onde partiu)
            linha_atual, coluna_atual = coordenadas[rota[0][i]]

            distancia += abs(linha_partida - linha_atual) +  abs(coluna_partida - coluna_atual)
        else:
            #Calcula a distância entre o ponto atual e o seguinte
            linha_atual, coluna_atual = coordenadas[rota[0][i]]
            linha_destino, coluna_destino = coordenadas[rota[0][i+1]]

            distancia += abs(linha_destino - linha_atual) + abs(coluna_destino - coluna_atual)
        
    return distancia

#============ ALGORITMO GENÉTICO ============#

seed(7)

def gerarPopulacao(lista, n_individuos):

    populacao = [] # variável que armazenará a população

    tam_max = factorial(len(lista)) 
    # fatorial da quantidade de elementos (o que significa a quantidade de permutações possíveis com estes elementos)

    for _ in range(n_individuos): # laço de repetição que se repetirá de acordo com o parâmetro passado

        # se a população já atingiu seu tamanho máximo, ou seja, todas as permutações possíveis, interrompe o laço
        if len(populacao) == tam_max: 
            break

        # OBS.: mesmo que o tamanho máximo seja um número superior a {n_individuos}, a população conterá apenas {n_individuos} indivíduos, visto que o laço se repete apenas {n_individuos} vezes.

        shuffle(lista) # embaralha a lista
        individuo = lista # salva a lista na variável individuo

        if [individuo] not in populacao: # se aquele individuo não estiver na população, ele é adicionado à lista
            populacao.append([individuo[:]]) # lista populacao adiciona a CÓPIA da variável individuo
         
         # OBS.: O cromossomo do indivíduo é representado por uma lista dentro de outra lista [['A', 'B', 'C']]


    return populacao # retorna a população abastecida


def avaliarPopulacao(pop, coordenadas):

    distancia_pop = [] # lista onde ficarão salvas as distancias de cada individuo
    maior_dist = 0 # inicializa a maior distância com 0

    for individuo in pop: # para cada individuo da população ...

        dist = calcularDistancia(individuo, coordenadas) # calcula a distancia do individuo(rota)
        distancia_pop.append(dist) # adiciona a distancia à lista das distancias
        individuo.append(dist) # Adiciona a distância do indivíduo à sua célula # Ex.: [['A', 'B', 'C'], 18]

        if dist > maior_dist: 
            # se a distancia calculada for maior do que a maior distância ...
            maior_dist = dist 

    for d in range(len(distancia_pop)): 

        # a aptidão do individuo é determinada pela diferença entre sua distancia e maior distancia
        aptidao = maior_dist - distancia_pop[d]  
        pop[d].append(aptidao) # adiciona a aptidao ao lado da distancia do individuo na lista da populacao
        # ↓
        # individuo = [[cromossomo], distancia, aptidao]     |    Ex.: [['A', 'B', 'C'], 18, 7] #


def selecionar(pop):

    vencedores = [] # lista que armazenará os vencedores da seleção

    # MÉTODO DE SELEÇÃO POR TORNEIO

    for _ in range(len(pop)): 
        # duelo recebe dois individuos selecionados aleatoriamente
        duelo = [pop[randint(0, len(pop)-1)], pop[randint(0, len(pop)-1)]]

        # se a aptidão do individuo 1 for maior, ele ganha, senão, o individuo 2 ganha
        if duelo[0][2] > duelo[1][2]:
            vencedores.append(duelo[0])
        else:
            vencedores.append(duelo[1])
    
    return vencedores
    

def crossover(vencedores, tam):

    filhos = [] # lista vazia para armazenar os filhos

    # variáveis auxiliares para manipular os indíces no interior do laço
    atual = 0
    prox = 1

    for i in range(int(len(vencedores)/2)): # 2 pais geram 2 filhos, logo, a iteração é a metade da qtd. de pais

        pai1 = vencedores[i+atual][0] # armazena o cromossomo do pai1
        pai2 = vencedores[i+prox][0] # armazena o cromossomo do pai2

        pais = [pai2, pai1] # armazena os pais em ordem inversa em uma lista

        corte = randint(0, tam-1) # variável que guarda a posição do corte nos cromossomos

        # realiza os cortes no cromossomo de cada pai
        corte_pai1 = pai1[:corte] 
        corte_pai2 = pai2[:corte]

        cortes = [corte_pai1, corte_pai2] # armazena os cortes de cada pai em uma lista

        for c in range(len(cortes)): 
            filho = cortes[c]   # filho recebe os genes do corte de um pai

            for gene in pais[c]: # para cada gene do outro pai ...
                if gene not in filho: # se este gene não está no filho
                    filho.append(gene) # filho herda o gene
            
            filhos.append([filho]) # lista filhos recebe o filho gerado
        
        atual += 1
        prox += 1

    return filhos


def mutacao(filhos):
    taxa_mut = 0.05 # Taxa de mutação de 5%

    for f in range(len(filhos)):
        m = random() # Sorteia um número entre zero e 1

        if m <= taxa_mut: # Se o valor sorteado for menor ou igual à taxa estabelecida, altera-se a ordem de um dos genes do cromossomo do individuo ...

            # Altera a ordem dos genes na posição 0 e 1  
            # Ex.: [['A', 'B', 'C'], 18, 7] --> [['B', 'A', 'C'], 18, 7] #

            filhos[f][0][0], filhos[f][0][1] = filhos[f][0][1], filhos[f][0][0]


def algoritmoGenetico(matriz_de_entrada, n_individuos=100, n_geracoes=100):

    #== CONFIGURAÇÕES DA MATRIZ ==#

    pontos = [] # lista que armazenará os pontos da matriz
    coordenadas = obterCoordenadas(matriz_de_entrada) # obtém as posições(linha x coluna) dos pontos na matriz

    for k in coordenadas.keys(): # para cada chave do dicionário em coordenadas ...
        if k != 'R': # se a chave for diferente de "R" (ou seja, a chave não é o ponto de partida)
            pontos.append(k) # o valor da chave é adicionado à lista de pontos
    
    n_pontos = len(pontos) # quantidade de pontos

    #== ESTRUTURA DO ALGORITMO GENÉTICO ==#

    pop = gerarPopulacao(pontos, n_individuos) # gera a população inicial
    avaliarPopulacao(pop, coordenadas) # avalia o desempenho da população inicial

    for geracao in range(n_geracoes):
        selecionados = selecionar(pop) # seleciona os melhores individuos
        pop = crossover(selecionados, n_pontos) # cruza os individuos selecionados e obtém os filhos
        mutacao(pop) # calcula a possibilidade de mutação dos filhos
        avaliarPopulacao(pop, coordenadas) # avalia a aptidão dos filhos gerados 


    maior_aptidao = -1
    mais_apto = None
    menor_dist = None
    for individuo in pop: # para cada individuo da populacao ...
        if individuo[2] > maior_aptidao: # se aptidão do individuo for maior do que a maior aptidão ...
            maior_aptidao = individuo[2] # maior_aptidao recebe o valor da aptidao desse individuo
            mais_apto = individuo[0] # o cromossomo do individuo é salvo em mais_apto
            menor_dist = individuo[1] # a distância do individuo é salva em menor_dist
    
    return mais_apto, menor_dist


if __name__ == '__main__':
    matriz = [] # lista que armazenará a matriz de entrada
    arquivo = open('matriz1.txt') # lê a o arquivo .txt onde se encontra a matriz
    linhas = arquivo.readlines() # armazena as linhas da matriz

    for linha in linhas: # para cada linha armazenada em linhas ...
        if not linha.isspace():
            matriz.append(linha.replace("\n", ""). split(" ")) # matriz adiciona linha formatada 
    

    resultado = algoritmoGenetico(matriz, 100, 100)
    print(f'{" → ".join(resultado[0])} | Distância: {resultado[1]} dronômetros')




