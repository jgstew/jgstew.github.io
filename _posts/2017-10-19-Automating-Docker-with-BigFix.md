**Note:** this is an overview for a presentation I gave at a BigFix User Group.

![Docker Logo](https://camo.githubusercontent.com/3482fc32e1f4cad0c44039c8f01e1e270e6894ee/687474703a2f2f692e696d6775722e636f6d2f4b6764574c64682e706e67)

## Docker

- A lightweight alternative to VMs
- Each Docker Container has access to all resources

## Setup Docker Host

There are tons of options for Docker Hosts, but in this case, a Linux OS that supports BigFix specifically is best if BigFix is going to manage it, though privileged containers may provide another option for BigFix Management of a Docker Host.

- [Install Ubuntu](https://forum.bigfix.com/t/thin-imaging-and-installing-the-bigfix-agent/15750)
  - Kickstart file
- [Install BigFix](https://github.com/jgstew/tools/blob/master/bash/install_bigfix.sh)
- [Install Docker](https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/)
  - Fixlets
  - [Baseline](https://github.com/jgstew/bigfix-content/blob/master/baselines/Docker%20Setup%20-%20Ubuntu.bes)

![Baseline: Docker Setup](http://jgstew.github.io/images/BFAutomatingDocker/DockerSetupBaseline.png)

## Use Docker Host

This particular use case refers to OS containers only, and specifically those which can run the BigFix client. Any container could work, but if it can't run BigFix, then it would require a proxy agent to appear in the console.

- Create Docker [Containers](https://github.com/jgstew/tools/blob/master/bash/docker_bigfix_client.sh)
- Create Docker [Images](https://github.com/jgstew/tools/blob/master/docker/Dockerfiles/bigfix_ubuntu/Dockerfile) -> Containers
- Create Many Containers with Docker Compose

## Analize Docker Host & Containers

Most info for Docker Containers is stored as JSON on the Docker Host, which BigFix can read.

- [Analyses](https://github.com/jgstew/bigfix-content/blob/master/analyses/Docker%20Host%20Info%20-%20Linux.bes)
- Automatic Groups


## Related:

- https://forum.bigfix.com/t/bay-area-bigfix-user-group-october-19th-2017-emeryville-ca/22323
- https://forum.bigfix.com/t/thin-imaging-and-installing-the-bigfix-agent/15750
- https://github.com/jgstew/tools/blob/master/bash/install_bigfix.sh
- https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/
- https://docs.docker.com/engine/reference/run/
