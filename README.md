<br />
<p align="center">
    <img src="/Microservice.png"/>
    <h3 align="center">Microservice Template</h3>
    <p align="center">
        Microservice Template Repository from Juno Innovations
    </p>
</p>

## Usage

This is a template repository for creating new microservices at Juno Innovations. It is designed to be the 
easiest jumping off point for creating new microservices for kubernetes.

## Pre-requisites

The following tools are required to be installed on your machine to use this repository:

- [devbox](https://www.jetify.com/devbox) - Development environment tooling

We have streamlined the development process for microservices at Juno Innovations by using devbox to automate the
installation of all required tools and dependencies.

## Development

> **NOTE** This is untested on Windows

Following the standard Juno micro service structure, Mercury is built using the following technologies

- [devbox](https://www.jetify.com/devbox) - Development environment tooling

Firstly, enter your devbox env. This will install all required packages.

```bash
devbox shell
```

Then, simply launch the dev environment using the following command:

```bash
make dev
```

This will launch the Mercury microservice in a local Kubernetes cluster using kind. You can then access the service at
[http://localhost:8000/mercury/docs](http://localhost:8000/mercury/docs).

To stop the development environment, first press `ctrl + c` and then run the following command:

```bash
make down
```

This will shut down the local Kubernetes cluster and remove all resources.

To exit the devbox environment, simply run the following command:

```bash
exit
```
