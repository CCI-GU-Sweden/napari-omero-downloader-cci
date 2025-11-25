# napari-omero-downloader-cci

[![License MIT](https://img.shields.io/pypi/l/napari-omero-downloader-cci.svg?color=green)](https://github.com/CCI-GU-Sweden/napari-omero-downloader-cci/raw/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/napari-omero-downloader-cci.svg?color=green)](https://pypi.org/project/napari-omero-downloader-cci)
[![Python Version](https://img.shields.io/pypi/pyversions/napari-omero-downloader-cci.svg?color=green)](https://python.org)
[![tests](https://github.com/CCI-GU-Sweden/napari-omero-downloader-cci/workflows/tests/badge.svg)](https://github.com/CCI-GU-Sweden/napari-omero-downloader-cci/actions)
[![napari hub](https://img.shields.io/endpoint?url=https://api.napari-hub.org/shields/napari-omero-downloader-cci)](https://napari-hub.org/plugins/napari-omero-downloader-cci)
[![npe2](https://img.shields.io/badge/plugin-npe2-blue?link=https://napari.org/stable/plugins/index.html)](https://napari.org/stable/plugins/index.html)
[![Copier](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-purple.json)](https://github.com/copier-org/copier)

A plugin that allows napari to connect to the Omero CCI server to visualize and download image data.

---

## Contents

- [Installation](#installation)
- [Plugin function](#plugin)
- [Troubleshooting](#troubleshooting)

---

## Installation

## Standalone napari

A standalone version of napari is available at [napari.org](https://napari.org/dev/tutorials/fundamentals/installation_bundle_conda.html), and the plugin is available on the [napari hub](https://napari-hub.org/plugins/napari-omero-downloader-cci.html). Just follow the installation instruction from napari, then you can install the plugin from the [plugin manager](#plugin-installation).

Only work from version v0.3.8 and upward.

## Via Conda Forge

### First napari installation

First install miniconda from conda forge: [https://conda-forge.org/download/]. This is mandatory!

Recommanded, create an environment for napari, bundling both napari and omero.

```shell
conda create -n napari -c conda-forge napari pyqt --yes
conda activate napari
napari
```

Or you can download from [my github repo](https://github.com/CCI-GU-Sweden/napari-omero-downloader-cci/tree/main/scripts) the install_napari_omero (bat for window, sh for Mac/Linux). This will also install the plugin!

**Note:** conda-forge does *not* provide OMERO-py or ICE bindings for Python ≥3.10.
When installing the plugin via pip, the plugin will install its own OMERO + Ice wheels.
This is normal and expected.

### Plugin installation

You can install the plugin through the napari plugin manager: Plugins -> Install/Uninstall Plugins.. -> search for 'omero'.

![napari plugin](https://raw.githubusercontent.com/CCI-GU-Sweden/napari-omero-downloader-cci/main/assets/napari_omero.png)

The plugin is named Omero Downloader CCI.

Or you can install `napari-omero-downloader-cci` via [pip]:

```shell
pip install napari-omero-downloader-cci
```

This will automatically install:

- the correct **zeroc-ice** wheel for your OS and Python version
- **omero-py 5.21.2**
- Qt (via napari)
- all plugin dependencies

No conda required.

To install latest development version :

```shell
pip install git+https://github.com/CCI-GU-Sweden/napari-omero-downloader-cci.git
```

— or, during development —

```shell
pip install -e .
```

For power user, the option to install the plugin **without** the dependencies:

```shell
pip install --no-deps napari-omero-downloader-cci
```

Dependency list:

- [dask](https://pypi.org/project/dask/) - to display images
- [numpy](https://pypi.org/project/numpy/) - to display images
- [qtpy](https://pypi.org/project/QtPy/) – abstraction layer for Qt (used by napari).
  A Qt backend (PyQt / PySide) is installed automatically with napari.
- [zeroc-ice wheel based on your system](https://github.com/glencoesoftware) for the connection handling
- [omero-py](https://pypi.org/project/omero-py/) version 5.21.2

Napari is also required, but not in the dependency.

Python version support locked by zeroc-ice: from 3.8 to 3.12.

### Python version support

This plugin supports **Python 3.8 – 3.12**, matching the available zeroc-ice wheels by Glencoe Software.
Newer Python versions will be supported once Glencoe publishes corresponding wheels.

## Running the plugin after Installation

The easy step: download from [my github repo](https://github.com/CCI-GU-Sweden/napari-omero-downloader-cci/tree/main/scripts) the start_napari (bat for window, sh for Mac/Linux) and run it. It should open python, activate the env then run napari (can take 10-30 seconds the first time!)

Otherwise, open the conda-forge CLI, then:

```shell
conda activate napari
napari
```

The plug will be in the plugin tab.

![plugin](https://raw.githubusercontent.com/CCI-GU-Sweden/napari-omero-downloader-cci/main/assets/plugin.png)

## Plugin

The plugin requires that you have access to Omero with the following features:

- CLI enable
- OAuth enable (2FA token)

### Why this plugin?

Another solution outside of this plugin is available: omero.insight ([openmicroscopy website](https://www.openmicroscopy.org/omero/downloads/)), as well as a FiJi plugin.

However, they do not fullfill the prerequiste at the CCI: A simple tool to quickly visualize and download data while being secure with 2FA.

### Login

In 'Options...', indicate the omero server address and port. The default is the one for the CCI at the University of Gothenburg.

![options](https://raw.githubusercontent.com/CCI-GU-Sweden/napari-omero-downloader-cci/main/assets/options.png)

Click on the link, login on Omero and grab a key. This key is valid only for a certain amount of time and for this session. Generating a new key, or closing your session (via the 'Disconnect') will invalidate the key.

Enter the key in the field and click on 'Connect'.

![login](https://raw.githubusercontent.com/CCI-GU-Sweden/napari-omero-downloader-cci/main/assets/login.png)

The square next to the connect button is indicating the connection status:

- Red: not connected
- Yellow: busy
- Green: ready

### Groups and users

If you are part of multiple group, you can change group with the drop down menu. If your Omero administrator allows it, you can also see the data of other people in the same group. If data are being imported on the Omero server, you may need to refresh the visualization to be able to see them.

### Queuing data for download

The data will be organized as a hierachical tree. Project -> Database -> Image.

Clicking on the arrow allow you to reveal the contained data.

Double click to add the element in the 'Download Queue'. Double clicking on a project will queue the whole project. Same for a dataset. However, double clicking on one image will download only this image.

There is a color on the 'OMERO Data' as well:

- Green: will download all the child of the element
- Yellow: will partially download the child of the element

You can remove an element by double clicking on it in the 'Download queue'.

![trees](https://raw.githubusercontent.com/CCI-GU-Sweden/napari-omero-downloader-cci/main/assets/tree.png)

### Data Visualization

It is possible to visualize the selected data (in the 'OMERO Data' tree) by clicking on the 'Visualize' button. This will download and display only one plane (first time point, middle of stack in case of multi-dimensional image). It is possible to scroll the data, but keep in mind that this is streamed from the Omero server. Do not expect high performance specially if the image is large!

![visualize](https://raw.githubusercontent.com/CCI-GU-Sweden/napari-omero-downloader-cci/main/assets/visualize.png)

### Data Downloading

To download the data that are queued, select a directory to save them (with the 'Browse...' button) then it the 'Download' button.

The data will be organized in a similar way that they are on the Omero server. If you have a key-value pair called 'Folder' associated to an image, the image will be nested on level deeper, in this folder.

In option, if download attachement and key-value pair is enable, these files will also be downloaded alongside the image.

![progressbar](https://raw.githubusercontent.com/CCI-GU-Sweden/napari-omero-downloader-cci/main/assets/progressbar.png)

![folder](https://raw.githubusercontent.com/CCI-GU-Sweden/napari-omero-downloader-cci/main/assets/folder.png)

### Data deletion

This napari plugin is **NOT** allowed to delete data on the Omero server. If you need to delete data, you should do it via Omero.web.

## Troubleshooting

### ❌ "No Qt bindings found"

Install napari with Qt:

```bash
pip install "napari[qt]"
```

### ❌ "Cannot import Ice"

This means the correct zeroc-ice wheel was not installed.
Check your Python version (3.8–3.12) and OS match the supported versions. Search for the correct wheel on [Glencoe](https://github.com/glencoesoftware), then you can install them with (for example):

```bash
pip install @ "zeroc-ice @ https://github.com/glencoesoftware/zeroc-ice-py-win-x86_64/releases/download/20240325/zeroc_ice-3.6.5-cp38-cp38-win_amd64.whl"
```

### ❌ "Cannot import omero"

Ensure the plugin was installed normally:

```bash
pip install napari-omero-downloader-cci
```

If needed, force the reinstall of omero for the correct version:

```bash
pip install --upgrade "omero-py == 5.21.2"
```

## Contributing

Contributions are very welcome. Tests can be run with [tox], please ensure
the coverage at least stays the same before you submit a pull request.

## License

Distributed under the terms of the [MIT] license,
"napari-omero-downloader-cci" is free and open source software

## Issues

If you encounter any problems, please [file an issue] along with a detailed description.

[MIT]: http://opensource.org/licenses/MIT
[file an issue]: https://github.com/CCI-GU-Sweden/napari-omero-downloader-cci/issues
[tox]: https://tox.readthedocs.io/en/latest/
[pip]: https://pypi.org/project/pip/
