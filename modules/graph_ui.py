from enum import Enum

import networkx as nx
import pandas as pd
from shiny import ui, render, reactive

from modules.djikstra_explanation import djikstra_explanation
from utils.graph_generators import generate_random_graph, generate_koot_example
from utils.graph_utils import plot_graph

distances_df = reactive.Value(pd.DataFrame())
graph = reactive.Value(nx.Graph())
seed = reactive.Value(1)
step_counter = reactive.Value(0)


class GraphType(Enum):
    RANDOM_GRAPH = "random_graph"
    KOOT_EXAMPLE_DEUTSCHLAND = "koot_example_deutschland"


def graph_ui():
    return ui.page_fluid(
        ui.layout_sidebar(
            ui.sidebar(
                ui.input_selectize(
                    "selectize_graph",
                    "Select a Graph",
                    {GraphType.RANDOM_GRAPH.value: "Random Graph",
                     GraphType.KOOT_EXAMPLE_DEUTSCHLAND.value: "Deutschland Beispiel"},
                    selected=GraphType.KOOT_EXAMPLE_DEUTSCHLAND.value
                ),
                ui.output_ui("random_graph_sliders"),
                ui.input_numeric("start_node", "Start Node", value=0, min=0),
                ui.input_numeric("target_node", "Target Node", value=1, min=0),
                ui.input_numeric("layout_seed", "Layout Seed", value=1, min=0),
            ),
            ui.input_action_button("next_step", "Next Step"),
            ui.output_plot("graph_plot"),
            ui.output_data_frame("display_distances"),
            djikstra_explanation
        ),
    )


def reset_df():
    print("reset_df")
    G = graph.get()
    if G:
        if "label" in G.nodes[0]:
            nodes = dict(sorted(nx.get_node_attributes(G, "label").items())).values()
            index_name = "Cities"
        else:
            nodes = [str(node) for node in G.nodes]
            index_name = "Node"

        distance_matrix = pd.DataFrame(float('inf'), index=nodes, columns=nodes)
        distance_matrix.index.name = index_name
        distance_matrix.reset_index(inplace=True)
        distances_df.set(distance_matrix)
        step_counter.set(0)


def init_df():
    print("init df")
    reset_df()


def graph_ui_server(input, output, session):
    @reactive.Effect
    @reactive.event(input.next_step)
    def next_step():
        print("next step")
        df = distances_df.get()
        if not df.empty:
            start_node = input.start_node()
            if 0 <= start_node < len(df):
                df.iloc[start_node, start_node + 1] = 0
                distances_df.set(df)
                print(f"Updated distance for node {start_node} to 1")
                step_counter.set(step_counter.get() + 1)
                # print(df)
            else:
                print(f"Invalid start node: {start_node}")

    @reactive.Effect
    def update_graph():
        if input.selectize_graph() == GraphType.RANDOM_GRAPH.value:
            graph.set(generate_random_graph(input.n_slider(), input.k_slider(), input.p_slider()))
        elif input.selectize_graph() == GraphType.KOOT_EXAMPLE_DEUTSCHLAND.value:
            graph.set(generate_koot_example())

    @output
    @render.data_frame
    @reactive.event(distances_df, step_counter, input.start_node, input.target_node)
    def display_distances():
        df = distances_df.get()
        if df.empty or df.shape[1] < 2:
            return render.DataGrid(df)

        return render.DataGrid(
            df,
            styles=[
                # Bold the first column
                {
                    "cols": [0],
                    "style": {"font-weight": "bold"},
                },
                # Highlight start node green
                {
                    "rows": [input.start_node()],
                    "cols": [input.start_node() + 1],
                    "style": {"background-color": "#2ca02c"},
                },
                # Highlight target node red
                {
                    "rows": [input.target_node()],
                    "cols": [input.target_node() + 1],
                    "style": {"background-color": "#d62728"},
                },
            ]
        )

    @reactive.Effect
    @reactive.event(input.target_node, input.start_node)
    def reset_djikstra():
        print("reset djikstra")
        reset_df()


    @reactive.Effect
    def initialize_distances():
        print("update distances")
        init_df()



    @output
    @render.ui
    def random_graph_sliders():
        if input.selectize_graph() == GraphType.RANDOM_GRAPH.value:
            return ui.TagList(
                ui.input_slider("n_slider", "Number of Nodes", 2, 30, 8),
                ui.input_slider("k_slider", "K", 2, 5, 3),
                ui.input_slider("p_slider", "P", 0, 1, 0.5),
            )

    @output
    @render.plot
    @reactive.event(input.selectize_graph, graph, input.layout_seed, input.start_node, input.target_node)
    def graph_plot():
        plot_graph(graph.get(), input.start_node(), input.target_node(), input.layout_seed())
