from mip import *

def ler_arquivo(nome_arquivo):
    with open(nome_arquivo, 'r') as f:
        linhas = f.readlines()

    # Gerando uma matriz com os valores das linhas
    val_linhas = [linha.strip().split() for linha in linhas]

    # salvando número de variáveis e restrições 
    num_variaveis = int(val_linhas[0][0])
    num_restricoes = int(val_linhas[0][1])

    # salvando um array com os  coeficientes da função objetivo (podem ser floats)
    coef_func_objetivo = list(map(float, val_linhas[1]))

    # salvando uma matriz com os coeficientes das restrições (podem ser floats)
    coef_restricoes = []
    for i in range(num_restricoes):
        restricao = list(map(float, val_linhas[2 + i])) # restrições começam a partir da linha 2 do arquivo
        coef_restricoes.append(restricao)
    
    return num_variaveis, num_restricoes, coef_func_objetivo, coef_restricoes


#--------------------------------------------------------------------------------------------------------------------

def Branch_and_Bound(num_variaveis, num_restricoes, coef_func_objetivo, coef_restricoes):

    model = Model(sense=MAXIMIZE, solver_name=CBC)

    #definindo as variaveis
    x = [model.add_var(var_type=CONTINUOUS, name=f"x_{i}", lb=0.0) for i in range(num_variaveis)]

    # função objetivo é a soma das variaveis vezes os coeficientes
    model.objective = xsum(coef_func_objetivo[i]*x[i] for i in range(num_variaveis))


    for i in range(num_restricoes):
        for j in  range(len(coef_restricoes[i])-1):
            model += xsum(coef_restricoes[i][j] * x[j] <= coef_restricoes[i][j - 1])
            print()



num_variaveis, num_restricoes, coef_func_objetivo, coef_restricoes = ler_arquivo("teste1.txt")

Branch_and_Bound(num_variaveis, num_restricoes, coef_func_objetivo, coef_restricoes)




        

    