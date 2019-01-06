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
