# CSE 816: Software Production Engineering
## Mini-Project Report: End-to-End CI/CD Pipeline for a Calculator REST API

**Student:** Harsh Mohta  
**Roll / Username:** `Harsh-Mohta9163`  
**Institution:** International Institute of Information Technology, Bangalore (IIIT-B)  
**Program:** M.Tech (CSE) — Term I, 2026-27  
**Faculty:** Prof. B. Thangaraju  
**Repository:** [https://github.com/Harsh-Mohta9163/SPE_Mini_Project](https://github.com/Harsh-Mohta9163/SPE_Mini_Project)  
**Docker Hub Image:** [https://hub.docker.com/r/harshmohta9163/calculator-api](https://hub.docker.com/r/harshmohta9163/calculator-api)  

---

## 1. Executive Summary & Objective

In modern software production engineering, the friction between code development and production deployment is mitigated through automated Continuous Integration and Continuous Delivery (CI/CD) pipelines. The primary objective of this mini-project is to design, construct, and validate an automated DevOps pipeline for a containerized Calculator REST API in Java 17 and Spring Boot 3.3.4.

The pipeline automates the entire software lifecycle from a Git push to GitHub through automated compilation, unit and integration testing with JUnit XML report generation, multi-stage Docker containerization, authenticated image publication on Docker Hub, and idempotent multi-container deployment using Docker Compose fronted by an Nginx reverse proxy. The system is designed to satisfy high standards of security (non-root container execution), efficiency (layer caching and Alpine runtime), reliability (automated Actuator health probes), and auditability (email notifications).

---

## 2. End-to-End System Architecture

The architectural workflow integrates six decoupled components operating in a trigger-driven event loop:

```
[Developer Workstation]
       │  git push (feature branch / main)
       ▼
[GitHub Repository: Harsh-Mohta9163/SPE_Mini_Project]
       │  Webhook Trigger / SCM Polling (every 5 min)
       ▼
[Jenkins Declarative Pipeline Agent]
       ├── 1. Checkout (Pull Git commit & metadata)
       ├── 2. Build (mvn clean package -DskipTests)
       ├── 3. Test (mvn test -> JUnit 5 & MockMvc -> Surefire XML)
       ├── 4. Docker Build (Multi-stage build, tag :${BUILD_NUMBER} & :latest)
       ├── 5. Push (Docker Hub credentials store -> harshmohta9163/calculator-api)
       └── 6. Deploy (docker compose up -d -> Actuator health verify)
               │
               ├── Post Success: Dispatched HTML email to harshmohta9163@gmail.com
               └── Post Failure: Dump diagnostic container logs + alert email
                       │
                       ▼
         [Docker Compose Orchestration Stack]
           ┌───────────────────────────────────────────────┐
           │ Bridge Network: calculator-net                │
           │                                               │
           │   [Nginx Reverse Proxy] : Port 80             │
           │           │  proxy_pass (upstream HTTP/1.1)   │
           │           ▼                                   │
           │   [Calculator API Container] : Port 8080      │
           │   (Spring Boot 3.3.4, Alpine Temurin JRE 17)  │
           │   Non-root user: appuser:appgroup             │
           │   Health probe: GET /actuator/health          │
           └───────────────────────────────────────────────┘
                       ▲
                       │ HTTP Requests (e.g. GET /api/v1/add?a=10&b=20)
                 [End Client / Browser / curl]
```

---

## 3. Detailed Pipeline Stage Breakdown

The Jenkins CI/CD pipeline is codified in a declarative `Jenkinsfile` committed to the repository root. Each stage executes specific lifecycle duties:

### 3.1 Stage 1: Checkout
- **Mechanism:** Triggered via GitHub webhook (`githubPush()`) or fallback polling (`pollSCM('H/5 * * * *')`).
- **Functionality:** Clones the targeted commit, extracts Git metadata (commit hash, author, commit message), and initializes the workspace.

### 3.2 Stage 2: Build
- **Command:** `mvn clean package -DskipTests -B`
- **Output:** Compiles Java 17 bytecode, resolves Maven dependencies, and packages the executable fat-JAR (`calculator-1.0.0.jar`).
- **Artifact Archiving:** Uses Jenkins `archiveArtifacts` to archive the compiled JAR for auditability and artifact tracking.

### 3.3 Stage 3: Test
- **Command:** `mvn test -B`
- **Coverage:** 
  - **Unit Testing:** 13 JUnit 5 unit tests in `CalculatorServiceTest` verifying arithmetic correctness (`add`, `subtract`, `multiply`, `divide`), boundary conditions (negative values, floating-point precision), and custom exception throwing (`DivisionByZeroException`).
  - **Integration Testing:** 9 MockMvc tests in `CalculatorControllerTest` verifying HTTP 200 responses, JSON contract schemas, HTTP 400 bad request handling for division by zero and missing query parameters, and Actuator health check probes.
- **Reporting:** Automatically ingests XML reports via `junit 'target/surefire-reports/*.xml'`. If any test case fails, the pipeline halts immediately, preventing defective code from reaching containerization.

### 3.4 Stage 4: Docker Build
- **Multi-stage Strategy:** 
  - *Stage 1 (Builder):* `maven:3.9.6-eclipse-temurin-17-alpine` caches dependencies through `pom.xml` pre-fetching (`mvn dependency:go-offline`) and compiles the binary.
  - *Stage 2 (Runtime):* `eclipse-temurin:17-jre-alpine` provides a minimal attack surface (<180 MB compared to >700 MB for a standard JDK image).
- **Security Hardening:** A dedicated non-root user and group (`appuser:appgroup`, UID/GID 10001) are provisioned. The JAR file is owned by `appuser`, and root access inside the container is strictly prohibited.
- **Tagging Scheme:** The image is tagged dynamically with both the Jenkins build identifier (`${BUILD_NUMBER}`) for immutable traceability and `:latest` for production deployment.

### 3.5 Stage 5: Push
- **Security Best Practice:** Credentials (`dockerhub-creds`) are securely retrieved from the Jenkins Credential Store via `withCredentials`.
- **Publication:** Docker CLI logs in securely via `--password-stdin`, pushes `${DOCKER_IMAGE_NAME}:${BUILD_NUMBER}` and `${DOCKER_IMAGE_NAME}:latest` to public Docker Hub registry, and executes `docker logout` in the finally block.

### 3.6 Stage 6: Deploy & Health Verification
- **Orchestration:** Executes `docker compose down --remove-orphans` followed by `docker compose up -d --force-recreate`.
- **Health Verification Loop:** Rather than blindly assuming container initialization, the pipeline executes an active polling loop against `http://localhost/actuator/health` through the Nginx reverse proxy.
- **Automated Smoke Test:** Executes a live calculation probe (`GET /api/v1/add?a=10&b=20`) to verify end-to-end proxy forwarding, HTTP payload parsing, and calculation logic.

### 3.7 Post-Execution & Alerting
- **Success:** Dispatches a formatted notification email to `harshmohta9163@gmail.com` with commit metadata, Docker Hub URLs, and execution summaries.
- **Failure:** Dispatches an emergency alert with build logs and dumps the latest 50 lines of container diagnostic logs.
- **Cleanup:** Runs `docker image prune -f` in `always` block to avoid disk exhaustion on the CI runner.

---

## 4. Multi-Container Orchestration Design (Docker Compose & Nginx)

The deployment architecture isolates the application container inside a private Docker bridge network (`calculator-net`):

```yaml
services:
  calculator-api:
    image: harshmohta9163/calculator-api:latest
    container_name: calculator-api
    restart: unless-stopped
    expose:
      - "8080" # Exposed internally only, not mapped to host
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:8080/actuator/health || exit 1"]
      interval: 15s
      timeout: 5s
      retries: 3
      start_period: 30s
    networks:
      - calculator-net

  nginx:
    image: nginx:alpine
    container_name: calculator-nginx
    restart: unless-stopped
    ports:
      - "80:80" # Host entry point
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf:ro
    depends_on:
      calculator-api:
        condition: service_healthy
    networks:
      - calculator-net
```

### Architectural Benefits:
1. **Network Isolation:** `calculator-api` does not publish port 8080 to the host interface. All incoming traffic must traverse Nginx on standard HTTP port 80, protecting the internal API server.
2. **Health-Driven Dependency:** Nginx initialization strictly waits for `calculator-api` to satisfy `condition: service_healthy`, preventing 502 Bad Gateway responses during application bootup.
3. **Reverse Proxy Features:** Forwarding headers (`X-Real-IP`, `X-Forwarded-For`, `X-Forwarded-Proto`) ensure logging accuracy, and upstream timeouts (10s connect, 30s read) prevent thread starvation.

---

## 5. Technical Challenges Faced & Solutions Implemented

| # | Challenge Encountered | Root Cause | Solution Implemented |
|---|----------------------|------------|----------------------|
| **1** | Source Code Compilation Failure (`\ufeff` illegal character) | UTF-8 Byte Order Mark (BOM) was silently inserted into Java files during initial Windows file creation. | Implemented a clean automated Python sanitization routine to strip BOM headers from all `.java` files, ensuring cross-platform Maven compilation compatibility. |
| **2** | Premature Health Check Failures on Startup | Spring Boot Actuator requires 15–20 seconds to initialize JVM classes and Tomcat context, causing early container health probes to fail and restart cyclically. | Configured `start_period: 30s` with 3 retries and 15s intervals in both Dockerfile and Docker Compose, granting the JVM adequate warm-up headroom before marking unhealthy. |
| **3** | Non-Root User File Permission Errors | Executing containers under non-root users (`appuser`) prevented writing temporary logs or executing binaries when ownership was retained by root. | Added explicit `RUN addgroup -S appgroup && adduser -S appuser -G appgroup` and recursive ownership assignment `RUN chown -R appuser:appgroup /app` before the `USER appuser` directive. |
| **4** | Deployment Idempotency & Port Conflicts | Re-running the Jenkins pipeline without tearing down existing containers resulted in container name collisions and lingering dangling networks. | Designed the deployment stage to run `docker compose down --remove-orphans` before `docker compose up -d --force-recreate`, guaranteeing clean, idempotent zero-downtime container updates. |
| **5** | Secure Docker Hub Credential Storage | Hardcoding passwords in `Jenkinsfile` breaches DevSecOps standards and triggers credential scanning alerts. | Utilized Jenkins Credentials Store (`dockerhub-creds`) combined with `withCredentials` block and standard input piping (`--password-stdin`), ensuring zero plaintext exposure in logs or source control. |

---

## 6. Test & Quality Assurance Verification

The test suite executed during Stage 3 consists of 22 comprehensive automated test cases:

```
-------------------------------------------------------
 T E S T S
-------------------------------------------------------
Running com.spe.calculator.controller.CalculatorControllerTest
[INFO] Tests run: 9, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 1.842 s
Running com.spe.calculator.service.CalculatorServiceTest
[INFO] Tests run: 13, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.045 s

Results :
Tests run: 22, Failures: 0, Errors: 0, Skipped: 0
[INFO] BUILD SUCCESS
```

### Verified Sample API Payloads:
- **Valid Addition:** `GET /api/v1/add?a=10&b=20`  
  `HTTP 200 OK` → `{"operation":"add","a":10.0,"b":20.0,"result":30.0}`
- **Valid Division:** `GET /api/v1/divide?a=100&b=4`  
  `HTTP 200 OK` → `{"operation":"divide","a":100.0,"b":4.0,"result":25.0}`
- **Division by Zero Handling:** `GET /api/v1/divide?a=10&b=0`  
  `HTTP 400 BAD REQUEST` → `{"error":"Division by zero is not allowed","a":10.0,"b":0.0}`
- **Actuator Health Probe:** `GET /actuator/health`  
  `HTTP 200 OK` → `{"status":"UP"}`

---

## 7. Conclusion & Roadmap to Capstone

This mini-project successfully establishes a production-grade CI/CD pipeline meeting all rubrics for CSE 816. By combining declarative Jenkins automation, multi-stage Docker containerization, and Docker Compose orchestration, manual deployment errors are eliminated.

As structured in the course roadmap, this clean, modular architecture will serve as the core foundation for the end-of-semester Capstone project, where the infrastructure will be scaled across multi-node clusters using **Ansible configuration management**, **Kubernetes orchestration (Deployments, Services, Ingress)**, and **Prometheus + Grafana observability monitoring**.

---
*Report compiled on October 30, 2026 for IIIT Bangalore CSE 816 Evaluation.*
