import networkx as nx
from pyvis.network import Network

def build_graph(txs):
    G = nx.DiGraph()

    for tx in txs:

        # ✅ Skip bad data
        if not isinstance(tx, dict):
            continue

        sender = tx.get("sender", "unknown")

        receivers = tx.get("receivers", [])

        # ✅ Handle both formats safely
        for r in receivers:
            if isinstance(r, dict):
                receiver = r.get("address", "unknown")
            else:
                receiver = str(r)

            G.add_edge(sender, receiver)

    net = Network(height="600px", width="100%", directed=True)
    net.from_nx(G)
    net.save_graph("graph.html")


def draw_graph(txs):
    build_graph(txs)