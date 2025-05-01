from mip import *

def ler_arquivo(nome_arquivo):
    with open(nome_arquivo, 'r') as f:
        linhas = f.readlines()

    #Gerando uma matriz com os valores das linhas
    val_linhas = [linha.strip().split() for linha in linhas]

    #salvando número de variáveis e restrições 
    num_variaveis = int(val_linhas[0][0])
    num_restricoes = int(val_linhas[0][1])

    #salvando um array com os  coeficientes da função objetivo (podem ser floats)
    coef_func_objetivo = list(map(float, val_linhas[1]))

    #salvando uma matriz com os coeficientes das restrições (podem ser floats)
    coef_restricoes = []
    for i in range(num_restricoes):
        restricao = list(map(float, val_linhas[2 + i])) # restrições começam a partir da linha 2 do arquivo
        coef_restricoes.append(restricao)
    
    return num_variaveis, num_restricoes, coef_func_objetivo, coef_restricoes

#--------------------------------------------------------------------------------------------------------------------


def Branch_and_Bound(num_variaveis, num_restricoes, coef_func_objetivo, coef_restricoes):

    zd = float("inf")
    zp = float ("-inf")

    model = Model(sense=MAXIMIZE, solver_name=CBC)

    #definindo as variaveis
    x = [model.add_var(var_type=CONTINUOUS, name=f"x_{i}", lb=0.0, ub=1.0) for i in range(num_variaveis)]

    # função objetivo é a somatorio das variaveis multiplicadas pelos respectivos coeficientes
    model.objective = xsum(coef_func_objetivo[i]*x[i] for i in range(num_variaveis))

    #Adicionando as restrições
    for i in range(num_restricoes):
        model += xsum(coef_restricoes[i][j]*x[j] for j in range(len(coef_restricoes[i])-1)) <= coef_restricoes[i][-1]

    #Criando uma lista de modelos
    models = [model]


    #Iniciando o looping de ramificação e podas
    while(models):

        status = models[0].optimize()

        print("\nValor Zi =", models[0].objective_value, "\n")

        #Poda por inviabilidade
        if status == OptimizationStatus.INFEASIBLE:
            models.pop(0)
            continue

        #Poda por limitante quando o valor da solução relaxada é menor ou igual ao zp
        if(models[0].objective_value <= zp):
            models.pop(0)
            continue

        # Verificando as variáveis não inteiras
        vars_not_int = []
        for var in models[0].vars:
            print(f"{var.name} = {var.x:.2f}" + (" (não é inteira)" if not var.x.is_integer() else ""))
            if not var.x.is_integer():
                vars_not_int.append(var) #adicionando no array de não inteiras


        #Se houverem variáveis não inteiras
        if vars_not_int:
            
            #É preciso encontrar a mais próxima de 0.5
            mais_proximo_05 = min(vars_not_int, key=lambda var: abs(var.x - 0.5))
            print("A variável mais próxima de 0.5:", mais_proximo_05, "\n")


            #Criando duas ramificações a partir da variável não inteira
            model2 = models[0].copy()
            model2 += mais_proximo_05 == 0
            models.append(model2)

            
            model3 = models[0].copy()
            model3 += mais_proximo_05 == 1
            models.append(model3)
            

            if(zd > models[0].objective_value):
                zd = models[0].objective_value


        #Poda por integralidade
        else:

            if(zp < models[0].objective_value):
                zp = models[0].objective_value

        models.pop(0)
    
    print(zp)

#--------------------------------------------------------------------------------------------------------------------

num_variaveis, num_restricoes, coef_func_objetivo, coef_restricoes = ler_arquivo("teste1.txt")

Branch_and_Bound(num_variaveis, num_restricoes, coef_func_objetivo, coef_restricoes)

