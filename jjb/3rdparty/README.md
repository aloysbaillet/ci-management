# Third Party Packages

This set of jenkins jobs to build binaries for VFX Platform packages that are required to build ASWF packages.

All builds are based on a minimal VFX Platform compliant docker image.

## Conan

This is using [conan.io] to build and retrieve dependencies.

### Conan Recipes

If there is an existing recipe to build a package found in the https://github.com/conan-community account then it is copied via a squashed subtree under the `jjp/3rdparty`
folder where it can be patched sustainably.

All build options are kept but the default options are updated to match the general expectations of the VFX Platform.

### Conan Settings

The conan settings for the platform are found in the `conan/config/settings.yml` and have the following additions compared to the default conan settings:
* `Linux: version: [None, rhel6, rhel7]`
which allows the indirect selection of the libc version and a set of system-level dependencies that do not belong here.

### Building packages against VFX Platform dependencies

For *end-users* of these conan packages you have to manually install Conan via pip: [Conan Install](https://docs.conan.io/en/latest/installation.html#install-with-pip-recommended) on a CentOS-7 machine.
You also need to have devtoolset-6 installed and activated [VFX Plaform Compiler](https://www.vfxplatform.com/#footnote-gcc6)
You probably want to also have a recent version of CMake installed [CMake](https://cmake.org/download/)

Once conan is installed you need to run the `conan config install THIS_REPO_CONAN_CONFIG_FOLDER` where THIS_REPO_CONAN_CONFIG_FOLDER is the `conan/config` folder of this github repository. 
This will install the right conan platform settings and install a profile called vfx2018 to use when building packages.

Finally you can create a file called `conanfile.txt` where you define the VFX platform packages required by your program and the generators you want to use, then run 
`mkdir build && cd build && conan install ..` to download all dependencies and allow you to build your program. See conan documentation there: [Conan](https://docs.conan.io/en/latest/getting_started.html)


## Jenkins Jobs

All jobs are named 3rdparty-X-vfx2018 where X is a third-party package for which we need binaries available.

Use the regular `jenkins-jobs update jjb/` script to upload the jobs to the jenkins sandbox.


## Local testing

In order to test these docker builds locally the `build_local.py` script can be used to build all 3rdparty packages in the right order
and with the right dependencies, the only requirement is a linux machine with docker installed.

To build all using a local conan server (running within docker as well):
`python build_local.py -r local_server`

To build a single package using a local conan server (running within docker as well):
`python build_local.py -r local_server OpenEXR`

To avoid having to re-download source packages at each build, you can manually download the .tar.gz files and place them alongside their corresponding `conanfile.py` and it will be used instead of re-downloading.
