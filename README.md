# DS in the Wild Project: Pokemon Card Identification

[Initial Proposal: Google Slides](https://docs.google.com/presentation/d/1t7WQ5hytdsKvZk0Yyzdm0pFz0CW3NU4ZImZ9vTHxLuE/edit?usp=sharing)

## Setup

```sh
# Install Poetry
$ curl -sSL https://install.python-poetry.org | python3 -
# Install dependencies
$ poetry install
# Download datasets
$ poetry run setup
```

If setup fails, make sure you have accepted the invite to `haydendaly/ds-poke-shared` which contains a dataset.

### Classification (CGC Only)

If you are also working on the classification CGC only project, you can run:

```sh
$ poetry run update-cgc
```

Which clones the images / labels from the `haydendaly/ds-poke-shared-cgc` repo.

## Usage

### Jupyter

You can start a Jupyter notebook server with:

```sh
$ poetry run notebook
```

This will add the `Pokemon Identification` kernel to Jupyter and open up `localhost:8888` for Jupyter hub. As a result, you will be able to access the up-to-date dependencies and local modules. You can alternatively use the kernel in VSCode.

This will run in its own terminal and you can `CTRL-C` it to stop the server.

### Lint

```sh
$ poetry run lint
```

## Directory Hierarchy

The project is broken into different modules which export the methods / variables specified in the respective `__init__.py` files. Goal is to have `*.py` files act as modules (ex: `src.shared` contains the exports of `src.shared.dataset` and all other files it contains).

## K8s

```
minikube start
```

Apply the generated Kubernetes configuration files:

```
kubectl apply -f k8s/namespace/namespace.yaml
kubectl apply -f k8s/zookeeper/zookeeper.yaml
kubectl apply -f k8s/kafka/kafka.yaml
kubectl apply -f k8s/postgres/postgres.yaml
kubectl apply -f k8s/redis/redis.yaml
kubectl apply -f k8s/market/market.yaml
kubectl apply -f k8s/details/details.yaml
kubectl apply -f k8s/images/images.yaml
```

Verify the deployments, services, and pods are running:

```
kubectl get deployments -n poke-namespace
kubectl get services -n poke-namespace
kubectl get pods -n poke-namespace
```

Access logs of a specific pod:

```
kubectl logs -f <pod-name> -n poke-namespace
```

- Exec into a specific pod:

```
kubectl exec -it <pod-name> -n poke-namespace -- /bin/bash
```

Update the deployments by applying the updated configuration files:

```
kubectl apply -f k8s/<service-name>/<service-name>.yaml
```

Delete the deployments and services:

```
kubectl delete -f k8s/<service-name>/<service-name>.yaml
```

Scale the deployment:

```
kubectl scale deployment <deployment-name> -n poke-namespace --replicas=<number-of-replicas>
```
