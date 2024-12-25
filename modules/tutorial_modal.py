from pathlib import Path

from shiny import reactive, ui, render

directory = Path("./images").resolve()


def tutorial_modal():
    return ui.input_action_button("tutorial", "Tutorial"),


def tutorial_modal_server(input, output, session):
    @reactive.effect
    @reactive.event(input.tutorial)
    def show_important_message():
        m = ui.modal(

            ui.h4("Step 1"),
            ui.output_ui("select_grap_image"),

            "You start by choosing a graph from the following options:", ui.br(),

            ui.accordion(
                ui.accordion_panel("Germany Example", "A simple example with some german cities."),
                ui.accordion_panel("Random Graph",
                                   "This works by generating a connected Watts–Strogatz small-world graph.", ui.br(),
                                   "You can tweak the parameters using the sliders."
                                   ),
                ui.accordion_panel("Import from Edgelist",
                                   "This lets you create you own graph by defining a edge list.", ui.br(),
                                   ui.p(),
                                   "An edge is the connection between nodes. You can create edges by defining a tuple with three integers for example:",
                                   ui.br(),
                                   "(0, 1, 10)", ui.br(),
                                   "This will create a connection between nodes 0 and 1 with a distance of 10.", ui.br(),
                                   ui.p(),
                                   "Create multiple edges by separating each tuple with a ','.", ui.br(),
                                   "Make sure that all of the network is connected and there are no loose nodes or multiple unconnected graphs!",
                                   ui.br(),
                                   "Nodes that do not exist yet will be automatically created."
                                   )
            ),

            ui.hr(),
            ui.h4("Step 2"),
            ui.output_ui("start_targe_seed_image"),
            "After choosing a graph you can select the start and the target node.", ui.br(),
            "The Dijkstra's algorithm will then try to find the fastest path from the start node to the target node.",
            ui.br(),
            "If you want to change the layout of you graph you simply need to change the layout seed until you find a good looking layout.",
            ui.hr(),
            ui.h4("Step 3"),
            ui.output_ui("prev_next_image", height="100%", width="100%"),
            "To see each the algorithm do its work press the next step button. Each step will also be explained on the card below.",
            ui.br(),
            "If you like to look at a previous step, simply press the previous step button.", ui.br(),
            "During this time you can follow what the algorithm already figured out by looking at the distances between nodes table or the visited nodes card.",
            ui.hr(),
            ui.h4("Step 4"),
            "After the algorithm is done it will highlight the fastest way possible for you on the graph and you.",
            ui.br(),
            "At that point you can either go back with the previous step button and review the steps again or start over with a new graph.",
            title="The Dijkstra Algorithm",
            easy_close=True,
            footer=None,
            size='l'
        )
        ui.modal_show(m)

    @render.ui
    def select_grap_image():
        return ui.tags.img(
            src="https://cdn.discordapp.com/attachments/1321459358768304158/1321459404792659988/select_graph.png?ex=676d5079&is=676bfef9&hm=03fb3f3b5104c7eb00a0bd81b136412d7640bdd333aef32239026424956ab2d7&",
            width="80%")

    @render.ui
    def start_targe_seed_image():
        return ui.tags.img(
            src="https://cdn.discordapp.com/attachments/1321459358768304158/1321459405199380551/start_target_seed.png?ex=676d5079&is=676bfef9&hm=97078623fe9fee7ec57e90766127d736a41421d32f7d75da1419d6c3fad6d3fe&",
            width="40%")

    @render.ui
    def prev_next_image():
        return ui.tags.img(
            src="https://cdn.discordapp.com/attachments/1321459358768304158/1321459404557520957/prev_next.png?ex=676d5079&is=676bfef9&hm=5e17398f1f24117237dc203241c84b3793ce51960944c3d9d8eecf302769d083&",
            width="100%")
