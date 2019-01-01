from conans import ConanFile, AutoToolsBuildEnvironment, RunEnvironment, tools
import os


class OpenEXRConan(ConanFile):
    name = "OpenEXR"
    description = "OpenEXR is a high dynamic-range (HDR) image file format developed by Industrial Light & " \
                  "Magic for use in computer imaging applications."
    version = "2.2.0"
    license = "BSD"
    url = "https://github.com/jgsogo/conan-openexr.git"
    settings = "os", "compiler", "build_type", "arch"
    generators = "pkg_config", "virtualenv"
    exports = "*.tar.gz"

    def requirements(self):
        self.requires('IlmBase/2.2.0@aswf/vfx2018')

    def source(self):
        base = "openexr-{version}.tar.gz".format(version=self.version)
        if os.path.exists(base):
            self.output.info("Found local source tarball {}".format(base))
            tools.unzip(base)
        else:
            self.output.warn("Downloading source tarball {}".format(base))
            tools.get("http://download.savannah.nongnu.org/releases/openexr/" + base)

    def build(self):
        args = ["--enable-shared",
                "--enable-namespaceversioning",
        ]
        autotools = AutoToolsBuildEnvironment(self)
        # LD_LIBRARY_PATH is needed by the configure script to find libHalf
        with tools.environment_append(RunEnvironment(self).vars):
            # To fix another configure error when checking for libz
            with tools.environment_append({'LDFLAGS': '-lpthread'}):
                autotools.configure(configure_dir='openexr-{}'.format(self.version), args=args)
        autotools.make()
        tools.replace_prefix_in_pc_file("OpenEXR.pc", "${package_root_path_openexr}")

    def package(self):
        autotools = AutoToolsBuildEnvironment(self)
        autotools.install()
        self.copy("license*", dst="licenses", src="ilmbase-%s" % self.version, ignore_case=True, keep_path=False)

    def package_info(self):
        self.cpp_info.includedirs = ['include', os.path.join('include', 'OpenEXR')]
        self.cpp_info.libs = ['IlmImf', 'IlmImfUtil']

        if self.settings.os == "Windows":
            self.cpp_info.defines.append("OPENEXR_DLL")
