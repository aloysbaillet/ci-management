
import os, glob

from conans import ConanFile, tools, AutoToolsBuildEnvironment


class IlmBaseConan(ConanFile):
    name = "IlmBase"
    description = "IlmBase is a component of OpenEXR. OpenEXR is a high dynamic-range (HDR) image file format developed by Industrial Light & Magic for use in computer imaging applications."
    version = "2.2.0"
    license = "BSD"
    url = "https://github.com/Mikayex/conan-ilmbase.git"
    settings = "os", "compiler", "build_type", "arch", "cppstd"
    generators = "cmake"
    exports = "*.tar.gz"

    def source(self):
        base = "ilmbase-{version}.tar.gz".format(version=self.version)
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
        autotools.configure(configure_dir='ilmbase-{}'.format(self.version), args=args)
        autotools.make()
        tools.replace_prefix_in_pc_file("IlmBase.pc", "${package_root_path_ilmbase}")

    def package(self):
        autotools = AutoToolsBuildEnvironment(self)
        autotools.install()
        self.copy("license*", dst="licenses", src="ilmbase-%s" % self.version, ignore_case=True, keep_path=False)

        for f in glob.glob(os.path.join(self.package_folder, 'lib', '*.la')):
            os.remove(f)

    def package_info(self):
        self.cpp_info.includedirs = ['include', os.path.join('include', 'OpenEXR')]
        self.cpp_info.libs = ['Half', 'Iex', 'IexMath', 'IlmThread', 'Imath']

        if self.settings.os == "Windows":
            self.cpp_info.defines.append("OPENEXR_DLL")

        if not self.settings.os == "Windows":
            self.cpp_info.cppflags = ["-pthread"]
