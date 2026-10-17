"""Small plotting helpers for the notebook and CLI."""
import matplotlib.pyplot as plt

def draw_topology(processor, output_path=None):
    edges = processor["coupling_edges"]
    n = processor["physical_qubits"]
    angle = [2*3.141592653589793*i/n for i in range(n)]
    xy = [(0.5+0.42*__import__('math').cos(a), 0.5+0.42*__import__('math').sin(a)) for a in angle]
    fig, ax = plt.subplots(figsize=(5, 4))
    for a, b in edges:
        ax.plot([xy[a][0], xy[b][0]], [xy[a][1], xy[b][1]], color="#9ca3af", zorder=1)
    ax.scatter([p[0] for p in xy], [p[1] for p in xy], s=500, color="#7c1730", zorder=2)
    for i, (x, y) in enumerate(xy): ax.text(x, y, str(i), color="white", ha="center", va="center", zorder=3)
    ax.set_title(f"{processor['name']} coupling map"); ax.axis("off"); fig.tight_layout()
    if output_path: fig.savefig(output_path, dpi=160, bbox_inches="tight")
    return fig
