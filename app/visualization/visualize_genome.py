import networkx as nx
import matplotlib.pyplot as plt

def visualize_network(genome, config):
    G = nx.DiGraph()
    
    # Add nodes with different colors for input, output, and hidden
    for node_key, node in genome.nodes.items():
        if node_key in config.genome_config.input_keys:
            G.add_node(node_key, color="lightblue", label=f"Input {node_key}")
        elif node_key in config.genome_config.output_keys:
            G.add_node(node_key, color="salmon", label=f"Output {node_key}")
        else:
            G.add_node(node_key, color="lightgreen", label=f"Hidden {node_key}")

    # Add edges with weights as labels
    for conn_key, conn in genome.connections.items():
        in_node, out_node = conn_key
        if in_node not in G and conn.enabled:
            G.add_node(in_node, color="lightblue", label=f"Implicit {in_node}") 
        if out_node not in G and conn.enabled:
            G.add_node(out_node, color="lightgreen", label=f"Implicit {out_node}")
        if conn.enabled:
            G.add_edge(conn_key[0], conn_key[1], weight=round(conn.weight, 2))


    # Draw the network
    pos = nx.spring_layout(G)  # Using spring layout for better spacing
    edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
    # Assign a default color ("gray") if "color" is not in the node's data
    node_colors = [data.get("color", "gray") for _, data in G.nodes(data=True)]

    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=700, font_size=10)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
    plt.title("Winning NEAT Network")
    plt.show()