step 1
PS C:\Users\syed shah's> cd minikube-assignment
PS C:\Users\syed shah's\minikube-assignment> dir

    Directory: C:\Users\syed shah's\minikube-assignment

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----         11/5/2026   2:21 AM                app
d-----         11/5/2026   2:21 AM                k8s
d-----         11/5/2026   2:21 AM                screenshots
-a----         11/5/2026   1:01 PM              0 outputs.txt

step 2 Tools check and kubectl install 

PS C:\Users\syed shah's\minikube-assignment> git --version
git version 2.55.0.windows.5
PS C:\Users\syed shah's\minikube-assignment> docker --version
Docker version 29.8.2, build 7fc2dff
PS C:\Users\syed shah's\minikube-assignment> docker ps
CONTAINER ID   IMAGE                              COMMAND                  CREATED       STATUS        PORTS                                                                                                                                  NAMES
fc1dc05cdded   gcr.io/k8s-minikube/kicbase:v0.0.51   "/usr/local/bin/entr…"   2 weeks ago   Up 15 hours   127.0.0.1:55841->22/tcp, 127.0.0.1:55842->2376/tcp, 127.0.0.1:55839->5000/tcp, 127.0.0.1:55840->8443/tcp, 127.0.0.1:55843->32443/tcp   minikube
PS C:\Users\syed shah's\minikube-assignment> winget install -e --id Kubernetes.kubectl
Found Kubernetes CLI [Kubernetes.kubectl] Version 1.37.2
This application is licensed to you by its owner.
Microsoft is not responsible for, nor does it grant any licenses to, third-party packages.
Downloading https://dl.k8s.io/release/v1.37.2/bin/windows/amd64/kubectl.exe
  60.5 MB / 60.5 MB
Successfully verified installer hash
Starting package install...
Path environment variable modified; restart your shell to use the new value.
Command line alias added: "kubectl"
Successfully installed

PS C:\Users\syed shah's> cd minikube-assignment
PS C:\Users\syed shah's\minikube-assignment> kubectl version --client
Client Version: v1.36.1
Kustomize Version: v5.8.1

step 3 Cluster start aur cluster-info 

PS C:\Users\syed shah's\minikube-assignment> minikube start --driver=docker
* minikube v1.39.0 on Microsoft Windows 11 Home 26H2
* Using the docker driver based on existing profile
* Starting "minikube" primary control-plane node in "minikube" cluster
* Pulling base image v0.0.51 ...
* Updating the running docker "minikube" container ...
* Preparing Kubernetes v1.37.0 on containerd 2.3.4 ...
* Verifying Kubernetes components...
  - Using image gcr.io/k8s-minikube/storage-provisioner:v5
* Enabled addons: storage-provisioner, default-storageclass
* Done! kubectl is now configured to use "minikube" cluster and "default" namespace by default
PS C:\Users\syed shah's\minikube-assignment> minikube status
minikube
type: Control Plane
host: Running
kubelet: Running
apiserver: Running
kubeconfig: Configured

PS C:\Users\syed shah's\minikube-assignment> kubectl cluster-info
Kubernetes control plane is running at https://127.0.0.1:55840
CoreDNS is running at https://127.0.0.1:55840/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'

Step 4: app.py making

PS C:\Users\syed shah's\minikube-assignment> dir app

    Directory: C:\Users\syed shah's\minikube-assignment\app

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----         11/5/2026   1:17 PM            277 app.py


PS C:\Users\syed shah's\minikube-assignment> Get-Content app\app.py
from flask import Flask
import os, socket

app = Flask(__name__)

@app.route('/')
def home():
    pod = os.environ.get('POD_NAME', socket.gethostname())
    return f'<h1>Hello from pod: {pod}</h1>\n'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

tep 5: Dockerfile making 
PS C:\Users\syed shah's\minikube-assignment> Rename-Item app\Dockerfile.txt Dockerfile
PS C:\Users\syed shah's\minikube-assignment> dir app

    Directory: C:\Users\syed shah's\minikube-assignment\app

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----         11/5/2026   1:18 PM            277 app.py
-a----         11/5/2026   1:20 PM            139 Dockerfile


PS C:\Users\syed shah's\minikube-assignment> Get-Content app\Dockerfile

FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir flask

COPY app.py .

EXPOSE 8080

CMD ["python", "app.py"]

Step 6 Docker image build making

PS C:\Users\syed shah's\minikube-assignment> docker build -t pod-name-app:1.0 ./app
[+] Building 21.0s (10/10) FINISHED                                                                  docker:desktop-linux
 => [internal] load build definition from Dockerfile                                                             0.0s
 => => transferring dockerfile: 178B                                                                             0.0s
 => [internal] load metadata for docker.io/library/python:3.12-slim                                              3.4s
 => [auth] library/python:pull token for registry-1.docker.io                                                    0.0s
 => [internal] load .dockerignore                                                                                0.0s
 => => transferring context: 2B                                                                                  0.0s
 => [1/4] FROM docker.io/library/python:3.12-slim@sha256:b18b261e1b4974b4f321451ad5251ded85abb22c2b8b262da527dda1 9.0s
 => => resolve docker.io/library/python:3.12-slim@sha256:b18b261e1b4974b4f321451ad5251ded85abb22c2b8b262da527dda1 0.0s
 => => sha256:acca7542dfc736e9ce20cbefc58b2d09822276d15d4a0c531531a6f1b057928e 251B / 251B                       0.3s
 => => sha256:f574edac59d9f092df596f54e5b52656c803fd3ae30825b8ee5a189ed05f63d3 12.12MB / 12.12MB                 2.3s
 => => sha256:3eb77115150676568f88e2957181b8f7e3014e797f1ce8cd640086dfbed45e35 1.29MB / 1.29MB                   1.8s
 => => sha256:6fc242d221a673263eabd14a9ad9584d3177c96e5cb504c891497338e2f912f5 29.86MB / 29.86MB                 8.0s
 => => extracting sha256:6fc242d221a673263eabd14a9ad9584d3177c96e5cb504c891497338e2f912f5                        0.6s
 => => extracting sha256:3eb77115150676568f88e2957181b8f7e3014e797f1ce8cd640086dfbed45e35                        0.1s
 => => extracting sha256:f574edac59d9f092df596f54e5b52656c803fd3ae30825b8ee5a189ed05f63d3                        0.3s
 => => extracting sha256:acca7542dfc736e9ce20cbefc58b2d09822276d15d4a0c531531a6f1b057928e                        0.0s
 => [internal] load build context                                                                                0.0s
 => => transferring context: 312B                                                                                0.0s
 => [2/4] WORKDIR /app                                                                                           0.1s
 => [3/4] RUN pip install --no-cache-dir flask                                                                   6.8s
 => [4/4] COPY app.py .                                                                                          0.0s
 => exporting to image                                                                                           1.5s
 => => exporting layers                                                                                          0.4s
 => => exporting manifest sha256:dedf9295aa2df5395f9f5e3feaeb88f27d8363657f169db9b82cc3315209cca7                0.0s
 => => exporting config sha256:f5e2f3ace7e2aec464deed0d048e0eef4efc0a932b4a67c7ad634f9c3b64a0bd                  0.0s
 => => exporting attestation manifest sha256:62040a23eca6b315fbcb5fbd2d7b5cdbf1affcde090ae653e18d3213c46c174f    0.0s
 => => exporting manifest list sha256:ba74e46e7152d731b7e36c0121e3d5b9773e1f5578d22482c174c143566d3249           0.0s
 => => naming to docker.io/library/pod-name-app:1.0                                                              0.0s
 => => unpacking to docker.io/library/pod-name-app:1.0                                                           1.0s
PS C:\Users\syed shah's\minikube-assignment> docker images pod-name-app

IMAGE               ID             DISK USAGE   CONTENT SIZE   EXTRA
pod-name-app:1.0    ba74e46e7152        198MB         48.3MB

Step 7 loading image in minikube

PS C:\Users\syed shah's\minikube-assignment> minikube image load pod-name-app:1.0
PS C:\Users\syed shah's\minikube-assignment> minikube image ls | findstr pod-name-app
docker.io/library/pod-name-app:1.0

Step 8 make 3 Deployments 

PS C:\Users\syed shah's\minikube-assignment> dir k8s

    Directory: C:\Users\syed shah's\minikube-assignment\k8s

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----         11/5/2026   1:29 PM           1636 deployments.yaml


PS C:\Users\syed shah's\minikube-assignment> kubectl apply -f k8s/deployments.yaml
deployment.apps/app-nodeport created
deployment.apps/app-clusterip created
deployment.apps/app-loadbalancer created
PS C:\Users\syed shah's\minikube-assignment> kubectl get deployments
NAME               READY   UP-TO-DATE   AVAILABLE   AGE
app-clusterip      2/2     2            2           6s
app-loadbalancer   2/2     2            2           6s
app-nodeport       2/2     2            2           6s
PS C:\Users\syed shah's\minikube-assignment> kubectl get pods -o wide
NAME                                READY   STATUS    RESTARTS   AGE   IP            NODE       NOMINATED NODE   READINESS GATES
app-clusterip-55579cbd98-9q5mz      1/1     Running   0          13s   10.244.0.3    minikube   <none>           <none>
app-clusterip-55579cbd98-jtt7m      1/1     Running   0          13s   10.244.0.8    minikube   <none>           <none>
app-loadbalancer-7cdffb9865-cfwwm   1/1     Running   0          13s   10.244.0.6    minikube   <none>           <none>
app-loadbalancer-7cdffb9865-g7r2f   1/1     Running   0          13s   10.244.0.5    minikube   <none>           <none>
app-nodeport-5c4749dfb6-fhp6t       1/1     Running   0          13s   10.244.0.4    minikube   <none>           <none>
app-nodeport-5c4749dfb6-wb5qv       1/1     Running   0          13s   10.244.0.7    minikube   <none>           <none>

 Step 9  3Services making

PS C:\Users\syed shah's\minikube-assignment> dir k8s

    Directory: C:\Users\syed shah's\minikube-assignment\k8s

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----         11/5/2026   1:29 PM           1636 deployments.yaml
-a----         11/5/2026   1:33 PM            704 services.yaml


PS C:\Users\syed shah's\minikube-assignment> kubectl apply -f k8s/services.yaml
service/app-nodeport-svc created
service/app-clusterip-svc created
service/app-loadbalancer-svc created
PS C:\Users\syed shah's\minikube-assignment> kubectl get services
NAME                   TYPE           CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE
app-clusterip-svc      ClusterIP      10.104.214.139   <none>        80/TCP         6s
app-loadbalancer-svc   LoadBalancer   10.104.220.120   <pending>     80:30479/TCP   6s
app-nodeport-svc       NodePort       10.104.96.41     <none>        80:30080/TCP   6s
kubernetes             ClusterIP      10.96.0.1        <none>        443/TCP        19d
PS C:\Users\syed shah's\minikube-assignment> kubectl get endpoints
Warning: v1 Endpoints is deprecated in v1.33+; use discovery.k8s.io/v1 EndpointSlice
NAME                   ENDPOINTS                         AGE
app-clusterip-svc      10.244.0.3:8080,10.244.0.8:8080   14s
app-loadbalancer-svc   10.244.0.5:8080,10.244.0.6:8080   14s
app-nodeport-svc       10.244.0.4:8080,10.244.0.7:8080   14s
kubernetes             192.168.49.2:8443                 19d

Step 10: ClusterIP  demo 

PS C:\Users\syed shah's\minikube-assignment> kubectl get svc app-clusterip-svc
NAME                TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)   AGE
app-clusterip-svc   ClusterIP   10.104.214.139   <none>        80/TCP    99s
PS C:\Users\syed shah's\minikube-assignment> curl.exe --max-time 5 http://10.104.214.139
curl: (28) Connection timed out after 5005 milliseconds
PS C:\Users\syed shah's\minikube-assignment> kubectl run curl-test --rm -it --image=curlimages/curl --restart=Never -- curl -s http://app-clusterip-svc
<h1>Hello from pod: app-clusterip-55579cbd98-jtt7m</h1>
All commands and output from this session will be recorded in container logs, including credentials and sensitive information passed through the command prompt.
If you don't see a command prompt, try pressing enter.
warning: couldn't attach to pod/curl-test, falling back to streaming logs: Internal error occurred: Internal error occurred: error attaching to container: container is in CONTAINER_EXITED state
<h1>Hello from pod: app-clusterip-55579cbd98-jtt7m</h1>
pod "curl-test" deleted from default namespace
PS C:\Users\syed shah's\minikube-assignment> kubectl run curl-test --rm -it --image=curlimages/curl --restart=Never -- curl -s http://app-clusterip-svc
All commands and output from this session will be recorded in container logs, including credentials and sensitive information passed through the command prompt.
If you don't see a command prompt, try pressing enter.
Session ended, resume using 'kubectl attach curl-test -c curl-test -n default -i -t' command
pod "curl-test" deleted from default namespace
PS C:\Users\syed shah's\minikube-assignment> kubectl run curl-test --rm -it --image=curlimages/curl --restart=Never -- curl -s http://app-clusterip-svc
<h1>Hello from pod: app-clusterip-55579cbd98-9q5mz</h1>
All commands and output from this session will be recorded in container logs, including credentials and sensitive information passed through the command prompt.
If you don't see a command prompt, try pressing enter.
warning: couldn't attach to pod/curl-test, falling back to streaming logs: unable to open upgrade connection: container curl-test not found in pod curl-test_default
<h1>Hello from pod: app-clusterip-55579cbd98-9q5mz</h1>
pod "curl-test" deleted from default namespace

Step 11: NodePort  demo 

PS C:\Users\syed shah's\minikube-assignment> kubectl run curl-test --rm -i --image=curlimages/curl --restart=Never -- curl -s http://app-nodeport-svc
<h1>Hello from pod: app-nodeport-5c4749dfb6-wb5qv</h1>
All commands and output from this session will be recorded in container logs, including credentials and sensitive information passed through the command prompt.
If you don't see a command prompt, try pressing enter.
warning: couldn't attach to pod/curl-test, falling back to streaming logs: Internal error occurred: Internal error occurred: error attaching to container: container is in CONTAINER_EXITED state
<h1>Hello from pod: app-nodeport-5c4749dfb6-wb5qv</h1>
pod "curl-test" deleted from default namespace
PS C:\Users\syed shah's\minikube-assignment> minikube ssh -- curl -s http://localhost:30080
<h1>Hello from pod: app-nodeport-5c4749dfb6-wb5qv</h1>

Step 12: opening NodePort with host machine (minikube service --url) 

PS C:\Users\syed shah's> cd minikube-assignment
PS C:\Users\syed shah's\minikube-assignment> minikube service app-nodeport-svc --url
http://127.0.0.1:61040
! Because you are using a Docker driver on windows, the terminal needs to be open to run it.
=== Step 13: LoadBalancer ka demo: minikube tunnel start karna ===

PS C:\Users\syed shah's> cd minikube-assignment\
PS C:\Users\syed shah's\minikube-assignment> minikube tunnel
* Tunnel successfully started

* NOTE: Please do not close this terminal as this process must stay alive for the tunnel to be accessible ...

! Access to ports below 1024 may fail on Windows with OpenSSH clients older than v8.1. For more information, see: https://minikube.sigs.k8s.io/docs/handbook/accessing/#access-to-ports-1024-on-windows-requires-root-permission
* Starting tunnel for service app-loadbalancer-svc.

step 13
PS C:\Users\syed shah's> cd minikube-assignment
PS C:\Users\syed shah's\minikube-assignment> kubectl get svc app-loadbalancer-svc
NAME                   TYPE           CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE
app-loadbalancer-svc   LoadBalancer   10.104.220.120   127.0.0.1     80:30479/TCP   22m

Step 14 access LoadBalancer from outside (curl) 

PS C:\Users\syed shah's\minikube-assignment> curl.exe http://127.0.0.1
<h1>Hello from pod: app-loadbalancer-7cdffb9865-cfwwm</h1>
PS C:\Users\syed shah's\minikube-assignment> 1..6 | ForEach-Object { curl.exe -s http://127.0.0.1 }
<h1>Hello from pod: app-loadbalancer-7cdffb9865-g7r2f</h1>
<h1>Hello from pod: app-loadbalancer-7cdffb9865-g7r2f</h1>
<h1>Hello from pod: app-loadbalancer-7cdffb9865-g7r2f</h1>
<h1>Hello from pod: app-loadbalancer-7cdffb9865-g7r2f</h1>
<h1>Hello from pod: app-loadbalancer-7cdffb9865-g7r2f</h1>
<h1>Hello from pod: app-loadbalancer-7cdffb9865-cfwwm</h1>

 Step 16 Project folder  final structure 

PS C:\Users\syed shah's\minikube-assignment> dir screenshots

    Directory: C:\Users\syed shah's\minikube-assignment\screenshots

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----         11/5/2026   1:59 PM          43692 loadbalancer.png
-a----         11/5/2026   1:47 PM          42759 nodeport.png


PS C:\Users\syed shah's\minikube-assignment> dir

    Directory: C:\Users\syed shah's\minikube-assignment

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----         11/5/2026   1:21 PM                app
d-----         11/5/2026   1:32 PM                k8s
d-----         11/5/2026   1:59 PM                screenshots
-a----         11/5/2026   1:58 PM          17249 outputs.txt

