import platform
import subprocess
import sys

from napari.utils.notifications import show_error, show_info
from qtpy.QtWidgets import QMessageBox


def ask_user_yes_no(title, text):
    """Show a modal Yes/No dialog. Return True if Yes."""
    mbox = QMessageBox()
    mbox.setWindowTitle(title)
    mbox.setText(text)
    mbox.setIcon(QMessageBox.Question)
    mbox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    mbox.setDefaultButton(QMessageBox.Yes)
    return mbox.exec_() == QMessageBox.Yes


def install_ice_wheel():
    osname = platform.system()
    pyver = f"{sys.version_info.major}.{sys.version_info.minor}"

    wheel_url = None

    # Window
    if osname == "Windows":
        wheels = {
            "3.8": "https://github.com/glencoesoftware/zeroc-ice-py-win-x86_64/releases/download/20240325/zeroc_ice-3.6.5-cp38-cp38-win_amd64.whl",
            "3.9": "https://github.com/glencoesoftware/zeroc-ice-py-win-x86_64/releases/download/20240325/zeroc_ice-3.6.5-cp39-cp39-win_amd64.whl",
            "3.10": "https://github.com/glencoesoftware/zeroc-ice-py-win-x86_64/releases/download/20240325/zeroc_ice-3.6.5-cp310-cp310-win_amd64.whl",
            "3.11": "https://github.com/glencoesoftware/zeroc-ice-py-win-x86_64/releases/download/20240325/zeroc_ice-3.6.5-cp311-cp311-win_amd64.whl",
            "3.12": "https://github.com/glencoesoftware/zeroc-ice-py-win-x86_64/releases/download/20240325/zeroc_ice-3.6.5-cp312-cp312-win_amd64.whl",
        }
        wheel_url = wheels.get(pyver)
    # Linux
    elif osname == "Linux":
        wheels = {
            "3.8": "https://github.com/glencoesoftware/zeroc-ice-py-linux-x86_64/releases/download/20240202/zeroc_ice-3.6.5-cp38-cp38-manylinux_2_28_x86_64.whl",
            "3.9": "https://github.com/glencoesoftware/zeroc-ice-py-linux-x86_64/releases/download/20240202/zeroc_ice-3.6.5-cp39-cp39-manylinux_2_28_x86_64.whl",
            "3.10": "https://github.com/glencoesoftware/zeroc-ice-py-linux-x86_64/releases/download/20240202/zeroc_ice-3.6.5-cp310-cp310-manylinux_2_28_x86_64.whl",
            "3.11": "https://github.com/glencoesoftware/zeroc-ice-py-linux-x86_64/releases/download/20240202/zeroc_ice-3.6.5-cp311-cp311-manylinux_2_28_x86_64.whl",
            "3.12": "https://github.com/glencoesoftware/zeroc-ice-py-linux-x86_64/releases/download/20240202/zeroc_ice-3.6.5-cp312-cp312-manylinux_2_28_x86_64.whl",
        }
        wheel_url = wheels.get(pyver)

    elif osname == "Darwin":
        wheels = {
            "3.8": "https://github.com/glencoesoftware/zeroc-ice-py-macos-x86_64/releases/download/20231130/zeroc_ice-3.6.5-cp39-cp39-macosx_11_0_x86_64.whl",
            "3.9": "https://github.com/glencoesoftware/zeroc-ice-py-macos-x86_64/releases/download/20231130/zeroc_ice-3.6.5-cp39-cp39-macosx_11_0_x86_64.whl",
            "3.10": "https://github.com/glencoesoftware/zeroc-ice-py-macos-universal2/releases/download/20240131/zeroc_ice-3.6.5-cp310-cp310-macosx_11_0_universal2.whl",
            "3.11": "https://github.com/glencoesoftware/zeroc-ice-py-macos-universal2/releases/download/20240131/zeroc_ice-3.6.5-cp311-cp311-macosx_11_0_universal2.whl",
            "3.12": "https://github.com/glencoesoftware/zeroc-ice-py-macos-universal2/releases/download/20240131/zeroc_ice-3.6.5-cp312-cp312-macosx_11_0_universal2.whl",
        }
        wheel_url = wheels.get(pyver)

    if wheel_url is None:
        show_error(
            "Unsupported OS/Python combo for automatic Ice installation."
        )
        return

    # ask the user first
    if not ask_user_yes_no(
        "Install Ice (zeroc-ice)?",
        f"Ice is required for OMERO support.\n\n"
        f"Do you want to install the following package?\n\n{wheel_url}",
    ):
        show_error("Installation cancelled. OMERO features will not work.")
        return

    # install it
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", wheel_url]
        )
        show_info("Ice installed successfully.")
    except subprocess.CalledProcessError as e:
        show_error(
            "Failed to install Ice (pip exited with a non-zero status).\n"
            f"Command: {' '.join(e.cmd)}\n"
            f"Return code: {e.returncode}"
        )
    except OSError as e:
        show_error(f"Failed to run pip to install Ice:\n{e}")


def install_omeropy():
    if not ask_user_yes_no(
        "Install OMERO-PY?",
        "OMERO-PY is required to connect to the OMERO server.\n\n"
        "Do you want to install OMERO-PY 5.21.2 now?",
    ):
        show_error("OMERO installation cancelled.")
        return

    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "omero-py==5.21.2"]
        )
        show_info("OMERO installed successfully.")
    except subprocess.CalledProcessError as e:
        show_error(
            "Failed to install OMERO (pip exited with a non-zero status).\n"
            f"Command: {' '.join(e.cmd)}\n"
            f"Return code: {e.returncode}"
        )
    except OSError as e:
        show_error(f"Failed to run pip to install OMERO:\n{e}")
