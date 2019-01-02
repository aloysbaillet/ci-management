import subprocess

if __name__ == "__main__":
    #subprocess.check_call('docker build -t aloysbaillet/aswf-vfx2018-conan -f Dockerfile_vfx2018 .', shell=True, cwd='../../../conan')

    build = '''
conan user demo -p demo -r=local_server
conan create /tmp/vfx-build/openexr aswf/vfx2018 &&\
conan upload OpenEXR/2.2.0@aswf/vfx2018 --all -r=local_server
'''
    subprocess.check_call('docker run --network="host" -v $(pwd):/tmp/vfx-build/openexr --rm aloysbaillet/aswf-vfx2018-conan /bin/bash -c "%s"'%build, shell=True)
