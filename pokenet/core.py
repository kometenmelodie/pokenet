from pathlib import Path

import polars as pl
from pyvis.network import Network


class PokeNet:
    def __init__(self, node_data_path: Path = Path(".data/node_data.csv")):
        self.node_data = pl.read_csv(node_data_path)
        self.net = None

    def create_network(self, generation: int | None = 2):
        # initialize network
        net = Network(
            height="900px", bgcolor="black", font_color="white", filter_menu=False
        )
        # filter self.node_data by generation
        if generation is not None:
            net_data = self.node_data.filter(pl.col("generation_id") == generation)
        else:
            net_data = self.node_data

        for pokemon in net_data.rows(named=True):
            # add source node
            net.add_node(
                pokemon["source_node"], title=pokemon["source_node"], color="white"
            )
            # add target node
            net.add_node(
                pokemon["target_node"], title=pokemon["target_node"], color="white"
            )
            # add edge
            net.add_edge(
                pokemon["source_node"], pokemon["target_node"], value=1.5, color="white"
            )

        self.net = net

    def save_network(self, path: Path = Path("graph.html"), overwrite: bool = False):
        if path.exists() and not overwrite:
            raise FileExistsError(
                f"File {path} already exists." "Set overwrite=True to overwrite it."
            )
        else:
            self.net.save_graph(str(path))
            print(f"Saved network to {path}.")
