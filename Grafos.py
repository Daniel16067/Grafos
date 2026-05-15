import networkx as nx
import numpy as np
from sympy import Matrix
import matplotlib.pyplot as plt

# =========================================================
# 1. CREAR EL GRAFO DIRIGIDO
# =========================================================
G = nx.DiGraph()

# =========================================================
# 2. DEFINIR LOS NODOS
# =========================================================
nodos = [
    "AA","AB","AC","AD","AE","AF","AG","AI","AJ","AK","AL","AM","AN","AO",
    "AP","AQ","AR","AS","AT","AU","AV","AX","AY","AZ","BA","BB","BC","BD",
    "BE","BF","BG","BH","BI","BJ","BK","BL","BM","BN","BO","BP","BQ","BR",
    "BS","BT","BU","BV","BX","BY","BZ","CC","CD","CE","CF"
]

G.add_nodes_from(nodos)

# =========================================================
# 3. DEFINIR LAS ARISTAS
# =========================================================
aristas = [
    ("AA", "AB"), ("AB", "AC"), ("AC", "AD"), ("AC", "AI"), ("AD", "AE"),
    ("AD", "AG"), ("AE", "AF"), ("AF", "AP"), ("AF", "AG"), ("AG", "AI"),

    ("AI", "AK"), ("AK", "AL"), ("AK", "AT"), ("AT", "AS"), ("AL", "AM"),
    ("AM", "AN"), ("AM", "AZ"), ("AZ", "AY"), ("AY", "AX"), ("AN", "AO"),

    ("AO", "AU"), ("AO", "AP"), ("AJ", "AK"), ("AS", "AJ"), ("AT", "AX"),
    ("AX", "BG"), ("AY", "AL"), ("AZ", "AN"), ("BA", "AZ"), ("AN", "AP"),

    ("AU", "BA"), ("BB", "AU"), ("AP", "AV"), ("AU", "AV"), ("AV", "BD"),
    ("BD", "BC"), ("BC", "BC"), ("BC", "BB"), ("BD", "BL"), ("BJ", "BB"),

    ("BK", "BL"), ("BI", "BJ"), ("BG", "BH"), ("BH", "BY"), ("BG", "BF"),
    ("BF", "AS"), ("AS", "AR"), ("AR", "AR"), ("AR", "AQ"), ("AQ", "BE"),

    ("BF", "BE"), ("BE", "BM"), ("BM", "BO"), ("BO", "BF"), ("BO", "BN"),
    ("BO", "BP"), ("BP", "BQ"), ("BQ", "BX"), ("BQ", "BR"), ("BR", "BI"),

    ("BR", "BS"), ("BS", "BS"), ("BS", "BT"), ("BL", "BV"), ("BT", "BV"),
    ("BV", "BY"), ("BU", "BY"), ("BU", "BU"), ("BU", "BX"), ("BX", "BQ"),

    ("BX", "BZ"), ("BP", "BZ"), ("BZ", "CC"), ("CC", "BO"), ("CD", "CC"),
    ("CD", "BN"), ("CD", "CE"), ("BN", "CD"), ("BM", "CE"), ("CE", "CF")
]

G.add_edges_from(aristas)

# =========================================================
# 4. ORIGEN Y DESTINO
# =========================================================
origen = "AA"
destino = "CF"

# =========================================================
# 5. CAMINO MÁS CORTO
# =========================================================
try:
    min_cuadras = nx.shortest_path_length(G, source=origen, target=destino)
    camino = nx.shortest_path(G, source=origen, target=destino)

    print("=== CAMINO MÁS CORTO ===")
    print(f"Cantidad mínima de cuadras: {min_cuadras}")
    print("Ruta:")
    print(" -> ".join(camino))

except nx.NetworkXNoPath:
    print("No existe camino entre AA y CF")

# =========================================================
# 6. MATRIZ DE ADYACENCIA
# =========================================================
nodos_lista = list(G.nodes())

idx_origen = nodos_lista.index(origen)
idx_destino = nodos_lista.index(destino)

matriz_np = nx.to_numpy_array(G, nodelist=nodos_lista, dtype=int)
matriz = Matrix(matriz_np)

# =========================================================
# 7. FUNCIÓN PARA CONTAR CAMINOS EXACTOS
# =========================================================
def contar_caminos(matriz, k, inicio, fin):
    potencia = matriz ** k
    return int(potencia[inicio, fin])

# =========================================================
# 8. CANTIDAD DE CAMINOS
# =========================================================
caminos_10 = contar_caminos(matriz, 10, idx_origen, idx_destino)
caminos_50 = contar_caminos(matriz, 50, idx_origen, idx_destino)
caminos_100 = contar_caminos(matriz, 100, idx_origen, idx_destino)

# =========================================================
# 9. RESULTADOS
# =========================================================
print("\n=== CANTIDAD DE CAMINOS ===")
print(f"Caminos de exactamente 10 cuadras: {caminos_10}")
print(f"Caminos de exactamente 50 cuadras: {caminos_50}")
print(f"Caminos de exactamente 100 cuadras: {caminos_100}")

# =========================================================
# 10. VISUALIZACIÓN DEL GRAFO
# =========================================================

plt.figure(figsize=(20, 14))

# Posiciones automáticas de los nodos
pos = nx.spring_layout(G, seed=42)

# Colores de nodos
color_nodos = []

for nodo in G.nodes():
    if nodo == origen:
        color_nodos.append("green")      # Nodo inicial
    elif nodo == destino:
        color_nodos.append("red")        # Nodo final
    elif nodo in camino:
        color_nodos.append("orange")     # Camino más corto
    else:
        color_nodos.append("lightblue")

# Dibujar nodos
nx.draw_networkx_nodes(
    G,
    pos,
    node_color=color_nodos,
    node_size=900
)

# Dibujar aristas normales
nx.draw_networkx_edges(
    G,
    pos,
    edge_color="gray",
    arrows=True,
    arrowsize=15
)

# Resaltar el camino más corto
aristas_camino = list(zip(camino[:-1], camino[1:]))

nx.draw_networkx_edges(
    G,
    pos,
    edgelist=aristas_camino,
    edge_color="blue",
    width=3,
    arrows=True,
    arrowsize=20
)

# Etiquetas
nx.draw_networkx_labels(
    G,
    pos,
    font_size=8,
    font_weight='bold'
)

# Título
plt.title("Grafo dirigido del Barrio El Lago", fontsize=18)

# Quitar ejes
plt.axis("off")

# Mostrar
plt.show() 
