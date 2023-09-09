from pathlib import Path

import polars as pl
import pytest
from pyvis.network import Network

from pokenet import PokeNet


class TestPokeNet:
    @pytest.fixture(scope="class")
    def net(self) -> PokeNet:
        return PokeNet()

    def test_init(self, net):
        assert isinstance(net.node_data, pl.DataFrame)
        assert net.net is None

    def test_create_network(self, net):
        """Just check if a network was created."""
        net.create_network(pokemon_generation=1)
        assert isinstance(net.net, Network)

        net.create_network(pokemon_generation=None)
        assert isinstance(net.net, Network)

    def test_save_network(self, net):
        output_path = Path("test/test.html")
        net.save_network(output_path=output_path, overwrite=False)
        assert output_path.exists()

        # try to save again
        with pytest.raises(FileExistsError):
            net.save_network(output_path=output_path, overwrite=False)

        # remove file
        output_path.unlink()
