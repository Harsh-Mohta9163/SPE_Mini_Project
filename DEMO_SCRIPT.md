# 🎤 Class 17 Live Demo Script & Viva Preparation Guide

**Course:** CSE 816 — Software Production Engineering  
**Faculty Evaluator:** Prof. B. Thangaraju  
**Student:** Harsh Mohta (`Harsh-Mohta9163`)  
**Project:** End-to-End CI/CD Pipeline for a Calculator REST API  
**Target Duration:** 5 to 7 Minutes  

---

## ⏱️ Live Demo Timeline & Walkthrough

### 1. Introduction (30 Seconds)
> *"Good morning / afternoon Professor. My name is Harsh Mohta. Today I am presenting my mini-project for CSE 816: an automated, end-to-end CI/CD pipeline for a containerized Calculator REST API built with Java 17, Spring Boot, Maven, Jenkins, Docker, and Docker Compose."*
>
> *"The objective of this pipeline is complete zero-touch deployment: from a single `git push` to GitHub, our Jenkins declarative pipeline automatically checks out code, runs 22 JUnit 5 and MockMvc tests, compiles and builds a secure multi-stage Docker image, pushes the image to Docker Hub, and orchestrates an idempotent multi-container deployment behind an Nginx reverse proxy with health check verification."*

---

### 2. Triggering the CI/CD Pipeline Live (1 Minute)
* Show your open Jenkins Dashboard on screen (`http://localhost:8080` or your lab Jenkins URL).
* Make a minor code or documentation edit in your terminal:
  ```bash
  # Example: update a comment or log in CalculatorService.java or README
  git checkout main
  git status
  ```
* Commit and push the change:
  ```bash
  git commit -am "chore(demo): trigger live automated pipeline build for Class 17 evaluation"
  git push origin main
  ```
* Switch to Jenkins: point out that the webhook / SCM poll has triggered the build automatically (e.g. Build `#N`).

---

### 3. Walking Through the 6 Pipeline Stages in Jenkins (2 Minutes)
While Jenkins executes the pipeline live in the **Stage View** or **Blue Ocean**:

1. **Stage 1: Checkout**
   - *"The pipeline detects the commit on the `main` branch, pulls the latest code, and prints the Git commit SHA and author information."*
2. **Stage 2: Build**
   - *"Executes `mvn clean package -DskipTests` to compile the Java 17 bytecode and package the executable fat-JAR. Notice that we archive the resulting JAR file directly in Jenkins for release auditing."*
3. **Stage 3: Test**
   - *"Executes `mvn test`. Here, 13 JUnit 5 unit tests and 9 MockMvc integration tests run. The Surefire XML reports are published to the Jenkins JUnit dashboard. If any test fails, the pipeline halts immediately, preventing defective builds from reaching the container stage."*
4. **Stage 4: Docker Build**
   - *"We use a multi-stage Dockerfile. Stage 1 compiles inside a Maven Alpine image with cached dependencies. Stage 2 copies only the JAR into an Eclipse Temurin 17 Alpine JRE image. This slashes image size from over 700 MB to around 180 MB. Notice that the container is secured with a non-root user `appuser:appgroup`."*
5. **Stage 5: Push**
   - *"Using Jenkins Credential Store (`dockerhub-creds`), Jenkins authenticates securely via standard input without exposing tokens in the console log. It tags the image with both the immutable build number (`#N`) and `:latest`, pushes both to Docker Hub, and logs out immediately."*
6. **Stage 6: Deploy**
   - *"Docker Compose tears down any orphaned containers and deploys the new containers with `--force-recreate`. The pipeline then actively polls the Spring Boot Actuator endpoint (`/actuator/health`) through Nginx until it receives HTTP 200 `UP`. It then runs an automated smoke calculation before declaring success."*

---

### 4. Live Verification & API Testing (1.5 Minutes)
Once the pipeline shows all green stages:

1. **Show Running Containers:**
   ```bash
   docker compose ps
   ```
   *Point out:*
   - `calculator-api` is `Up (healthy)` on private port 8080.
   - `calculator-nginx` is `Up` and bound to host port 80.
   - Both reside on the isolated `calculator-net` bridge network.

2. **Execute Smoke Test Suite:**
   ```bash
   python scripts/smoke_test.py
   ```
   *Point out:*
   - All 7 automated test assertions pass with HTTP 200 OK.
   - Show the divide-by-zero validation returning HTTP 400 with structured JSON:
     `{"error":"Division by zero is not allowed","a":50.0,"b":0.0}`

3. **Show Docker Hub & Email Notification:**
   - Open browser tab: [https://hub.docker.com/r/harshmohta9163/calculator-api](https://hub.docker.com/r/harshmohta9163/calculator-api) to show the freshly pushed tag.
   - Show the received success email in the inbox with build metadata.

---

## 🧠 Anticipated Viva Questions & Model Answers

### Q1: Why did you use a multi-stage Dockerfile instead of a simple single-stage Dockerfile?
> **Answer:** *"A single-stage Dockerfile that includes the Maven build tools, JDK compiler, and cached repository produces an image larger than 700 MB and includes build tools that introduce an unnecessary attack surface in production. In our multi-stage Dockerfile, Stage 1 (builder) uses `maven:3.9.6-eclipse-temurin-17-alpine` to build the JAR. Stage 2 (runtime) uses `eclipse-temurin:17-jre-alpine`, copying only the resulting JAR. This reduces the runtime image size down to approximately 180 MB, optimizes layer caching, and eliminates build tools from production."*

### Q2: How did you handle container security inside the Docker image?
> **Answer:** *"By default, Docker containers run as root (UID 0), which violates the principle of least privilege. In our Dockerfile, we explicitly provision a non-root system user and group (`appuser:appgroup`), recursively transfer ownership of the `/app` directory, and switch to `USER appuser` before the entry point. Even if an attacker were to exploit a vulnerability in the application, they cannot gain root access on the container or host."*

### Q3: Why is an Nginx reverse proxy used in front of the Spring Boot application?
> **Answer:** *"Nginx acts as a single, hardened entry point on port 80. The `calculator-api` container only exposes port 8080 internally within the private `calculator-net` bridge network; it is not bound to the host network interface. Furthermore, in `docker-compose.yml`, we configure `depends_on: { calculator-api: { condition: service_healthy } }`. This ensures Nginx only forwards traffic once Spring Boot Actuator confirms the application is fully initialized, preventing 502 Bad Gateway errors."*

### Q4: How is pipeline idempotency guaranteed on repeated runs?
> **Answer:** *"If a pipeline is triggered twice in rapid succession or re-run after failure, it must not fail due to container name collisions or port conflicts. In the Deploy stage, we execute `docker compose down --remove-orphans` before issuing `docker compose up -d --force-recreate`. This cleanly cleans up lingering state, recreates containers with the newly built image, and safely verifies health before terminating."*

### Q5: How are Docker Hub credentials protected in the pipeline?
> **Answer:** *"We never commit credentials to Git or hardcode them in the `Jenkinsfile`. Instead, we store the username and password in the Jenkins Credentials Store under ID `dockerhub-creds`. In the pipeline, we wrap the login step in `withCredentials([usernamePassword(...)])` and pipe the password directly into `docker login --password-stdin`. This masks the secret in all Jenkins console logs and wipes the credentials from environment variables immediately upon stage completion."*

---
*Ready for live presentation in Class 17.*
