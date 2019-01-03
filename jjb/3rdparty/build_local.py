import subprocess
import argparse
import sys
import os
from contextlib import contextmanager

PACKAGES = ['boost',
            'IlmBase',
            'OpenEXR',
            'PyIlmBase',
            'TBB']

def host_call(cmd):
    print('+ %s'%cmd)
    return subprocess.check_call(cmd, shell=True)

def docker_call(cmd, cmds):
    cmds.append(cmd)

def start_server():
    repoRoot = os.path.abspath(os.path.join(os.path.curdir, '..', '..'))
    host_call('docker network create --driver bridge conan_network')        
    host_call('docker run '
              '--network=conan_network '
              '--detach -p 9300:9300 '
              '-v %s/conan/server:/root/.conan_server '
              '--name local_conan_server '
              'conanio/conan_server:latest'%repoRoot)

def stop_server():
    subprocess.call('docker stop local_conan_server', shell=True)
    subprocess.call('docker rm --force local_conan_server', shell=True)
    subprocess.call('docker network rm conan_network', shell=True)
    subprocess.call('docker rm --force conan_builder', shell=True)

@contextmanager
def managed_docker(args):
    try:
        if args.remote == 'local_server':
            try:
                start_server()
            except subprocess.CalledProcessError:
                stop_server()
                start_server()
        yield None
    finally:
        if args.remote == 'local_server':
            stop_server()

def main():
    parser = argparse.ArgumentParser(description='Build script')
    parser.add_argument('--no-ssl-verify', '-ns', action='store_true', help='Disable SSL cert verify on remotes.')
    parser.add_argument('--upload', '-up', action='store_true', help='Upload package after successful build.')
    parser.add_argument('--remote', '-r', help='Remote name for upload. Use "local_server" to start a local conan server. '
                        'No need for username/password with local_server.')
    parser.add_argument('--username', '-u', help='Username for upload to remote.')
    parser.add_argument('--password', '-p', help='Password or API Key for upload to remote.')
    parser.add_argument('packages', nargs='*', help='Package names to build, builds all if not specified', )
    args = parser.parse_args()

    cmds = []
    docker_call('conan remote add aswftest https://api.bintray.com/conan/aloysbaillet/aswftest %r'%(not args.no_ssl_verify), cmds)
    
    if args.remote == 'local_server':
        docker_call('conan remote add local_server http://local_conan_server:9300 False', cmds)
        docker_call('conan user local_user -p local_password -r=local_server', cmds)
    else:
        if args.upload:
            docker_call('conan user %s -p %s -r=%s'%(args.username, args.password, args.remote), cmds)

    if args.no_ssl_verify:
        docker_call('conan remote update conan-center https://conan.bintray.com False', cmds)

    for pkg in args.packages or PACKAGES:
        docker_call('conan create /tmp/vfx-build/%s aswf/vfx2018'%pkg, cmds)
    
        if args.upload:
            docker_call('conan upload %s/*@aswf/vfx2018 --force --confirm --all -r=%s'%(pkg, args.remote), cmds)

    with managed_docker(args):
        print('Docker calls:\n' + '\n- '.join(cmds))
        build = ' && '.join(cmds)
        if args.remote == 'local_server':
            net = '--network=conan_network '
        else:
            net = ''
        host_call('docker run '
                  + net +
                  '-v $(pwd):/tmp/vfx-build '
                  '--name conan_builder '
                  'aloysbaillet/aswf-vfx2018-conan '
                  '/bin/bash -c "%s"'%build)

    return 0


if __name__ == "__main__":
    sys.exit(main())
