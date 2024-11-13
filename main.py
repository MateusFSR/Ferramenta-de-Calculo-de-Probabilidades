import tkinter as tk
from tkinter import messagebox
from collections import Counter, deque

# Definindo as listas
Coluna_1C = [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34]
Coluna_2C = [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35]
Coluna_3C = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36]

# Lista inicial vazia e limite de tamanho
tamanho_maximo = 50
ultimos_numeros = deque(maxlen=tamanho_maximo)

# Contador de entradas
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

# Função chamada quando o botão de adicionar é pressionado
def adicionar_numero(event=None):
    global ultima_entrada
    try:
        numero = int(entrada.get())
        
        # Adicionando o número à lista mantendo o limite de 50 elementos
        if len(ultimos_numeros) == tamanho_maximo:
            ultima_entrada = ultimos_numeros.popleft()
        ultimos_numeros.append(numero)
        
        # Calculando e exibindo as porcentagens e o total de entradas
        percentuais = calcular_percentuais()
        coluna, percentual, classificacao, percentuais = determinar_coluna_e_classificacao(numero)
        
        # Atualizando a interface com as novas informações
        resultado.set(f"% 1C: {percentuais['Coluna_1C']:.2f}%\n"
                      f"% 2C: {percentuais['Coluna_2C']:.2f}%\n"
                      f"% 3C: {percentuais['Coluna_3C']:.2f}%\n"
                      f"-\n"
                      f"Quantidade de números contabilizados: {len(ultimos_numeros)}\n"
                      f"-\n"
                      f"Último número contabilizado: {numero}\n"
                      f"-\n"
                      f"Ação a ser tomada: {sugestao_acao(coluna, percentual, percentuais)}\n"
                      f"-")
        
        ultima_entrada = numero
        entrada.delete(0, tk.END)  # Limpa o campo de entrada
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira um número válido.")

# Função chamada quando o botão de corrigir é pressionado
def corrigir_ultima_entrada():
    global ultima_entrada
    if ultima_entrada is None:
        messagebox.showwarning("Aviso", "Nenhuma entrada para corrigir.")
        return
    try:
        novo_numero = int(entrada.get())
        ultimos_numeros.remove(ultima_entrada)
        ultimos_numeros.append(novo_numero)
        
        # Calculando e exibindo as porcentagens e o total de entradas
        percentuais = calcular_percentuais()
        coluna, percentual, classificacao, percentuais = determinar_coluna_e_classificacao(novo_numero)
        
        # Atualizando a interface com as novas informações
        resultado.set(f"% 1C: {percentuais['Coluna_1C']:.0f}%\n"
                      f"% 2C: {percentuais['Coluna_2C']:.0f}%\n"
                      f"% 3C: {percentuais['Coluna_3C']:.0f}%\n"
                      f"-\n"
                      f"Quantidade de números contabilizados: {len(ultimos_numeros)}\n"
                      f"-\n"
                      f"Último número contabilizado: {novo_numero}\n"
                      f"-\n"
                      f"Ação a ser tomada: {sugestao_acao(coluna, percentual, percentuais)}\n"
                      f"-")
        
        ultima_entrada = novo_numero
        entrada.delete(0, tk.END)  # Limpa o campo de entrada
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira um número válido.")

# Configurando a interface gráfica
root = tk.Tk()
root.title("Roll Calculate")

# Definindo o tamanho da janela (largura x altura)
root.geometry('500x250')

# Cor de fundo da janela principal
root.configure(bg='#001a00')

# Layout da interface
tk.Label(root, text="Digite um número:", bg='#001a00', fg='white').pack()
entrada = tk.Entry(root)
entrada.pack()

tk.Button(root, text="Adicionar", command=adicionar_numero, bg='lightgreen').pack()
tk.Button(root, text="Corrigir Última Entrada", command=corrigir_ultima_entrada, bg='lightcoral').pack()

resultado = tk.StringVar()
tk.Label(root, textvariable=resultado, bg='#001a00', fg='white').pack()

# Vinculando a tecla Enter para adicionar números
root.bind('<Return>', adicionar_numero)

root.mainloop()
