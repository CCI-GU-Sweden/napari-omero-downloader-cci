#!/usr/bin/env bash

echo "==========================================="
echo " Installing Napari + OMERO Downloader (CCI)"
echo "==========================================="
echo

echo "Creating Conda environment 'napari'..."
conda create -n napari -c conda-forge python=3.10 napari pyqt -y
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create conda environment."
    exit 1
fi

echo
echo "Activating environment..."
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate napari

echo "Detecting OS..."
UNAME=$(uname -s)
ARCH=$(uname -m)

echo "  OS:   $UNAME"
echo "  Arch: $ARCH"
echo

ICE_URL=""

# Linux (x86_64 only)
if [[ "$UNAME" == "Linux" ]]; then
    if [[ "$ARCH" != "x86_64" ]]; then
        echo "ERROR: Only Linux x86_64 is supported for this installer."
        exit 1
    fi

    ICE_URL="https://github.com/glencoesoftware/zeroc-ice-py-linux-x86_64/releases/download/20240202/zeroc_ice-3.6.5-cp310-cp310-manylinux_2_28_x86_64.whl"

# macOS (Intel or Apple Silicon)
elif [[ "$UNAME" == "Darwin" ]]; then
    ICE_URL="https://github.com/glencoesoftware/zeroc-ice-py-macos-universal2/releases/download/20240131/zeroc_ice-3.6.5-cp310-cp310-macosx_11_0_universal2.whl"

else
    echo "ERROR: Unsupported OS: $UNAME"
    echo "This installer only supports Linux and macOS."
    exit 1
fi

echo
echo "Installing zeroc-ice:"
python -m pip install "$ICE_URL"
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install zeroc-ice."
    exit 1
fi

echo
echo "Installing napari-omero-downloader-cci..."
pip install napari-omero-downloader-cci
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install plugin."
    exit 1
fi

echo
echo "==========================================="
echo "Installation complete! Starting Napari..."
echo "==========================================="
napari
