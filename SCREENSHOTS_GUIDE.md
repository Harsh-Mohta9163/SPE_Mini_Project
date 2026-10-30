# 📸 Screenshots Guide & Submission Checklist

**Course:** CSE 816 — Software Production Engineering  
**Institution:** IIIT Bangalore  
**Student:** Harsh Mohta (`Harsh-Mohta9163`)  
**Project:** End-to-End CI/CD Pipeline for a Calculator REST API  

---

## 🎯 Evaluation Rubric Focus (1.0 Mark)
According to **Section 5 (Deliverables)** of the project specification, the following screenshots must be captured and included in the submission / demo folder:

1. **A green Jenkins pipeline run** showing all 6 stages passing
2. **Email notification** received upon successful build
3. **`docker ps` / `docker compose ps`** showing healthy running containers
4. **Sample API responses** across all endpoints including HTTP 400 error handling
5. **GitHub repository overview** showing progressive commit history, feature branches, and pull requests

---

## 📋 Screenshot Capture Checklist

### 1. Green Jenkins Pipeline Run (`screenshots/01_jenkins_pipeline_success.png`)
* **Where to capture:** Jenkins Web UI → Job `calculator-devops-pipeline` → Main Pipeline Overview or Blue Ocean view.
* **What must be visible:**
  - Build number (e.g. `#1`, `#2`, etc.) with green status ball
  - All 6 declarative stages displayed in green:
    1. `Checkout`
    2. `Build`
    3. `Test` (with test count badge e.g. "22 tests")
    4. `Docker Build`
    5. `Push`
    6. `Deploy`
  - Total pipeline duration (e.g., ~1m 30s)
  - GitHub commit SHA and author (`Harsh-Mohta9163`)

---

### 2. Email Notification (`screenshots/02_email_notification.png`)
* **Where to capture:** Email inbox of `mohta.harsh9163@gmail.com` (or local mail client).
* **What must be visible:**
  - Sender: `Jenkins <jenkins@...>`
  - Subject: `SUCCESS: Jenkins Build #<N> - Calculator REST API`
  - Body containing:
    - Build number, Build URL, Docker Image tag
    - Docker Hub URL link
    - Health endpoint URL (`http://localhost/actuator/health`)
    - Pipeline stages checklist (`[✓] 1. Checkout ... [✓] 6. Deploy`)

---

### 3. Running Docker Containers (`screenshots/03_docker_containers_healthy.png`)
* **Where to capture:** Terminal / PowerShell command prompt.
* **Commands to run:**
  ```bash
  docker compose ps
  # or
  docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}\t{{.Image}}"
  ```
* **What must be visible:**
  - `calculator-api` container running with status `Up ... (healthy)`
  - `calculator-nginx` container running with port `0.0.0.0:80->80/tcp`
  - Network: connected to `calculator-net`

---

### 4. Sample API Responses (`screenshots/04_api_responses_curl.png`)
* **Where to capture:** Terminal executing the automated smoke test script or individual `curl` commands.
* **Commands to run:**
  ```bash
  # Execute automated test suite
  python scripts/smoke_test.py
  # or run individually:
  curl "http://localhost/actuator/health"
  curl "http://localhost/api/v1/add?a=10&b=20"
  curl "http://localhost/api/v1/subtract?a=45&b=15"
  curl "http://localhost/api/v1/multiply?a=6&b=7"
  curl "http://localhost/api/v1/divide?a=100&b=4"
  curl "http://localhost/api/v1/divide?a=10&b=0"
  ```
* **What must be visible:**
  - Correct JSON outputs for arithmetic operations:
    - `{"operation":"add","a":10.0,"b":20.0,"result":30.0}`
    - `{"operation":"subtract","a":45.0,"b":15.0,"result":30.0}`
    - `{"operation":"multiply","a":6.0,"b":7.0,"result":42.0}`
    - `{"operation":"divide","a":100.0,"b":4.0,"result":25.0}`
  - Structured HTTP 400 JSON error for division by zero:
    - `{"error":"Division by zero is not allowed","a":10.0,"b":0.0}`
  - Actuator health status:
    - `{"status":"UP"}`

---

### 5. GitHub Repository & Commit History (`screenshots/05_github_commits_and_prs.png`)
* **Where to capture:** GitHub web page for `Harsh-Mohta9163/SPE_Mini_Project`.
* **What must be visible:**
  - Progressive commit history (no single "final commit")
  - Merged Pull Requests:
    - `PR #1: feature/spring-boot-api -> main`
    - `PR #2: feature/docker-and-compose -> main`
    - `PR #3: feature/jenkins-and-pipeline-deliverables -> main`
  - Clean repository root containing `Dockerfile`, `docker-compose.yml`, `Jenkinsfile`, `pom.xml`, `README.md`, etc.

---

## 🗂️ Suggested Directory Layout for Screenshots

Place your captured image files in the `screenshots/` directory:
```
screenshots/
  ├── 01_jenkins_pipeline_success.png
  ├── 02_email_notification.png
  ├── 03_docker_containers_healthy.png
  ├── 04_api_responses_curl.png
  └── 05_github_commits_and_prs.png
```

These screenshots can be directly referenced in your submission bundle or shown on screen during your Class 17 live evaluation.
