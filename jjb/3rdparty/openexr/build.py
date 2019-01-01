import subprocess

if __name__ == "__main__":
    subprocess.check_call('docker build -t aswf/vfx2018-builder -f Dockerfile_vfx2018 .', shell=True, cwd='../../../conan')

    build = '''
conan create /tmp/vfx-build/openexr aswf/vfx2018 &&\
conan upload OpenEXR/2.2.0@aswf/vfx2018 --all -r=my_local_server
'''
    subprocess.check_call('docker run -v $(pwd):/tmp/vfx-build/openexr --rm aswf/vfx2018-builder /bin/bash -c "%s"'%build, shell=True)
