import matplotlib.pyplot as plt
import networkx as nx
from collections import deque
from matplotlib.patches import Patch

from solver import get_next_states


def build_state_graph(capacity_a, capacity_b):
    """Build the graph of every reachable water-jug state."""

    graph = nx.DiGraph()
    start = (0, 0)
    queue = deque([start])
    visited = {start}

    while queue:
        current = queue.popleft()
        graph.add_node(current)

        for next_state, operation in get_next_states(
            current, capacity_a, capacity_b
        ):
            graph.add_edge(
                current,
                next_state,
                label=operation
            )

            if next_state not in visited:
                visited.add(next_state)
                queue.append(next_state)

    return graph


def draw_state_graph(
    capacity_a,
    capacity_b,
    target,
    solution_path=None
):
    """Draw all reachable states and valid transitions."""

    graph = build_state_graph(capacity_a, capacity_b)

    solution_states = {
        item["state"] for item in (solution_path or [])
    }

    positions = nx.spring_layout(
        graph,
        seed=42,
        k=1.3,
        iterations=150
    )

    node_colors = []

    for state in graph.nodes():
        if state == (0, 0):
            node_colors.append("lightgreen")
        elif state[0] == target or state[1] == target:
            node_colors.append("gold")
        elif state in solution_states:
            node_colors.append("lightskyblue")
        else:
            node_colors.append("lightgray")

    fig, ax = plt.subplots(figsize=(13, 9))

    nx.draw_networkx_nodes(
        graph,
        positions,
        node_color=node_colors,
        node_size=1450,
        edgecolors="black",
        linewidths=1.2,
        ax=ax
    )

    nx.draw_networkx_labels(
        graph,
        positions,
        labels={
            state: f"({state[0]}, {state[1]})"
            for state in graph.nodes()
        },
        font_size=9,
        font_weight="bold",
        ax=ax
    )

    nx.draw_networkx_edges(
        graph,
        positions,
        arrows=True,
        arrowsize=14,
        edge_color="gray",
        alpha=0.6,
        connectionstyle="arc3,rad=0.10",
        min_source_margin=18,
        min_target_margin=18,
        ax=ax
    )

    legend_items = [
        Patch(facecolor="lightgreen", edgecolor="black",
              label="Initial state"),
        Patch(facecolor="gold", edgecolor="black",
              label="Target state"),
        Patch(facecolor="lightskyblue", edgecolor="black",
              label="BFS solution path"),
        Patch(facecolor="lightgray", edgecolor="black",
              label="Other reachable states")
    ]

    ax.legend(handles=legend_items, loc="upper left",
              bbox_to_anchor=(1.01, 1), fontsize=9)

    ax.set_title(
        f"Complete Water Jug State-Space Graph\n"
        f"A = {capacity_a} L | B = {capacity_b} L | "
        f"Target = {target} L",
        fontsize=14,
        fontweight="bold"
    )

    ax.axis("off")
    fig.tight_layout()

    return fig


def draw_solution_path(
    solution_path,
    capacity_a,
    capacity_b,
    target
):
    """Draw only the shortest solution found by BFS."""

    graph = nx.DiGraph()

    states = [item["state"] for item in solution_path]

    for index in range(len(solution_path) - 1):
        current = solution_path[index]
        following = solution_path[index + 1]

        graph.add_edge(
            current["state"],
            following["state"],
            label=following["operation"]
        )

    if len(solution_path) == 1:
        graph.add_node(states[0])

    # Place states in solution order.
    positions = {
        state: (index * 2.5, 0)
        for index, state in enumerate(states)
    }

    node_colors = []

    for state in states:
        if state == (0, 0):
            node_colors.append("lightgreen")
        elif state[0] == target or state[1] == target:
            node_colors.append("gold")
        else:
            node_colors.append("lightskyblue")

    fig, ax = plt.subplots(
        figsize=(max(10, len(states) * 2.6), 5)
    )

    nx.draw_networkx_nodes(
        graph,
        positions,
        node_color=node_colors,
        node_size=1900,
        edgecolors="black",
        linewidths=1.3,
        ax=ax
    )

    nx.draw_networkx_labels(
        graph,
        positions,
        labels={
            state: f"({state[0]}, {state[1]})"
            for state in graph.nodes()
        },
        font_size=10,
        font_weight="bold",
        ax=ax
    )

    nx.draw_networkx_edges(
        graph,
        positions,
        arrows=True,
        arrowsize=22,
        width=2,
        edge_color="darkblue",
        min_source_margin=25,
        min_target_margin=25,
        ax=ax
    )

    edge_labels = nx.get_edge_attributes(graph, "label")

    nx.draw_networkx_edge_labels(
        graph,
        positions,
        edge_labels=edge_labels,
        font_size=8,
        font_color="darkblue",
        rotate=False,
        label_pos=0.5,
        bbox={
            "alpha": 0.9,
            "color": "white",
            "edgecolor": "none",
            "pad": 2
        },
        ax=ax
    )

    ax.set_title(
        f"BFS Shortest Solution Path\n"
        f"A = {capacity_a} L | B = {capacity_b} L | "
        f"Target = {target} L | "
        f"Minimum operations = {len(solution_path) - 1}",
        fontsize=13,
        fontweight="bold",
        pad=20
    )

    ax.axis("off")
    fig.tight_layout()

    return fig
