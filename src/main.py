import gcol
import pandas as pd
import time
import argparse

from leitura import criarGrafos

parser = argparse.ArgumentParser(description="Executa algoritmos de coloração GCol em um grafo de conflitos.")
parser.add_argument("arquivo_csv", help="O caminho para o arquivo .csv contendo os conflitos.")
args = parser.parse_args()

Dataset = args.arquivo_csv

algoritmosTestes = [
    "dsatur",
    "rlf",
    "random",
    "welsh_powell"
]

resultadosAlgoritmos = []

Grafo = criarGrafos(Dataset)

if Grafo is None:
    print(f"Erro: não foi possivel criar o grafo.")
else:
    
    for algsNome in algoritmosTestes:
        try:
            tempoInicio = time.time()

            coloring_map = gcol.node_coloring(Grafo, strategy=algsNome)

            tempoFim = time.time()

            tempoGasto = tempoFim - tempoInicio
            numCores = len(set(coloring_map.values()))
            resultadosAlgoritmos.append({
                "algoritmo": algsNome,
                "tempoExecucao": tempoGasto,
                "num_cores": numCores,
                "mapa_coloracao": coloring_map
            })
        except Exception as e:
            print(f"Erro ao executar {algsNome}: {e}")
            resultadosAlgoritmos.append({
                "algoritmo": algsNome,
                "tempoExecucao": -1,
                "num_cores": -1,
                "mapa_coloracao": None
            })
        
    print("----Comparação de Algoritmos----\n")

    df_resultados = pd.DataFrame(resultadosAlgoritmos)
    df_resultados = df_resultados.sort_values(by=["num_cores", "tempoExecucao"])

    print(df_resultados.to_string(
        columns=["algoritmo", "num_cores", "tempoExecucao"],
        header=["Algoritmo", "Nº de Cores", "Tempo"],
        index=False,
        float_format="{:,.6f}".format
    ))

    if not df_resultados.empty and df_resultados.iloc[0]["num_cores"] > 0:
        melhorResultado = df_resultados.iloc[0]

        print("\n--- Melhor Resultado ---")
        print(f"Algoritmo: {melhorResultado['algoritmo']}")
        print(f"Número de cores (Horários): {melhorResultado['num_cores']}")
        print(f"Tempo de execução aproximado: {melhorResultado['tempoExecucao']:.6f} segundos")

        print("\n")

        mapa_cores = resultadosAlgoritmos[melhorResultado.name]['mapa_coloracao']

        for disciplina, cor in mapa_cores.items():
            print(f"  - {disciplina}: Horário {cor}")
            