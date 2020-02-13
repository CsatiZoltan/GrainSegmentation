# GrainSegmentation

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
   If you want to remove the environment you have just created, type
   ```bash
   conda remove --name imagepy --all
   ```
   When the installation is done, you can start *ImagePy* with `python -m imagepy`.



## Full installation

Since both *ImagePy* and *ImageJ* are needed for a good segmentation result, it is recommended to install both.

1. Install Conda and Python 3 (Anaconda already ships them)
2. Install Java
3. Activate the conda-forge channel
   ```bash
   conda config --add channels conda-forge
   conda config --set channel_priority strict
   ```
4. Download or clone the *ImagePy* repository
   ```bash
   git clone git://github.com/Image-Py/imagepy
   cd imagepy
   ```
5. Copy the `environment.yml` from **this** repository to the root of the previously downloaded *ImagePy* repository, overwriting the existing file. This file essentially contains the dependencies both for *ImagePy* and for *pyimagej*. It was created by first installing *pyimagej*, then issuing `conda env export > environment.yml`, finally inserting the *ImagePy* dependencies to this file and changing the name of the environment to *imagepy+pyimagej*.
6. Install *pyimagej* and the dependencies of *ImagePy* to an isolated environment, and then activate the newly created environment
   ```bash
   conda env create
   conda activate imagepy+pyimagej
   ```
7. Install *ImagePy* to this new environment
   ```
   python setup.py install
   ```
   The following commands must both give a non-empty output
   ```bash
   conda list | grep "imagepy"
   conda list | grep "pyimagej"
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



### Other problems

If you have other problems using these tools, [open an issue](https://github.com/CsatiZoltan/GrainSegmentation/issues/new) on GitHub after reading the [existing ones](https://github.com/CsatiZoltan/GrainSegmentation/issues).