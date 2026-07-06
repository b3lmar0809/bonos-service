# VidalCasino 2.0 - Bonos Service

Este repositorio contiene el microservicio **bonos-service** del proyecto **VidalCasino 2.0**, desarrollado para la evaluación EP3 de Introducción a Herramientas DevOps. Este servicio administra los bonos y promociones disponibles para los usuarios, permitiendo acreditar saldo y registrar automáticamente las transacciones correspondientes.

---

# Descripción general

**bonos-service** permite consultar los bonos disponibles, visualizar los bonos reclamados por un usuario y reclamar promociones como bonos de bienvenida, recarga y cashback.

El microservicio comparte la base de datos PostgreSQL y el **JWT_SECRET** con **casino-backend**, validando los tokens emitidos por el backend sin contar con un sistema de autenticación propio.

El servicio se ejecuta dentro del clúster de **Amazon EKS** y se expone únicamente mediante un **Service** de tipo **ClusterIP**, siendo consumido por el backend y el frontend a través de las rutas **/api/bonos**.

---

# Arquitectura del sistema

El sistema **VidalCasino 2.0** está compuesto por los siguientes servicios:

- casino-frontend: interfaz web pública mediante LoadBalancer.
- casino-backend: backend principal encargado de la autenticación y lógica del negocio.
- bonos-service: gestión de bonos y promociones.
- apuestas-service: administración de eventos deportivos y apuestas.
- estadisticas-service: generación de estadísticas y dashboards.
- postgres: base de datos compartida.

---

# Tecnologías utilizadas

- Python
- FastAPI
- PostgreSQL
- Docker
- Kubernetes
- Amazon EKS
- Amazon ECR
- GitHub Actions
- Horizontal Pod Autoscaler (HPA)
- AWS Academy Learner Lab

---

# Endpoints disponibles

| Método | Endpoint | Descripción |
|---------|----------|-------------|
| GET | `/api/bonos` | Obtiene el listado de bonos disponibles. |
| GET | `/api/bonos/mis-bonos` | Consulta los bonos reclamados por el usuario autenticado. |
| POST | `/api/bonos/{codigo}/reclamar` | Reclama un bono y acredita el saldo correspondiente. |

---

# Endpoints de salud

El servicio incorpora sondas de salud para Kubernetes:

- `/livez`
- `/readyz`

### `/livez`

Verifica que el proceso de FastAPI continúa ejecutándose correctamente.

### `/readyz`

Comprueba que el servicio se encuentra listo para recibir tráfico y que mantiene conectividad con la base de datos PostgreSQL.

---

# Despliegue en Kubernetes

Los manifiestos del servicio se encuentran en:

```text
k8s/
```

Archivos principales:

```text
k8s/deployment.yaml
k8s/service.yaml
k8s/hpa.yaml
```

El servicio se despliega con **2 réplicas** y se expone internamente mediante un **Service** de tipo **ClusterIP** en el puerto **8004**.

Además, incorpora un **Horizontal Pod Autoscaler (HPA)** que incrementa o reduce automáticamente la cantidad de Pods según el consumo de CPU.

---

# CI/CD

El despliegue automático se encuentra definido en:

```text
.github/workflows/deploy.yml
```

El workflow se ejecuta al realizar un **push** sobre la rama **deploy**.

El pipeline realiza las siguientes tareas:

- Descarga del código fuente.
- Configuración de credenciales de AWS Academy.
- Inicio de sesión en Amazon ECR.
- Construcción de la imagen Docker.
- Publicación de la imagen con los tags **latest**, **v1.0.1** y el SHA del commit.
- Conexión al clúster de Amazon EKS.
- Actualización del Deployment.
- Verificación del rollout.
- Validación del estado de los Pods.

---

# Ejecución local

Crear el entorno virtual:

```bash
python -m venv .venv
```

Activarlo:

**Linux / macOS**

```bash
source .venv/bin/activate
```

**Windows**

```powershell
.venv\Scripts\activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Configurar las variables de entorno copiando:

```text
.env.example
```

como

```text
.env
```

---

# Comandos de verificación

```bash
kubectl get deployment bonos-service

kubectl get svc bonos-service

kubectl get hpa bonos-service-hpa

kubectl get pods -l app=bonos-service -o wide

kubectl describe deployment bonos-service
```

---

# Estado esperado

- Deployment disponible con 2 réplicas.
- Service interno de tipo ClusterIP.
- Horizontal Pod Autoscaler activo.
- Pods en estado **Running**.
- Imagen desplegada desde Amazon ECR.
- Pipeline de GitHub Actions ejecutado correctamente.
- Servicio respondiendo correctamente a las rutas **/livez**, **/readyz**, **/api/bonos**, **/api/bonos/mis-bonos** y al reclamo de bonos mediante **/api/bonos/{codigo}/reclamar**.
