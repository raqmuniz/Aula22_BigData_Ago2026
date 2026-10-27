import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt


# Obtendo os dados
try:
    print(f'Obtendo os dados...')

    ENDERECO_DADOS = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'

    # utf-8, iso-8859-1, latin1, cp1252
    df_ocorrencias = pd.read_csv(ENDERECO_DADOS, sep=';', encoding='iso-8859-1')
        # print(df_ocorrencias)
    
    df_ocorrencias = df_ocorrencias[df_ocorrencias['regiao'] == 'Interior']

    # delimitando os dados
    df_roubo_veiculo = df_ocorrencias[['munic', 'roubo_veiculo']]
    # print(df_roubo_veiculo.head(30))
    # print(df_roubo_veiculo.tail(30))


    # ### PREPARANDO OS DADOS
    # Totalizando os roubos por cidade (Var Qualitativa 'munic' e Var Quant 'roubo_veiculo')
    df_roubo_veiculo = df_roubo_veiculo.groupby('munic', as_index=False)['roubo_veiculo'].sum()

    # Obtendo o total e o percentual de roubos por município
    #Total
    total_roubos = df_roubo_veiculo['roubo_veiculo'].sum()

    # Percentual
    df_roubo_veiculo['percentual %'] = round(
        ((df_roubo_veiculo['roubo_veiculo']/total_roubos) * 100), 2
    )


    # Ordenando os dados
    df_roubo_veiculo = df_roubo_veiculo.sort_values(
        by='roubo_veiculo',
        ascending=False
    )

    print(df_roubo_veiculo.head(10))
    # print(df_roubo_veiculo.tail(10))

except Exception as e:
    print(f'Erro ao obter os dados - {e}')



try:
    print(f'\nObtendo informações a cerca dos roubos dos veículos...')
    array_roubo_veiculo = np.array(df_roubo_veiculo['roubo_veiculo'])

    media_roubo_veiculo = np.mean(array_roubo_veiculo)
    mediana_roubo_veiculo = np.median(array_roubo_veiculo)
    distancia = abs(
        (media_roubo_veiculo - mediana_roubo_veiculo) / mediana_roubo_veiculo * 100
    )

    print(f'\nMedidas de Tendência Central')
    print(f'Média: {media_roubo_veiculo}')
    print(f'Mediana: {mediana_roubo_veiculo}')
    print(f'Distância Média - Mediana: {distancia:.2f}%')


except Exception as e:
    print(f'Obtendo Medidas - {e}')



# Calculando os quartis
try:
    print(f'\nSeparando os quartis...')
    q1 = np.quantile(array_roubo_veiculo, .25)
    q2 = np.quantile(array_roubo_veiculo, .50)
    q3 = np.quantile(array_roubo_veiculo, .75)

    print(f'\nMedidas de Posição')
    print(f'Q1: {q1}')
    print(f'Q2: {q2}')
    print(f'Q3: {q3}')

    # Cidades c/ menos ocorrências de roubos
    df_roubo_veiculo_menores = df_roubo_veiculo[
        df_roubo_veiculo['roubo_veiculo'] < q1
    ]

    # Cidades c/ maiores ocorrências de roubos
    df_roubo_veiculo_maiores = df_roubo_veiculo[
        df_roubo_veiculo['roubo_veiculo'] > q3
    ]

    # Menores
    print(f'\nMunicípios com menores roubos')
    print(30*'-')
    print(df_roubo_veiculo_menores.sort_values(by='roubo_veiculo', ascending=True))
    # Exportando o dataframe
    # index=False - Não exporta os índices. Salva os dados das colunas munic e roubo_veiculo
    # sep=';' - Altera o separador de colunas para ';'
    # encoding='iso-8859-1' - Informa o encoding para salvar o csv. "Pode ser o mesmo"
    df_roubo_veiculo_menores.to_csv('menores.csv', index=False, sep=';', encoding='iso-8859-1')

    # Maiores
    print(f'\nMunicípios com maiores roubos')
    print(30*'-')
    print(df_roubo_veiculo_maiores.sort_values(by='roubo_veiculo', ascending=False))
    # Exportando o dataframe
    df_roubo_veiculo_maiores.to_csv('maiores.csv', index=False, sep=';', encoding='iso-8859-1')


except Exception as e:
    print(f'Erro ao analizar a distribuição {e}')

#Medidas de Posição e dispersão
try:
    print('n\Calculando a Amplitude Total')
    #Amplitude_total = maior - menor
    #Quanto mais próximo de 0, mais homogêneos são os dados do cnjunto
    #Quanto mais próximo do maior valor, mais hetereogêneo é o conjunto de dados
    maximo = np.max(array_roubo_veiculo)
    minimo = np.min(array_roubo_veiculo)
    amplitude = maximo - minimo
     

except Exception as e:
    print(f'Erro ao calcular amplitude: {e}')


#Medidas de dispersão
try:
#variância
    #É uma medida de observação da dispersão dos dados
    #Observa-se em relação à média
    #É a média dos quadrados das diferenças de cada valor e a média
    #Obs: O resultado da variância está elevado ao quadrado
    variancia = np.var(array_roubo_veiculo)

    #distância variância média
    #<10% - Baixa Dispersão
    #Entre 10% - 25% - Dispersão moderada
    #Acima dos 25% - Alta dispersão

    distancia_var_media = variancia / (media_roubo_veiculo **2) *100

    #Desvio padrão (Raiz quadrada da variância). Observa-se em relação à média.
    #É a Normalização da variância
    #Quanto os dados se afastam da média
    desvio_padrao = np.std(array_roubo_veiculo)

    #Coeficiente de variação
    #É a magnitude do desvio padrão em relação à média
    coef_variacao = (desvio_padrao / media_roubo_veiculo) * 100



except Exception as e:
    print(f'Erro ao calcular a variabiliade do conjunto {e}')

#Verificando a assimetria da distribuição
    #Indica como os dados estão distribuídos. Para que lado tende a distribuição
try:
    # Assimetria > 1 (Assimetria Positiva alta); Cauda longa, à direita
    #Existem valores altos, "puxando" a média para cima
    # A média tende a ser maior que a mediana

    # Assimetria entre 0,5 e 1 (Assimetria Positiva moderada); Cauda menos acentuada, à direita
    # A média tende a ser maior que a mediana


    # Assimetria entre -0,5 e 0,5 
    # Tendência a uma simetria (Dados tendem a estar equilibrados em torno do centro)
    # Medidas de tendência central aproximados


    #  # Assimetria entre -0,5 e -1 (Assimetria Negativa moderada); Cauda menos acentuada, à esquerda
    # A média tende a ser menor que a mediana

     # Assimetria < 1 (Assimetria Negativa alta); Cauda longa, à esquerda
    #Existem valores baixos, "puxando" a média para baixo
    # A média tende a ser menor que a mediana

    assimetria = df_roubo_veiculo['roubo_veiculo'].skew()

    # Curtose
    # É uma medida que verifica o peso das caudas de uma distribuição 
    # Indicando a importância dos valores extremos. 
    # Quanto maior a curtose, maior tende a ser a influência dos extremos.

    # Referência: Excesso de curtose de Fisher (pandas)

    # -0.5 a 0.5 (Aproximadamente mesocúrtica)
    # Curtose próxima de uma distribuição normal
    # Outliers não são comuns, mas pode ocorrer.

    # Curtose > 0.5 (Leptocúrtica)
    # Caudas mais longas e pesadas e maior influência dos extremos.
    # Poucos valores muito extremos, elevando bastante a curtose.
    # Pode apresentar picos muito altos.
    # Outliers são mais frequentes

    # Curtose < -0.5 (Platcúrtica)
    # Caudas mais leves. Menor influência dos extremos.
    # Tende à distribuição mais achatada.

    curtose = df_roubo_veiculo['roubo_veiculo'].kurtosis()


    print('n\Analisando a distribuição')
    print(30*'-')
    print(f'Assimetria: {assimetria}')
    print(f'Curtose: {curtose}')


except Exception as e:
    print(f'Erro ao calcular a assimetria e curtose dos dados {e}')

# Achando os outliers
try:
    # Intervalo Interquartil
    # É a amplitude dos dados mais centrais
    iqr = q3 - q1

    # calculando os limites
    # Superior
    limite_superior = q3 + (1.5 * iqr)

    # Inferior
    limite_inferior = q1 - (1.5 * iqr)


    print(f'\nLimite Superior: {limite_superior}')
    print(f'\nLimite Inferior: {limite_inferior}')

    # Filtrando os outliers menores
    df_roubo_veiculo_outliers_menores = (
        df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] < limite_inferior]
    )

    # Printando os outliers menores
    print('\nMunicípios com outliers inferiores')
    print(30*'-')
    if len(df_roubo_veiculo_outliers_menores) == 0:
        print('Não há outliers Inferiores')
    else:
        print(df_roubo_veiculo_outliers_menores)
    

    # Printando os outliers maiores
    df_roubo_veiculo_outliers_maiores = (
        df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] > limite_superior]
    )

    print('\nMunicípios com outliers superiores')
    print(30*'-')
    if len(df_roubo_veiculo_outliers_maiores) == 0:
        print('Não há outliers Superiores')
    else:
        print(df_roubo_veiculo_outliers_maiores)

except Exception as e:
    print(f'Erro ao calcular os outliers {e}')


try: 
    print(f'n/Mostrando Medidas')
    print(30*'-')
    print(f'Mínimo: {minimo}')
    print(f'Máximo: {maximo}')
    print(f'Limite inferior: {limite_inferior}')
    print(f'Q1: {q1}')
    print(f'Q2: {q2}')
    print(f'Q3: {q3}')
    print(f'Limite Superior: {limite_superior}')
    print(f'Máximo {maximo}')
    print(f'Total de roubos: {total_roubos}')

    print(f'\nMédia: {media_roubo_veiculo}')
    print(f'Mediana : {mediana_roubo_veiculo}')
    print(f'Distância: {distancia}')
    print(f'IQR: {iqr}')
    print(f'Amplitude: {amplitude}')
    print(f'Variância: {variancia: .2f}')
    print(f'Distância Variância e Média: {distancia_var_media: .2f}')
    print(f'Desvio Padrão: {desvio_padrao: .2f}')
    print(f'Coeficiente de variação: {coef_variacao: .2f}%') 



except Exception as e:
    print(f'Erro ao mostrar as medidas {e}')


#Plotando gráficos
    # print('Plotando BoxPlot')
    #pip install matplotlib
   # import matplotlib.pyplot as plt (lá em cima)
try:
    print('\nInformações de Roubos de Veículos')
    plt.figure(figsize= (16, 10))
    #Posição 1 - BoxPlot
    plt.subplot(2, 2, 1)

    
#Boxplot 
    plt.boxplot(df_roubo_veiculo['roubo_veiculo'], orientation='horizontal', showmeans=True, showfliers=True)
    plt.title('Distribuição de dados')
    plt.xlabel('Roubo de Veículos')
    #plt.ylabel('Municípios')
    #showfliers coloca ou remove os outliers
    #showmeans = média (coloca (True) ou retira (False))

#Posição 2
    plt.subplot(2, 2, 2)
    plt.text(0.1, 0.95, f'Limite inferior: {limite_inferior}', fontsize=12)
    #0.1 é o eixo x e 0.95 é o eixo y
    plt.text(0.1, 0.90, f'Minimo: {minimo}', fontsize=12)
    plt.text(0.1, 0.85, f'Q1: {q1}', fontsize=12)
    plt.text(0.1, 0.80, f'Q2: {q2}', fontsize=12)
    plt.text(0.1, 0.75, f'Q3: {q3}', fontsize=12)
    plt.text(0.1, 0.70, f'Limite Superior: {limite_superior}')
    plt.text(0.1, 0.65, f'Máximo: {maximo}', fontsize=12)

    plt.text(0.1, 0.55, f'Mediana: {mediana_roubo_veiculo}', fontsize=12)
    plt.text(0.1, 0.50, f'Média: {media_roubo_veiculo}', fontsize=12)
    plt.text(0.1, 0.45, f'IQR Intervalo Interquartil: {iqr}', fontsize=12)
    plt.text(0.1, 0.40, f'Amplitude Total: {amplitude}', fontsize=12)
    plt.text(0.1, 0.35, f'Máximo: {maximo}', fontsize=12)
    plt.axis('off')

#Histograma
    plt.subplot(2, 2, 3)

    plt.hist(array_roubo_veiculo, bins=100, edgecolor= 'black')
    plt.axvline(media_roubo_veiculo, color='green', linewidth= 1)
    plt.axvline(mediana_roubo_veiculo, color='orange', linewidth= 1)

    contagens, limites = np.histogram(array_roubo_veiculo, bins=100)
    #print(contagens)

    print(f'\nFaixas de roubos do histograma')
    for i in range(len(contagens)):
        # Não vai printar as contagens de zero município
        if contagens[i] > 0:
            print(
                f'Faixa {i + 1}:'
                f'{limites[i]:.0f} até {limites[i+1]:.0f} roubos'
                f'=> {contagens[i]} Municipios'
        )

#Gráfico de colunas / Top 10 Maiores
    plt.subplot(2, 2, 4)
    df_roubo_veiculo_10maiores = (
    df_roubo_veiculo_maiores
    .head(10)
    .sort_values(by= 'roubo_veiculo', ascending=True)
)

    plt.bar(df_roubo_veiculo_10maiores['munic'], df_roubo_veiculo_10maiores['roubo_veiculo'])

    plt.xticks(rotation=45, ha='right')
    plt.xlabel('Municípios')
    plt.ylabel('Roubo de veículos')

    plt.suptitle('Informações Roubo veículos')


    plt.show()



except Exception as e:
    print(f'Erro ao plotar o gráfico {e}')
