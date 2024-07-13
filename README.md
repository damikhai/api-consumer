# API Consumer

### Introduction
There is a cluster consisting of several nodes, and on this cluster, we need to create and manage groups. 
To create a group, you need to create a record on all nodes via an API. 
Similarly, when you delete a group, you need to delete it from all nodes. 

The problem is that the API is unstable, with possible connection timeouts or 500 errors for unknown reasons. 
If an error occurs, all changes should be rolled back.

### Assumptions
Due to the unstable cluster APIs that can return 500 errors or timeouts and etc,
the API Consumer has multiple failure protection mechanisms against APIs failures:
- Retry logic for specific status codes (429, 500, 503).
- Rollback mechanism on failure to ensure data consistency across the cluster.
- General exceptions handling

## Usage
### Requirements

- Python ~3.11
- Poetry
- Docker
- Kubernetes
- Helm
- Minikube

### How to run
- Install all needed dependencies:
  ```
  poetry install
  ```
- Activate your virtual environment:
  ```
  poetry shell
  ```
- Create your own `.env` file based on `.env_example` (if not default values will be encountered)
- Go to `app` folder:
  ```
  cd app
  ```
- For running `API Consumer` execute following command:
  ```
  python main.py
  ```
- For running tests execute any following command:
  ```
  python -m pytest
  ```
  ```
  pytest
  ```
  ```
  poetry run pytest
  ```

### Linter (Ruff):
- Run the Ruff linter over the project via `ruff check <path>`
  ```
  ruff check .
  ```

## Build and Deploy to Minikube
- Ensure you are in the root directory of the project where the Dockerfile is located, then build the image.
  ```
  docker build -t api-consumer .
  ```
  Start minikube 
  ```
  minikube start --driver=docker
  ```
  Load the docker image to minikube cluster
  ```
  minikube image load api-consumer
  ```
  Verify the image was loaded to minikube cluster
  ```
  minikube ssh -- docker images
  ```
  Deploy the helm chart to the default minikube namespace
  ```
  helm upgrade --install api-consumer manifests/. --namespace default
  ```
  Verify the helm chart was deployed and pod is running
  ```
  kubectl get all
  ```
  Get logs from the pod
  ```
  kubectl logs <pod_name> > file-name.log 
  ```
 