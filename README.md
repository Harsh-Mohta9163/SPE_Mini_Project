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
  ├── scripts/
  │   ├── generate_pdf_report.py    # ReportLab academic PDF generator
  │   ├── smoke_test.py             # Python multi-endpoint deployment verification
  │   └── smoke_test.sh             # Bash multi-endpoint deployment verification
  ├── pom.xml                       # Maven build specification (Spring Boot 3.3.4)
  ├── Dockerfile                    # Multi-stage Docker build (Alpine JRE 17)
  ├── .dockerignore                 # Excludes target/, .git/, and IDE artifacts
  ├── docker-compose.yml            # Multi-container orchestration (API + Nginx)
  ├── nginx.conf                    # Reverse proxy gateway configuration
  ├── Jenkinsfile                   # Declarative 6-stage CI/CD pipeline
  ├── REPORT.md                     # Comprehensive academic project report
  ├── REPORT.html                   # Print-optimized HTML report
  ├── SPE_Mini_Project_Report.pdf   # 3-Page evaluation PDF report
  ├── SCREENSHOTS_GUIDE.md          # Guide for 5 required rubric screenshots
  ├── DEMO_SCRIPT.md                # Live demonstration script & viva preparation
  ├── PHASE_PLAN.md                 # 7-Phase implementation roadmap & tracker
  ├── .gitignore                    # Git ignore file for Java, Maven, and OS files
  └── README.md                     # Project overview and instructions
```

---

## Automated Smoke Testing

To verify all endpoints and Actuator health probe in a single command against the running stack:

```bash
# Python runner (cross-platform)
python scripts/smoke_test.py

# Or Bash runner
bash scripts/smoke_test.sh
```

---

## CI/CD Pipeline (Jenkins)

The Jenkins pipeline is defined in `Jenkinsfile` and includes these stages:

| Stage        | Description                                      |
|--------------|--------------------------------------------------|
| Checkout     | Pull latest code from GitHub on push/poll trigger |
| Build        | `mvn clean package -DskipTests` + archive JAR    |
| Test         | `mvn test` + publish JUnit XML results (22 tests) |
| Docker Build | Build multi-stage Alpine image tagged with build #|
| Push         | Authenticate with Docker Hub (`dockerhub-creds`) |
| Deploy       | `docker compose up -d` + Actuator health verify  |

---

## Deliverables & Documentation

- **Project Report (PDF):** [`SPE_Mini_Project_Report.pdf`](file:///SPE_Mini_Project_Report.pdf) (Generated via `python scripts/generate_pdf_report.py`)
- **Report Source (Markdown):** [`REPORT.md`](file:///REPORT.md)
- **Screenshots Checklist:** [`SCREENSHOTS_GUIDE.md`](file:///SCREENSHOTS_GUIDE.md)
- **Live Demo Script:** [`DEMO_SCRIPT.md`](file:///DEMO_SCRIPT.md)
- **Phase Implementation Tracker:** [`PHASE_PLAN.md`](file:///PHASE_PLAN.md)

---

## License
MIT — For educational purposes (SPE Mini-Project, IIIT Bangalore)

