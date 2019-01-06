from conans import ConanFile, AutoToolsBuildEnvironment, RunEnvironment, tools
import os


class PyIlmBaseConan(ConanFile):
    name = "PyIlmBase"
    description = "PyIlmBase is a high dynamic-range (HDR) image file format developed by Industrial Light & " \
                  "Magic for use in computer imaging applications."
    version = "2.2.0"
    license = "BSD"
    url = "https://github.com/jgsogo/conan-openexr.git"
    settings = "os", "compiler", "build_type", "arch"
    generators = "pkg_config", "virtualenv"
    exports = "*.tar.gz"

    def requirements(self):
        self.requires('IlmBase/2.2.0@aswf/vfx2018')
        self.requires('boost/1.61.0@aswf/vfx2018')

    def source(self):
        base = "pyilmbase-{version}.tar.gz".format(version=self.version)
        if os.path.exists(base):
            self.output.info("Found local source tarball {}".format(base))
            tools.unzip(base)
        else:
            url = "http://download.savannah.nongnu.org/releases/openexr/" + base
            self.output.warn("Downloading source tarball {}".format(url))
            tools.get(url)

    def build(self):
        args = ["--enable-shared",
                "--enable-namespaceversioning",
        ]
        autotools = AutoToolsBuildEnvironment(self)
        # LD_LIBRARY_PATH is needed by the configure script to find libHalf
        with tools.environment_append(RunEnvironment(self).vars):
            autotools.configure(configure_dir='pyilmbase-{}'.format(self.version), args=args)
        autotools.make()
        tools.replace_prefix_in_pc_file("PyIlmBase.pc", "${package_root_path_pyilmbase}")

    def package(self):
        autotools = AutoToolsBuildEnvironment(self)
        autotools.install(args=['-j1'])
        self.copy("license*", dst="licenses", src="ilmbase-%s" % self.version, ignore_case=True, keep_path=False)

    def package_info(self):
        self.env_info.PYTHONPATH.append(os.path.join(self.package_folder, 'lib64/python2.7/site-packages'))
        self.cpp_info.includedirs = ['include', os.path.join('include', 'OpenEXR')]
        self.cpp_info.libs = ['PyImath', 'Pylex']
