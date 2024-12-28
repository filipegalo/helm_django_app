# helm_django_app

A Django application demonstrating Kubernetes deployment with Helm, featuring safe database migrations with locking mechanisms and rollback capabilities.

  - [Prerequisites](#prerequisites)
  - [Features](#features)
  - [Migration Management](#migration-management)
    - [Rolling Back Migrations](#rolling-back-migrations)
  - [Local Development](#local-development)
  - [Docker](#docker)
  - [K8s](#k8s)
  - [Helm](#helm)

## Prerequisites

- Python 3.12+
- Docker
- Minikube
- Helm 3
- kubectl

## Features

- Django application deployment using Helm
- Safe database migrations with locking mechanism (preventing race conditions and data corruption)
- Migration rollback capability
- Multi-replica support

## Migration Management

The project includes a custom management command for safe database migrations across multiple replicas.

### Rolling Back Migrations

To roll back migrations, modify `chart/values.yaml`:

```yaml
migrations:
  targets:
    - "main 0001" # Run specific migration for main app
    - "main zero" # Revert all migrations for main app
```

In a real-world scenario, we would implement a CI/CD pipeline that automatically updates the appVersion in the Helm chart. Additionally, a continuous delivery tool (such as ArgoCD) would handle deploying the new version of the application.

If we discover that the database migrations are not functioning as intended after deployment, we can easily roll them back to a previous state by modifying the targets list in the chart/values.yaml file.

To test the rollback mechanism, please follow the steps [Docker](#docker), [K8s](#k8s) and [Helm](#helm).

After installing Helm and starting the application, you can access it using the URL provided by the `minikube service` command to view the list of applied migrations.

![preview](https://i.postimg.cc/bNFD6b99/before-migrations.png)

As shown in the screenshot, there are two migrations: `main 0001` and `main 0002`.
Let's say we discover issues with the `main 0002` migration and need to roll it back.

To do that, we need to change the targets list in the chart/values.yaml file.

```yaml
migrations:
  targets:
    - "main 0001" # Run specific migration for main app
```

After this change, we can run:

```bash
helm upgrade helm-django-postgres ./chart
```

After the upgrade is done, we can check the list of migrations again and see that main 0002 has been reverted and we only have main 0001.

![preview](https://i.postimg.cc/0QTxMkYm/after-migrations.png)

To test locked migrations, just increase the number of replicas in the chart/values.yaml file.

## Local Development

1. **Run a Postgres container**

```

docker run --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=mysecretpassword -d postgres

```

2. **Create Python virtual environment**

```

cd app
python -m venv venv
source venv/bin/activate

```

3. **Install dependencies**

```

pip install -r requirements-dev.txt

```

4. **Run the Django app**

```

python manage.py runserver

```

**Note:** If you customized the docker run command for Postgres, you need to update the file **.env** with the changed values.

- POSTGRES_DB
- POSTGRES_USER
- POSTGRES_PASSWORD
- POSTGRES_HOST
- POSTGRES_PORT

## Docker

1. **Build the Docker image**

```

cd app && docker build -t django-app:0.0.1 .

```

## K8s

To demonstrate the deployment of the Django app in a Kubernetes cluster, we will use Minikube.
Follow the documentation on the [Minikube website](https://minikube.sigs.k8s.io/docs/start/) to install Minikube on your machine.

1. **Start Minikube**

```

minikube start

```

2. **Load the Docker image into Minikube**

```

minikube image load django-app:0.0.1

```

## Helm

1. **Install the Helm chart**

```

helm install helm-django-postgres ./chart

```

2. **Expose the Django app**

```

minikube service helm-django-postgres-django --url

```

3. **Access the application with the provided url**
