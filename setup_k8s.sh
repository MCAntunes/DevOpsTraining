#!/bin/bash

# show commands on CLI and exit on error
set -e

# configure k8s componentes
kubectl apply -f KubernetesConfig/storageclass.yaml &>/dev/null
kubectl apply -f KubernetesConfig/persistent-volume.yaml &>/dev/null
kubectl apply -f KubernetesConfig/persistent-volume-claim.yaml &>/dev/null
kubectl apply -f KubernetesConfig/secret.yaml &>/dev/null
kubectl apply -f KubernetesConfig/configmap.yaml &>/dev/null
kubectl apply -f KubernetesConfig/statefulset.yaml &>/dev/null
kubectl apply -f KubernetesConfig/service.yaml &>/dev/null

# wait until pod is running
STATUS=`kubectl get pods mongodb-statefulset-0 --no-headers -o custom-columns=":status.phase"`

while :
do
    if [[ "$STATUS" =~ "Running" ]];
    then
        break
    else
        STATUS=`kubectl get pods mongodb-statefulset-0 --no-headers -o custom-columns=":status.phase"`
        sleep 1
    fi
done

kubectl get sc,pv,pvc --output=wide

# get IP for 'mongodb-service' service
minikube service --url mongodb-service
