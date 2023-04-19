# K8s Getting started

## Kubernetes esquema

![K8s](./kubernetes_schema.png)

## Minikube

Cluster de Kubernetes en local, centrado para el aprendizaje y desarrollo.

1. Instalación.
    ```shell
    curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
    sudo install minikube-linux-amd64 /usr/local/bin/minikube
    ```
2. Iniciar el clúster.
    ```shell
    minikube start
    ```
3. Dashboard.
    ```shell
    minikube dashboard
    ```
4. Desplegar aplicaciones.

    - **Service**
        ```shell
        # Deployment "hello-minikube" de tipo NodePort
        kubectl create deployment hello-minikube --image=kicbase/echo-server:1.0
        kubectl expose deployment hello-minikube --type=NodePort --port=8080

        # Ver el estado del servicio
        kubectl get services hello-minikube

        # Iniciar el servicio bajo un túnel, todo gestionado automáticamente por minikube
        minikube service hello-minikube

        # O bien, usar kubectl para mapear el puerto.
        kubectl port-forward service/hello-minikube 7080:8080
        ```

    - **LoadBalancer**
        ```shell
        # Deployment "balanced" de tipo LoadBalancer
        kubectl create deployment balanced --image=kicbase/echo-server:1.0
        kubectl expose deployment balanced --type=LoadBalancer --port=8080

        # Iniciar el túnel
        minikube tunnel

        # Obtener la IP external del servicio "balanced"
        kubectl get services balanced

        # Deployment disponible en <EXTERNAL-IP>:8080
        ```

    - **Ingress**
        ```shell
        # Habilitar el addon ingress
        minikube addons enable ingress

        # Aplicar el contenido del fichero `ingress-example.yml`
        kubectl apply -f ./ingress-example.yml

        # Iniciar el túnel
        minikube tunnel

        # Comprobar que funciona el ingress
        curl 127.0.0.1/foo
        curl 127.0.0.1/bar
        ```
5. Gestionar el clúster.
    ```shell
    # Pauser el clúster
    minikube pause

    # Reaunar el clúster pausado
    minikube unpause

    # Parar el clúster
    minikube stop

    # Obtener propiedades de configuración (previamente deben haber sido establecidas)
    minikube config set memory 9001
    minikube config get memory

    # Listado del catálogo de servicios de Kubernetes
    minikube addons list

    # Crear un segundo clúster con una release más antigua de K8s
    minikube start -p aged --kubernetes-version=v1.16.1

    # Eliminar todos los minikube clústers
    minikube delete --all
    ```

### Referencias

- [Controles básicos](https://minikube.sigs.k8s.io/docs/handbook/controls)
- [Configuración](https://minikube.sigs.k8s.io/docs/handbook/config)
- [Despliegue de aplicaciones](https://minikube.sigs.k8s.io/docs/handbook/deploying)
- [Kubectl](https://minikube.sigs.k8s.io/docs/handbook/kubectl)
- [Accediendo a aplicaciones](https://minikube.sigs.k8s.io/docs/handbook/accessing)
- [Headlamp](https://minikube.sigs.k8s.io/docs/handbook/addons/headlamp)
- [Ingress DNS](https://minikube.sigs.k8s.io/docs/handbook/addons/ingress-dns)
- [Subiendo imágenes](https://minikube.sigs.k8s.io/docs/handbook/pushing)

## Deploy

Antes de poder desplegar una aplicación, es necesario disponer de la imagen Docker de dicha aplicación.

En el directorio *ping_api* se ha dejado una pequeña aplicación para simular el proceso.

1. Construir la imagen.
    ```shell
    cd ping_api
    docker build -t {image_name:tag} .
    ```
2. Subir la imagen al registry de minikube.
    ```shell
    minikube image load {image_name:tag}
    ```
3. Crear el deployment.
    ```shell
    kubectl create deployment {deployment_name} --image={image_name:tag}
    # verificar que se ha creado correctamente el deployment
    kubectl get deployments {deployment_name}
    ```

## Pods y Nodos

Un **nodo** es una máquina (virtual o física, dependiendo del clúster) gestionado por el Control Plane de K8s. Dentro de cada nodo puede haber varios pods, el cual contendrá la aplicación contenerizada y (opcional) volúmenes.

Cada nodo ejecuta al menos:

- **Kubelet**, el cual se encarga de gestionar el nodo con el Control Plane de K8s; el cual gestiona los pods y los contenedores corriendo dentro de la máquina.
- **Contenedor runtime** (como Docker) responsable de:
    - Bajarse la imagen del registry.
    - Desempaquetal el contenedor.
    - Ejecutar la aplicación.

Comandos útiles:

- `kubectl get pods`
- `kubectl describe pod {pod_name}`
- `kubectl logs {pod_name}`
- `kubectl exec {pod_name}` -- {command}
- `kubectl exec -it {pod_name}` -- bash
