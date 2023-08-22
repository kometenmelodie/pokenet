from pathlib import Path

import polars as pl
from pyvis.network import Network


class PokeNet:
    def __init__(self, node_data_path: Path = Path(".data/node_data.csv")):
        self.node_data = pl.read_csv(node_data_path)
        self.net = None

    def create_network(
        self, pokemon_generation: int | None = 2, pokemon_pics_path: str | None = None
    ):
        # initialize network
        net = Network(
            height="900px", bgcolor="black", font_color="white", filter_menu=False
        )
        # filter self.node_data by Pokémon generation
        if pokemon_generation is not None:
            net_data = self.node_data.filter(
                pl.col("generation_id") == pokemon_generation
            )
        else:
            net_data = self.node_data

        for pokemon in net_data.rows(named=True):
            source_node = pokemon["source_node"]
            target_node = pokemon["target_node"]

            if pokemon_pics_path is None:
                # add source node
                net.add_node(source_node, title=source_node, color="white")
                # add target node
                net.add_node(target_node, title=target_node, color="white")
            else:
                source_id = pokemon["source_id"]
                target_id = pokemon["target_id"]

                # add pictures of Pokémon as nodes
                net.add_node(
                    source_node,
                    title=source_node,
                    shape="image",
                    image=f"{pokemon_pics_path}/{source_id}.png",
                )
                net.add_node(
                    target_node,
                    title=target_node,
                    shape="image",
                    image=f"{pokemon_pics_path}/{target_id}.png",
                )
            # add edge
            net.add_edge(source_node, target_node, value=1.5, color="white")

        self.net = net

    def save_network(self, path: Path = Path("graph.html"), overwrite: bool = False):
        if path.exists() and not overwrite:
            raise FileExistsError(
                f"File {path} already exists." "Set overwrite=True to overwrite it."
            )
        else:
            self.net.save_graph(str(path))
            print(f"Saved network to {path}.")
