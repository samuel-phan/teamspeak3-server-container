FROM centos:7

USER root
RUN yum install -y rpm-build rpmdevtools sudo

RUN mkdir /rpmbuild
VOLUME ["/rpmbuild"]

COPY sudo-as-user.sh /usr/local/bin/sudo-as-user.sh

RUN yum clean all

ENTRYPOINT ["/usr/local/bin/sudo-as-user.sh"]
CMD ["rpmbuild", "--define", "_topdir /rpmbuild", "-ba", "/rpmbuild/SPECS/teamspeak3-server-container.spec"]
