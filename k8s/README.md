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
