# Pokénet 👾

Visualize Pokémon evolution chains as a network. The below network shows all
Pokémon of the third generation.

![Pokénet](.data/pokenet.gif)

## Installation

In order to install the project, `python = "^3.11"` is necessary. To set up
your environment simply type

```shell
poetry install
```

## Usage

Currently, there are two options to generate a network. Either call the main
class `PokeNet` from the command line or from a `Python` script.

### Python 🐍

To generate the above network (without Pokémon pictures as nodes), create a 
new `Python` script with the following content.

```python
from pokenet import PokeNet

n = PokeNet()
n.create_network(pokemon_generation=3)
n.save_network()
```

Note: `create_network()` has a parameter `pokemon_pics_path` which allows to
add Pokémon pictures as nodes. However, the pictures are not provided in this
repository. Fortunately, there exist a lot of image datasets on the internet
(for example this one [here](https://www.kaggle.com/datasets/kvpratama/pokemon-images-dataset?resource=download)).

### Command Line Interface 👨‍💻

In order to retrieve the same network as above, simply type:

```shell
pokenet --pokemon-generation 3
```

For more information on the CLI:
    
```shell
pokenet --help
```

# Resources

The creation of the node data wouldn't have been possible without the 
work of [veekun](https://github.com/veekun/pokedex/blob/master/).
