import networkx as nx
import numpy as np
from sympy import Matrix, Integer  # For handling large integers in matrix powers

# 1. Crear el grafo dirigido (DiGraph)
G = nx.DiGraph()

# Definir todos los nodos
nodos_especiales = ["AA", "CF"]
nodos_azules = [
    "AB", "AC", "AD", "AE", "AF", "AG", "AI", "AJ", "AK", "AL", "AM", "AN", 
    "AO", "AP", "AQ", "AR", "AS", "AT", "AU", "AV", "AW", "AX", "AY", "AZ", 
    "BA", "BB", "BC", "BD", "BE", "BF", "BG", "BH", "BI", "BJ", "BK", "BL", 
    "BM", "BN", "BO", "BP", "BQ", "BR", "BS", "BT", "BU", "BV", "BX", "BY", 
    "BZ", "CC", "CD", "CE"
]
G.add_nodes_from(nodos_especiales + nodos_azules)

# Definir la lista de aristas (Flechas) según el mapa vial del barrio
# Removed duplicates and self-loops (e.g., ("BC", "BC"), ("AR", "AR"), etc., and duplicate ("CE", "CD"))
aristas = [
    ("AA", "AB"), ("AB", "AC"), ("AC", "AD"), ("AD", "AE"), ("AE", "AF"), 
    ("AG", "AF"), ("AD", "AG"), ("AI", "AG"), ("AC", "AI"), ("AK", "AI"), 
    ("AK", "AL"), ("AL", "AM"), ("AM", "AN"), ("AN", "AO"), ("AO", "AP"), 
    ("AF", "AP"), ("AJ", "AK"), ("AS", "AJ"), ("AW", "AK"), ("AS", "AT"), 
    ("AT", "AX"), ("AX", "AL"), ("AY", "AW"), ("AY", "AM"), ("AZ", "AY"), 
    ("AZ", "AN"), ("BA", "AZ"), ("AN", "AP"), ("AU", "BA"), ("BB", "AU"), 
    ("AP", "AV"), ("AU", "AV"), ("AV", "BD"), ("BC", "BD"), 
    ("BB", "BC"), ("BD", "BL"), ("BJ", "BB"), ("BK", "BL"), ("BI", "BJ"), 
    ("BH", "BA"), ("BG", "BH"), ("AX", "BG"), ("AW", "BH"), ("AT", "AW"), 
    ("BF", "BG"), ("AS", "BF"), ("AR", "AS"), ("AQ", "AR"), 
    ("AQ", "BE"), ("BE", "BF"), ("BM", "BE"), ("BM", "BF"), ("BN", "BM"), 
    ("BO", "BN"), ("BP", "BO"), ("BP", "BQ"), ("BQ", "BH"), ("BQ", "BR"), 
    ("BR", "BI"), ("BR", "BS"), ("BS", "BT"), ("BL", "BV"), 
    ("BT", "BV"), ("BV", "BY"), ("BU", "BY"), ("BX", "BU"), 
    ("BX", "BQ"), ("BZ", "BX"), ("BZ", "BP"), ("CC", "BZ"), ("CC", "BP"), 
    ("CD", "CC"), ("CD", "BO"), ("CE", "CD"), ("CE", "BN"), 
    ("CE", "BM"), ("CE", "CF") 
]
G.add_edges_from(aristas)

# Identificar origen (tooGEEK) y destino (Kuty)
origen = "AA"
destino = "CF"

# =====================================================================
# ALGORITMO 1: Cantidad mínima de cuadras (Shortest Path Length)
# =====================================================================
try:
    min_cuadras = nx.shortest_path_length(G, source=origen, target=destino)
    camino_nodos = nx.shortest_path(G, source=origen, target=destino)
except nx.NetworkXNoPath:
    min_cuadras = None

# =====================================================================
# ALGORITMO 2: Contar caminos de longitud exacta usando Álgebra Lineal
# =====================================================================
# Obtener la matriz de adyacencia y la lista ordenada de nodos
nodos_lista = list(G.nodes())
idx_origen = nodos_lista.index(origen)
idx_destino = nodos_lista.index(destino)

adj_matrix_np = nx.to_numpy_array(G, nodelist=nodos_lista, dtype=int)
adj_matrix = Matrix(adj_matrix_np)  # Convert to SymPy Matrix for big integers

def contar_caminos_longitud(matriz, k, start_idx, end_idx):
    # Eleva la matriz de adyacencia a la potencia k usando SymPy
    matriz_potencia = matriz ** k
    # El valor en la coordenada representa la cantidad de caminos exactos
    return int(matriz_potencia[start_idx, end_idx])

caminos_10 = contar_caminos_longitud(adj_matrix, 10, idx_origen, idx_destino)
caminos_50 = contar_caminos_longitud(adj_matrix, 50, idx_origen, idx_destino)
caminos_100 = contar_caminos_longitud(adj_matrix, 100, idx_origen, idx_destino)

# =====================================================================
# PRESENTACIÓN DE RESULTADOS
# =====================================================================
print("=== RESPUESTAS AL PROFESOR ===")
if min_cuadras is not None:
    print(f"1. Cantidad mínima de cuadras desde tooGEEK hasta Kuty: {min_cuadras} cuadras.")
    print(f"   Ruta óptima sugerida: {' -> '.join(camino_nodos)}")
else:
    print("1. No hay conexión directa respetando los sentidos de las calles.")

print(f"2. Cantidad de caminos posibles pasando por EXACTAMENTE 10 cuadras: {caminos_10}")
print(f"3. Cantidad de caminos posibles pasando por EXACTAMENTE 50 cuadras: {caminos_50}")
print(f"4. Cantidad de caminos posibles pasando por EXACTAMENTE 100 cuadras: {caminos_100}")