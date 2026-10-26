# Calculator REST API — SPE Mini-Project

**CSE 816 — Software Production Engineering**
M.Tech (CSE) | Term I, 2026-27 | Faculty: Prof. B. Thangaraju

A production-style Calculator REST API built with **Java 17 + Spring Boot + Maven**, wrapped in a complete automated DevOps pipeline using **Git/GitHub → Jenkins → Docker → Docker Compose**.

---

## Architecture

```
[GitHub Push]
     |
     v
[Jenkins Pipeline]
  ├── Checkout
  ├── Build   (mvn clean package)
  ├── Test    (mvn test → JUnit XML)
  ├── Docker Build (multi-stage)
  ├── Push    (Docker Hub)
  └── Deploy  (docker compose up -d)
         |
         v
[Nginx :80] → [calculator-api :8080]
```

---

## Tech Stack

| Layer       | Technology              |
|-------------|-------------------------|
| Language    | Java 17                 |
| Framework   | Spring Boot 3.3.4       |
| Build       | Maven                   |
| Testing     | JUnit 5 + MockMvc       |
| CI/CD       | Jenkins (Declarative)   |
| Container   | Docker (multi-stage)    |
| Orchestration | Docker Compose        |
| Registry    | Docker Hub              |
| VCS         | Git / GitHub            |

---

## REST API Endpoints

| Method | Endpoint                     | Description                        |
|--------|------------------------------|------------------------------------|
| GET    | `/api/v1/add?a=&b=`      | Returns a + b                      |
| GET    | `/api/v1/subtract?a=&b=` | Returns a - b                      |
| GET    | `/api/v1/multiply?a=&b=` | Returns a * b                      |
| GET    | `/api/v1/divide?a=&b=`   | Returns a / b (b=0 → HTTP 400)    |
| GET    | `/actuator/health`           | Spring Actuator health probe       |

### Sample Response
```json
{
  "operation": "add",
  "a": 2,
  "b": 3,
  "result": 5
}
```

### Error Response (HTTP 400)
```json
{
  "error": "Division by zero is not allowed",
  "a": 10,
  "b": 0
}
```

---

## Getting Started

### Prerequisites
- Java 17+
- Maven 3.8+
- Docker & Docker Compose

### Build
```bash
mvn clean package
```

### Run Tests
```bash
mvn test
```
JUnit XML reports are generated in `target/surefire-reports/` for Jenkins.

### Run Locally (JAR)
```bash
java -jar target/calculator-1.0.0.jar
```

### Run with Docker
```bash
docker build -t calculator-api .
docker run -p 8080:8080 calculator-api
```

### Run Full Stack (Docker Compose)
```bash
docker compose up -d
```
API will be available via Nginx at `http://localhost/api/v1/...`

---

## Sample API Calls

```bash
# Add
curl "http://localhost/api/v1/add?a=5&b=3"

# Subtract
curl "http://localhost/api/v1/subtract?a=10&b=4"

# Multiply
curl "http://localhost/api/v1/multiply?a=6&b=7"

# Divide
curl "http://localhost/api/v1/divide?a=10&b=2"

# Divide by zero (expect HTTP 400)
curl "http://localhost/api/v1/divide?a=10&b=0"

# Health check
curl "http://localhost/actuator/health"
```

---

## Project Structure

```
calculator-devops/
  ├── src/
  │   ├── main/
  │   │   ├── java/com/spe/calculator/
  │   │   │   ├── CalculatorApplication.java
  │   │   │   ├── controller/CalculatorController.java
  │   │   │   ├── service/CalculatorService.java
  │   │   │   └── dto/
  │   │   │       ├── CalculatorResponse.java
  │   │   │       └── ErrorResponse.java
  │   │   └── resources/application.properties
  │   └── test/
  │       └── java/com/spe/calculator/
  │           ├── service/CalculatorServiceTest.java
  │           └── controller/CalculatorControllerTest.java
  ├── pom.xml
  ├── Dockerfile
  ├── .dockerignore
  ├── docker-compose.yml
  ├── nginx.conf
  ├── Jenkinsfile
  ├── .gitignore
  └── README.md
```

---

## CI/CD Pipeline (Jenkins)

The Jenkins pipeline is defined in `Jenkinsfile` and includes these stages:

| Stage        | Description                                      |
|--------------|--------------------------------------------------|
| Checkout     | Pull latest code from GitHub                     |
| Build        | `mvn clean package -DskipTests`                  |
| Test         | `mvn test` + publish JUnit XML results           |
| Docker Build | Build multi-stage image tagged with build number |
| Push         | Push image to Docker Hub                         |
| Deploy       | `docker compose up -d` + health check verify     |

---

## License
MIT — For educational purposes (SPE Mini-Project, IIIT Bangalore)
