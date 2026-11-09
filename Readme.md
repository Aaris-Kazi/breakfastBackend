# Quick Commerece backend Implementation

This is the basic archetecture for Quick Commerce the developing and deploying the backend for the
adding cart, ordering and updating the order/ delivery status 

## To Deploy Kubernetes
    kubectl apply -f deployment.yml
    minikube image load aariskazi/breakfast-app:v19
    kubectl rollout restart deployment breakfast-app
    kubectl get svc
    minikube service breakfast-app-service --url
    kubectl get endpoints breakfast-app-service

## Archetechture of the Microservice

![Alt Archetecture](snapshots/arch_bf.png)