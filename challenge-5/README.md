# Challenge 5: Helm Chart

## Preparation

As we want the helm chart to be installable by default we need to make sure that our container image is available in some kind of container registry. Therefore we have modified the Dockerfile of challenge-3 and added a LABEL as noted in the official docs of GitHub (see https://docs.github.com/en/packages/learn-github-packages/connecting-a-repository-to-a-package#connecting-a-repository-to-a-container-image-using-the-command-line):

```sh
LABEL org.opencontainers.image.source=https://github.com/ef8619-or/interview-homework-challenge-sre
```

After we have rebuilt our image we need to add a new tag to our image so that docker push needs to know where to correctly push our image to the GitHub container registry:

```sh
docker tag orcrist-challenge-3 ghcr.io/ef8619-or/orcrist-challenge-3:latest
```

In the final step of our preparation we login in to the GitHub container registry with our personal GitHub Token which we created and push the image:

```sh
export CR_PAT=<Token>
echo $CR_PAT | docker login ghcr.io -u ef8619-or --password-stdin
docker push ghcr.io/ef8619-or/orcrist-challenge-3:latest
```

I have decided to change the visibility of the package in the GitHub container registry to public as it doesn't contain any critical or sensitive information. Thus we don't need to add `imagePullSecret` to our deployment. 

Now we are able to really use the image in our helm chart so that it can pull the container image from the registry.

## Helm Chart

Please take a look at `deployment.yaml`, `service.yaml` and `_helpers.tpl` in the templates directory. A detailed explanation in this README of why I did the things as they are would be too long. This is more suitable as a subject in an interview. I decided to use a _helpers.tpl as it gives us the convenience to standardize and re-use common elements like fullname, labels, selectLabels and so on.

The `values.yaml`file in the root directory of challenge-5 contains all neccessary values which are needed for helm to render the chart correctly.

## Verficiation of the solution

Now that we have completed creating the helm chart we have to proof that everything is working as it should.

### Helm lint

We execute the following command in the shell:

```sh
helm lint ./server-chart
```

which gives us following response:

```sh
==> Linting ./server-chart
[INFO] Chart.yaml: icon is recommended

1 chart(s) linted, 0 chart(s) failed
```

Great, linting was done without any errors.

### Helm template

Before we are going to install the helm chart into our cluster we want it to be rendered and with the values from values.yaml and take a look at it. So we execute:

```sh
helm template ./server-chart
```

This is what we get:

```sh
---
# Source: server-chart/templates/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: release-name-server-chart
  labels:
    helm.sh/chart: server-chart
    app.kubernetes.io/name: server-chart
    app.kubernetes.io/instance: release-name
    server-chart/version: "0.1.0"
spec:
  type: ClusterIP
  ports:
    - port: 80
      targetPort: 8080
      protocol: TCP
      name: http
  selector:
    app.kubernetes.io/name: server-chart
    app.kubernetes.io/instance: release-name
---
# Source: server-chart/templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: release-name-server-chart
  labels:
    helm.sh/chart: server-chart
    app.kubernetes.io/name: server-chart
    app.kubernetes.io/instance: release-name
    server-chart/version: "0.1.0"
spec:
  replicas: 1
  selector:
    matchLabels:
      app.kubernetes.io/name: server-chart
      app.kubernetes.io/instance: release-name
  template:
    metadata:
      labels:
        helm.sh/chart: server-chart
        app.kubernetes.io/name: server-chart
        app.kubernetes.io/instance: release-name
        server-chart/version: "0.1.0"
    spec:
      containers:
        - name: server-chart
          image: "ghcr.io/ef8619-or/orcrist-challenge-3:latest"
          imagePullPolicy: Always
          ports:
            - containerPort: 8080
              name: http
          resources:
            requests:
              cpu: 5m
              memory: 128Mi
            limits:
              cpu: 500m
              memory: 512Mi
```

Great, Helm did not give us any errors and when we have a look at the result everything seems to be fine.

### Helm install

Of course we want to install our freshly created helm chart into our cluster. Therefore we are going to use the great tool #k3d# (see: https://k3d.io/stable/#what-is-k3d). k3d gives us the possibility to spin up a fully working k3s cluster with the help of docker containers in an eyeblink.

We will not go into detail on how to install k3d. We are using a Mac M4 paltform and installed it with brew.

So we create a little cluster as following:

```sh
k3d cluster create orcrist
```

This spins up a cluster called orcrist. We can check the clusters and nodes as following:

```sh
k3d cluster ls
```

We get:

```sh
NAME      SERVERS   AGENTS   LOADBALANCER
orcrist   1/1       0/0      true
```

Next we check the nodes:

```sh
k3d node ls
```

This outputs:

```sh
k3d-orcrist-server-0   server         orcrist   running
k3d-orcrist-serverlb   loadbalancer   orcrist   running
k3d-orcrist-tools                     orcrist   running
```

Nice, everything is up and running. Time to go ahead and create a namespace where we want to install our chart into:

```sh
kubectl create namespace challenge-5
```

Finally we can now deploy our application into this freshly created namespace with Helm:

```sh
helm install challenge-5 ./server-chart -n challenge-5
```

Helm confirms the successful installation with:

```sh
NAME: challenge-5
LAST DEPLOYED: Wed Apr 29 19:47:00 2026
NAMESPACE: challenge-5
STATUS: deployed
REVISION: 1
TEST SUITE: None
```

## Testing if everything works

First we want to make sure that our pod is up and running, so we check:

```sh
kubectl get pods -n challenge-5
```

The output is:

```sh
NAME                                        READY   STATUS    RESTARTS   AGE
challenge-5-server-chart-647684d94d-xkpb5   1/1     Running   0          2m15s
```

Next we want to take a look at the services in the challenge-5 namespace:

```sh
kubectl get svc -n challenge-5
```

The result is:

```sh
NAME                       TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)   AGE
challenge-5-server-chart   ClusterIP   10.43.167.84   <none>        80/TCP    3m22s
```

As we can see our pod is running and we have a service of type ClusterIP which listens on port 80.

To be able to test our application we need to do portforwarding of our service in the cluster to our localhost:

```sh
kubectl port-forward svc/challenge-5-server-chart -n challenge-5 9091:80
```

Our terminal session will now be blocked as long as the port forwarding is active. The output begins with:

```sh
Forwarding from 127.0.0.1:9091 -> 8080
Forwarding from [::1]:9091 -> 8080
...
```

Why port 9091? we have no permission to use port 80. Instead we used a port which is more distinct from commonly used ports and decided to take 9091.

The last step is to test if the service routes the traffic to the pod so we can execute a simple cURL command (as we know from challenge-3 we should use a specific header to get a HTTP status code of 200):

```sh
curl -i -H "Challenge: orcrist.org" -X GET http://localhost:9091
```

And voilà we get a nice looking reponse:

```sh
HTTP/1.0 200 OK
Server: SimpleHTTP/0.6 Python/3.14.4
Date: Wed, 29 Apr 2026 17:56:24 GMT
Content-type: text/html

Everything works!%
```