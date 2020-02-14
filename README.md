# Grain segmentation

[![Join the chat at https://gitter.im/Grain-Segmentation/community](https://badges.gitter.im/Grain-Segmentation/community.svg)](https://gitter.im/Grain-Segmentation/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Identification of individual grains in microscopic images



### Contents

- [Purpose](#purpose)
- [Dependencies](#dependencies)
- [Installation](#installation)
   - [*pyimagej*](#installing-pyimagej)
   - [*ImagePy*](#installing-ImagePy)
   - [full installation](#full-installation)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)



## Purpose



## Dependencies

Depending on the features you want to use, the requirements are different:
1. Image segmentation algorithms
   The only requirements are Python 3 with the following packages:
   - scipy
   - numpy
   - scikit-image (a.k.a. skimage)
2. Use *ImagePy* for manual corrections
   - [additional packages](https://github.com/Image-Py/imagepy/blob/master/requirements.txt)
   - the [source code of *ImagePy*](https://github.com/Image-Py/imagepy) itself
   - [Conda](https://conda.io/en/latest/) (only if you want to install it to an isolated environment)
3. Use algorithms from *ImageJ*/*Fiji*
To call the functions of *ImageJ* from within Python, the [pyimagej](https://imagej.net/Python) connector is used. Its dependencies:
   - Conda (not necessary but highly recommended)
   - [additional packages](https://github.com/imagej/pyimagej/blob/master/environment.yml)



## Installation

To use the algorithms, no installation is needed. Just keep the files [grain_segmentation.py](https://github.com/CsatiZoltan/GrainSegmentation/blob/master/src/grain_segmentation.py) and [gala_light.py](https://github.com/CsatiZoltan/GrainSegmentation/blob/master/src/gala_light.py), found in the [src/](https://github.com/CsatiZoltan/GrainSegmentation/tree/master/src) directory, together.



### Installing *pyimagej*

**Note**: it is important that you first install *pyimagej* and not *ImagePy* because *pyimagej* has several requirements on the versions of the Python packages and on Python as well. If you want both *pyimagej* and *ImagePy*, rather follow the [full installation guide](#full-installation).
If you want to use *ImageJ*, you need to have Java installed (OpenJDK 8 is recommended).
Check the Java versions installed on your machine:

```bash
update-java-alternatives --list
```
You can now install *pyimagej* following the official [installation instructions](https://github.com/imagej/pyimagej#installation).



### Installing *ImagePy*

1. For Windows, there is a [standalone package](https://github.com/Image-Py/imagepy/releases/download/v0.2/ImagePy-64.rar) (quite an old version)
2. You can install *ImagePy* with pip: `pip install imagepy`. To install it from your current Python environment, use `python -m pip install imagepy`.
3. If you want the latest version, download the source:
   ```bash
   git clone git://github.com/Image-Py/imagepy
   cd imagepy
   ```
   You can now choose to install it to the current Python environment or create a separate environment for it. In the first case, just type
   ```bash
   python setup.py install
   ```
   If you want an isolated environment, use conda before installing:
   ```bash
   conda env create # creates the "imagepy" environment
   conda activate imagepy
   python setup.py install
   ```
4. To check whether *ImagePy* is recognized:
   ```bash
    conda list | grep "imagepy"
   ```
   When the installation is done, you can start *ImagePy* with `python -m imagepy`.

If you want to remove the environment you have just created, type
```bash
conda remove --name imagepy --all
```



## Full installation

Since both *ImagePy* and *ImageJ* are needed for a good segmentation result, it is recommended to install both.

1. Install Conda and Python 3 (Anaconda already ships them)
2. Install Java
3. Activate the conda-forge channel
   ```bash
   conda config --add channels conda-forge
   conda config --set channel_priority strict
   ```
4. Install *pyimagej* and those requirements for *ImagePy* that can be fetched from conda-forge. We create an isolated environment so that it does not interfere with our existing Python installation.
   ```bash
   conda create -n combined pyimagej openjdk=8 numba numpy-stl openpyxl pandas pydicom pypubsub read-roi scikit-image scikit-learn shapely wxpython xlrd xlwt markdown python-markdown-math moderngl
   ```
5. Activate the new environment, called *combined*. This is important so that *ImagePy* is installed there.
   ```
   conda activate combined
   ```
6. We will use pip to install the remaining required packages for *ImagePy*, which couldn't be obtained from conda-forge
   ```bash
   python -m pip install pystackreg
   ```
7. Download and install *ImagePy*
   ```bash
   git clone https://github.com/Image-Py/imagepy
   cd imagepy
   python setup.py install
   ```
8. The following commands must both give a non-empty output
   ```bash
   conda list | grep "imagepy"
   conda list | grep "pyimagej"
   ```
9. Delete the *ImagePy* folder. We don't need it any more and we want to avoid accidentally launching *ImagePy* from here.
   ```bash
   cd ..
   rm -r imagepy/
   ```



## Usage



## Troubleshooting

### `imagej.init()` throws an error

If you choose to use *pyimagej*, check if the environment variable JAVA_HOME is found on your path
```bash
printenv | grep JAVA_HOME
```
If you get no result, set JAVA_HOME to `/usr/lib/jvm/java-8-openjdk-amd64/` (or something similar). To do so, edit the environment variable
   - from the [shell](https://stackoverflow.com/a/39691105/4892892) (or put it into `.bashrc` to make it permanent):
      ```bash
      export JAVA_HOME="/usr/lib/jvm/java-8-openjdk-amd64/"
      export PATH=$PATH:$JAVA_HOME/bin
      ```
   - from within you Python session:
      ```python
      import os
      os.environ['JAVA_HOME'] = '/usr/lib/jvm/java-8-openjdk-amd64/'
      ```

If
```python
import imagej
ij = imagej.init()
```
throws no error, *pyimagej* work properly on your machine.



### Getting help

If you have other problems using these tools, [open an issue](https://github.com/CsatiZoltan/GrainSegmentation/issues/new) on GitHub after reading the [existing ones](https://github.com/CsatiZoltan/GrainSegmentation/issues) or discuss it on [Gitter](https://gitter.im/Grain-Segmentation/community).



## Contributing

Contributions to this open source project are welcome.

### How can you contribute?

- Send a pull request
- Discuss ideas on [Gitter](https://gitter.im/Grain-Segmentation/community)

### What can you help in?
- Suggestions for improved segmentation algorithms
  This is the most important aspect.
- Improve the documentation
  Let me know about typos and inconsistencies in the documentation (this README file, comments in the source code).
- Improve the *ImagePy* integration
  As I am new to *ImagePy*, suggestions are definitely welcome. Those who are new to *ImagePy*, the best sources are the
  - [official page](https://github.com/Image-Py/imagepy)
  - [detailed tutorial](https://github.com/Image-Py/demoplugin) on how to write *ImagePy* plugins
  - [image.sc forum](https://forum.image.sc/tag/imagepy), where you can find tutorials and can ask questions