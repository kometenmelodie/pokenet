from pathlib import Path
from typing import Union

import polars as pl
import typer
from pyvis.network import Network
from typing_extensions import Annotated


class PokeNet:
    """Create a network graph of Pokémon evolution chains.

    :param node_data_path: Path to node data file.
    """

    def __init__(self, node_data_path: Path = Path(".data/node_data.csv")):
        self.node_data = pl.read_csv(node_data_path)
        self.net = None

    def create_network(
        self, pokemon_generation: int | None = 2, pokemon_pics_path: str | None = None
    ):
        """Initialize and draw the network graph.

        :param pokemon_generation: Plot a specific Pokémon generation.
        :param pokemon_pics_path: Path to Pokémon pictures which are used as nodes.
        """
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

    def save_network(
        self, output_path: Path = Path("graph.html"), overwrite: bool = False
    ):
        """Save the network graph to a html file.

        :param output_path: Path to save the network graph to.
        :param overwrite: Whether to overwrite existing file.
        """
        if output_path.exists() and not overwrite:
            raise FileExistsError(
                f"File {output_path} already exists."
                "Set overwrite=True to overwrite it."
            )
        else:
            self.net.save_graph(str(output_path))
            print(f"Saved network to {output_path}.")


def _cli_network(
    node_data_path: Annotated[
        str, typer.Argument(help="Path to node data file.")
    ] = ".data/node_data.csv",
    output_path: Annotated[
        str, typer.Argument(help="Network output file.")
    ] = "graph.html",
    pokemon_generation: Annotated[
        Union[int, None], typer.Option(help="Plot a specific Pokémon generation.")
    ] = None,
    pokemon_pics_path: Annotated[
        Union[str, None],
        typer.Option(help="Path to Pokémon pictures which are used as nodes."),
    ] = None,
    overwrite: Annotated[
        bool, typer.Option(help="Whether to overwrite existing file.")
    ] = False,
):
    """CLI to create a network graph of Pokémon evolution chains."""

    network = PokeNet(node_data_path=Path(node_data_path))
    network.create_network(
        pokemon_generation=pokemon_generation, pokemon_pics_path=pokemon_pics_path
    )
    network.save_network(output_path=Path(output_path), overwrite=overwrite)


def cli_network():
    typer.run(_cli_network)
