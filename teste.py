import os
from collections import Counter, deque

# Função para limpar o terminal
def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

# Definindo as listas
Coluna_1C = [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34]
Coluna_2C = [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35]
Coluna_3C = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36]

# Lista inicial vazia e limite de tamanho
tamanho_maximo = 50
ultimos_numeros = deque(maxlen=tamanho_maximo)

# Contador de entradas
contador_entradas = 0
ultima_entrada = None

# Função para contar as ocorrências de todos os números de uma coluna
def contar_total_ocorrencias(coluna, contador):
    total_ocorrencias = sum(contador.get(numero, 0) for numero in coluna)
    return total_ocorrencias

# Função para calcular e retornar as porcentagens
def calcular_percentuais():
    # Criando o contador para os números em ultimos_numeros
    contador = Counter(ultimos_numeros)
    
    # Contando as ocorrências totais para cada coluna
    total_ocorrencias_coluna_1C = contar_total_ocorrencias(Coluna_1C, contador)
    total_ocorrencias_coluna_2C = contar_total_ocorrencias(Coluna_2C, contador)
    total_ocorrencias_coluna_3C = contar_total_ocorrencias(Coluna_3C, contador)

    # Dividindo os totais por 50 e convertendo para porcentagem
    percentual_ocorrencias_coluna_1C = (total_ocorrencias_coluna_1C / tamanho_maximo) * 100
    percentual_ocorrencias_coluna_2C = (total_ocorrencias_coluna_2C / tamanho_maximo) * 100
    percentual_ocorrencias_coluna_3C = (total_ocorrencias_coluna_3C / tamanho_maximo) * 100

    return {
        'Coluna_1C': percentual_ocorrencias_coluna_1C,
        'Coluna_2C': percentual_ocorrencias_coluna_2C,
        'Coluna_3C': percentual_ocorrencias_coluna_3C
    }

# Função para determinar a coluna e classificação do último número
def determinar_coluna_e_classificacao(numero):
    percentuais = calcular_percentuais()
    
    if numero in Coluna_1C:
        coluna = 'Coluna_1C'
        percentual = percentuais['Coluna_1C']
    elif numero in Coluna_2C:
        coluna = 'Coluna_2C'
        percentual = percentuais['Coluna_2C']
    elif numero in Coluna_3C:
        coluna = 'Coluna_3C'
        percentual = percentuais['Coluna_3C']
    else:
        coluna = 'Nenhuma coluna'
        percentual = 0
    
    # Classificando a porcentagem
    if percentual < 20:
        classificacao = 'fraca'
    elif percentual < 50:
        classificacao = 'média'
    else:
        classificacao = 'alta'
    
    return coluna, percentual, classificacao, percentuais

# Função para sugerir ações baseadas nos percentuais
def sugestao_acao(coluna_atual, percentual_atual, percentuais):
    if percentual_atual <= 26:
        # Identifica outras colunas com percentuais maiores
        outras_colunas = [(col, perc) for col, perc in percentuais.items() if col != coluna_atual and perc > percentual_atual]
        outras_colunas.sort(key=lambda x: x[1], reverse=True)  # Ordena em ordem decrescente
        
        if len(outras_colunas) >= 2:
            col1, perc1 = outras_colunas[0]
            col2, perc2 = outras_colunas[1]
            return f'Entrar na coluna {col1} e coluna {col2}'
        elif len(outras_colunas) == 1:
            col1, perc1 = outras_colunas[0]
            return f'Entrar na coluna {col1}'
        else:
            return 'Nenhuma coluna com percentual maior disponível.'
    else:
        return 'Nenhuma ação necessária.'

# Loop contínuo para entrada do usuário
while True:
    try:
        comando = input("Digite um número, 'corrigir' para ajustar a última entrada, ou 'sair' para terminar: ")
        
        if comando.lower() == 'sair':
            break
        elif comando.lower() == 'corrigir':
            if ultima_entrada is None:
                print("Nenhuma entrada para corrigir.")
                continue
            
            novo_numero = input(f"Digite o novo número para substituir o último ({ultima_entrada}): ")
            try:
                novo_numero = int(novo_numero)
                ultimos_numeros.remove(ultima_entrada)
                ultimos_numeros.append(novo_numero)
                print(f"Última entrada corrigida: {novo_numero}")
                ultima_entrada = novo_numero
            except ValueError:
                print("Número inválido.")
                continue
        else:
            # Convertendo a entrada para um número inteiro
            numero = int(comando)
            
            # Adicionando o número à lista mantendo o limite de 50 elementos
            if len(ultimos_numeros) == tamanho_maximo:
                ultima_entrada = ultimos_numeros.popleft()
            ultimos_numeros.append(numero)
            
            # Incrementando o contador de entradas
            contador_entradas += 1
            
            # Limpar o terminal antes de exibir as novas informações
            limpar_terminal()
            
            # Calculando e exibindo as porcentagens e o total de entradas após cada entrada
            percentuais = calcular_percentuais()
            
            # Determinando a coluna e a classificação do último número
            coluna, percentual, classificacao, percentuais = determinar_coluna_e_classificacao(numero)
            
            # Imprimindo informações adicionais sobre o último número
            print(f'% 1C: {percentuais["Coluna_1C"]:.2f}%')
            print(f'% 2C: {percentuais["Coluna_2C"]:.2f}%')
            print(f'% 3C: {percentuais["Coluna_3C"]:.2f}%')
            print('-')
            print(f'Quantidade de números contabilizados: {len(ultimos_numeros)}')
            print('-')
            print(f'Último número contabilizado: {numero}')
            print('-')
            
            # Sugerindo ação com base no percentual da coluna
            acao = sugestao_acao(coluna, percentual, percentuais)
            print(f'Ação a ser tomada: {acao}')
            print('-')
            
            # Atualiza a última entrada com o número atual
            ultima_entrada = numero
    
    except ValueError:
        print("Por favor, insira um número válido ou um comando ('corrigir', 'sair').")
