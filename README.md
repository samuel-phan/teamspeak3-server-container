# Description

This project builds an RPM for TeamSpeak 3 Server on CentOS 7. It relies on Docker container.

TeamSpeak 3 Server container: https://github.com/docker-library/docs/tree/master/teamspeak/

# Requirements

Since dependencies aren't not trivial to install, they are not put as dependencies inside the RPM file, but you need to
install them before using this TeamSpeak service:

- docker-ce (tested on version 18.06.1-ce)
- docker-compose (tested on version 1.22.0)

# How to build the RPM

## Python 3 requirements

You must have a Python 3 interpreter, and install the requirements:

```
pip3 install -r requirements.txt
```

## Build the Docker image with rpmbuild

You need to build first the Docker image containing the binary `rpmbuild`:

```
inv build-rpmbuild-img
```

## Build the RPM file

Run:

```
inv clean build-rpm
```

The RPM file is in the `dist` directory.
