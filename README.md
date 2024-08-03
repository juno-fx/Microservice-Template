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

## Development Workflow

> **NOTE** This is untested on Windows


### Enter the devbox environment

Enter your devbox environment. This will install all required packages and then install and build your 
python environment.

```bash
devbox shell
```

> For more information, feel free to take a look at the [devbox documentation](https://www.jetify.com/devbox/docs/).

> We completely automate the entire process of installing `kind`, `kubectl`, `docker`, ` python`, `uv`, and build your 
> development environment for you using devbox.

### Start the development environment

Then, simply launch the dev environment using the following command:

```bash
make dev
```

This will launch the `myapp` microservice in a local Kubernetes cluster using [kind](https://kind.sigs.k8s.io/). 
You can access the service at: [http://localhost:8000/docs](http://localhost:8000/docs).

### Stop the development environment

To stop the development environment, first press `ctrl + c`.

### Clean Up

Simply closing out the development environment will not delete the cluster itself. To do that, make sure to run the following:

```bash
make down
```

This will shut down the local Kubernetes cluster and remove all resources.

### Exit the devbox environment
To exit the devbox environment, simply press `ctrl + d` or run the following command:

```bash
exit
```


### Testing Luna

Let's take a look at how we test one of our core microservices, `Luna`.

#### Dependencies

* **`Mongo Database`** - This is the database that `Luna` uses. We also need to launch this.
* **`Titan Microservice`** - Titan is used for authorization in the cluster and `Luna` uses it to validate user requests from `jfx-luna`.
* **`Mars Microservice`** - Finally, we have `Mars Microservice` which is used to manage the file system. `Luna` uses this to manage the files in the Luna project.

Once again, mocking all of these services would be a nightmare. This time we are using a FastAPI test client to run our
tests.

```mermaid
graph TD;
    skaffold[Skaffold Verify]
    subgraph Kind[Kind Cluster]
        subgraph s[Skaffold Deployment]
            subgraph l[Luna Test Env]
                Luna[Luna Server]
                Mongo
                Mars
                Titan
            end
            subgraph luna-runner[Internal Cluster Luna Tests]
                coverage
                pytest
                luna[FastAPI Test Client]
                luna-int[requests Test Client]
            end
            
            coverage --> pytest
            pytest --> luna
            pytest --> luna-int
            luna-int -->|Luna Server Tests| Luna
            luna -->|Internal Tests| Mongo
            Luna -.- Mongo
            Luna -.- Titan
            Luna -.- Mars
        end
    end
    
    subgraph luna-external-runner[External Cluster Luna Tests]
        coverage-ext[coverage]
        pytest-ext[pytest]
        luna-ext[requests Test Client]
    end
    
    coverage-ext --> pytest-ext
    pytest-ext --> luna-ext
    luna-ext -->|External Tests| Luna
    
    skaffold -.- luna-runner
    skaffold -.- luna-external-runner

```

The above graph seems complex, but we are actually testing 3 major use cases for `Luna`:

1. **Utility Endpoint Tests** - These are tests that test the utility endpoints of `Luna`. These are endpoints that are
   used internally by `jfx-luna` and other services.
2. **Direct Database Tests** - These are tests that test the direct database access of `Luna`. These are tests that
   directly interact with the database and simulate how `Luna` itself functions internally.
3. **External Endpoint Tests** - These are tests that test the external endpoints of `Luna`. These are endpoints that
   are exposed to external services and are the main way that `Luna` interacts with the outside world.

All 3 of these test environments would be difficult to test and mock if we didn't have the ability to launch a real
instance of `Luna` in our testing environment.
