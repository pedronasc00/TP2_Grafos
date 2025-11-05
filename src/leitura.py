import networkx as nx
import pandas as pd

def criarGrafos(datasets_coloring: str) -> nx.Graph | None :
    try:
        df = pd.read_csv(datasets_coloring)
    except FileNotFoundError:
        print(f"Erro: Arquivo {datasets_coloring} não encontrado!")
        return None
    except pd.errors.EmptyDataError:
        print(f"Erro: Arquivo {datasets_coloring} vazio!")
        return None
    except Exception as e:
        print(f"Erro inesperado! {e}")
        return None

    Grafo = nx.from_pandas_edgelist(df, 'Disciplina1', 'Disciplina2')

    print(f"Grafo de conflitos montado com sucesso.")
    print(f"  - {Grafo.number_of_nodes()} disciplinas (vértices)")
    print(f"  - {Grafo.number_of_edges()} conflitos (arestas)")

    return Grafo