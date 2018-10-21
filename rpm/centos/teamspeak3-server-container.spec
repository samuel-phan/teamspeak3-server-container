%global version %(cat /rpmbuild/SPECS/teamspeak3-server-container.version)
%{?systemd_requires}

Name:           teamspeak3-server-container
Version:        %{version}
Release:        1%{?dist}
Summary:        TeamSpeak server in a container
License:        MIT
URL:            https://github.com/samuel-phan/teamspeak-server-container
Source0:        %{name}-%{version}.tar.gz

BuildArch:      x86_64

BuildRequires: systemd

%description
Run a TeamSpeak server in a Docker container.
Requires docker and docker-compose, but since docker-ce and docker-compose have specific ways to be installed, they are
not listed as Requires in the RPM.

%prep
%setup -n %{name}-%{version}

%build

%install
mkdir -p %{buildroot}/opt/teamspeak3-server
install -m 644 docker-compose/teamspeak.yml %{buildroot}/opt/teamspeak3-server

mkdir -p %{buildroot}/usr/lib/systemd/system
install -m 644 systemd/teamspeak.service %{buildroot}/usr/lib/systemd/system

mkdir -p %{buildroot}/usr/lib/systemd/system-preset
install -m 644 systemd/90-teamspeak.preset %{buildroot}/usr/lib/systemd/system-preset

mkdir -p %{buildroot}/var/local/ts3server

%post

%systemd_post teamspeak.service

%preun
%systemd_preun teamspeak.service

%check

%files
/opt/teamspeak3-server
/usr/lib/systemd/system/teamspeak.service
/usr/lib/systemd/system-preset/90-teamspeak.preset
/var/local/ts3server

%changelog
* Sun Oct 21 2018 Samuel Phan <samuel@quoonel.com> 0.0.1
- Initial package
