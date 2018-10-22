import os
from pathlib import Path

from invoke import task


PROJECT_DIR = Path(__file__).parent
VERSION_FILE = PROJECT_DIR / 'version'

with open(VERSION_FILE) as fh:
    VERSION = fh.read().strip()

BUILD_DIR = PROJECT_DIR / 'build'
SOURCE_DIR = BUILD_DIR / '{}-{}'.format(PROJECT_DIR.name, VERSION)
SOURCE_TARBALL = BUILD_DIR / '{}.tar.gz'.format(SOURCE_DIR.name)

DIST_DIR = PROJECT_DIR / 'dist'

DOCKER_DIR = PROJECT_DIR / 'docker'
DOCKER_COMMON_DIR = DOCKER_DIR / 'common'
RPMBUILD_IMG_NAME = 'centos7-rpmbuild'
RPMBUILD_IMG_DIR = DOCKER_DIR / RPMBUILD_IMG_NAME


@task(help={'dest': 'destination directory of the archive. Default: {}'.format(BUILD_DIR.name)})
def build_src(ctx, dest=None):
    """
    build source archive
    """
    ctx.run('mkdir -p {}'.format(SOURCE_DIR))

    # Copy files
    for f in (PROJECT_DIR / 'docker-compose',
              PROJECT_DIR / 'systemd'):
        ctx.run('cp -r {} {}'.format(f, SOURCE_DIR))

    # Build the tarball
    with ctx.cd(str(BUILD_DIR)):
        ctx.run('tar -cvzf {} {}'.format(SOURCE_TARBALL, SOURCE_DIR.name))

    if dest:
        ctx.run('mv -f {} {}'.format(SOURCE_TARBALL, dest))


@task
def build_rpm(ctx):
    """
    build an RPM package
    """
    rpmbuild_dir = DIST_DIR / 'rpmbuild'

    # Create directories layout
    ctx.run('mkdir -p {}'.format(' '.join(str(rpmbuild_dir / d)
                                          for d in ('BUILD', 'RPMS', 'SOURCES', 'SPECS', 'SRPMS'))))

    # Copy the sources & spec file
    build_src(ctx, dest=rpmbuild_dir / 'SOURCES')
    ctx.run('cp -f {} {}'.format(PROJECT_DIR / 'rpm/centos/teamspeak3-server-container.spec', rpmbuild_dir / 'SPECS'))
    ctx.run('cp -f {} {}'.format(VERSION_FILE, rpmbuild_dir / 'SPECS/teamspeak3-server-container.version'))

    # Build the RPM
    ctx.run('docker run -e LOCAL_USER_ID={local_user_id} -v {local}:{cont} {img}'
            .format(local_user_id=os.getuid(),
                    local=rpmbuild_dir,
                    cont='/rpmbuild',
                    img=RPMBUILD_IMG_NAME))

    ctx.run('mv -f {} {}'.format(rpmbuild_dir / 'RPMS/x86_64/teamspeak3-server-container-{}-*.rpm'.format(VERSION),
                                 DIST_DIR))


@task
def build_rpmbuild_img(ctx):
    """
    build docker image for rpmbuild on CentOS 7
    """
    ctx.run('docker rmi -f {0}'.format(RPMBUILD_IMG_NAME), warn=True)

    rpmbuild_img_build_dir = BUILD_DIR / RPMBUILD_IMG_NAME
    ctx.run('mkdir -p {}'.format(rpmbuild_img_build_dir))
    ctx.run('cp -r {} {} {}'.format(RPMBUILD_IMG_DIR / '*',
                                    DOCKER_COMMON_DIR / 'sudo-as-user.sh',
                                    rpmbuild_img_build_dir))
    ctx.run('docker build -t {} {}'.format(RPMBUILD_IMG_NAME, rpmbuild_img_build_dir))


@task
def clean(ctx):
    """
    clean generated project files
    """
    patterns = [BUILD_DIR.name,
                DIST_DIR.name]
    with ctx.cd(str(PROJECT_DIR)):
        ctx.run('rm -vrf {0}'.format(' '.join(patterns)))
