#!/usr/bin/env python3
"""Generates IMT2023106_Harsh_Mohta.pdf (CSE 816 mini-project report).

Structure: title block, 1 Overview, 2 Pipeline architecture, 3 Application,
4 Pipeline stages, 5 Containerization and deployment, 6 Version control,
7 Challenges faced, Appendix: Screenshots.

Run from the repository root:  python scripts/generate_pdf_report.py
"""
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.graphics.shapes import Drawing, Line, Polygon, Rect, String
from reportlab.platypus import (Image, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate,
                                Spacer, Table, TableStyle)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOTS = os.path.join(ROOT, "screenshots")
OUT = os.path.join(ROOT, "IMT2023106_Harsh_Mohta.pdf")

NAME = "Harsh Mohta"
ROLL = "IMT2023106"
DATE = "30 October 2026"
REPO = "https://github.com/Harsh-Mohta9163/SPE_Mini_Project"
HUB = "https://hub.docker.com/r/harsh9163/calculator-api"

BLUE = colors.HexColor("#1F4E79")
GREY = colors.HexColor("#555555")
LIGHT = colors.HexColor("#E8EEF5")

ss = getSampleStyleSheet()
body = ParagraphStyle("body", parent=ss["BodyText"], fontName="Helvetica", fontSize=9, leading=12)
title = ParagraphStyle("title", parent=body, fontName="Helvetica-Bold", fontSize=17, leading=21,
                       alignment=1, textColor=BLUE)
meta = ParagraphStyle("meta", parent=body, fontSize=8.5, leading=11, alignment=1, textColor=GREY)
h1 = ParagraphStyle("h1", parent=body, fontName="Helvetica-Bold", fontSize=12, leading=15,
                    textColor=BLUE, spaceBefore=8, spaceAfter=3)
cell = ParagraphStyle("cell", parent=body, fontSize=8, leading=10)
cellb = ParagraphStyle("cellb", parent=cell, fontName="Helvetica-Bold")
code = ParagraphStyle("code", parent=cell, fontName="Courier", fontSize=7.5)
cap = ParagraphStyle("cap", parent=body, fontSize=8.5, leading=11, alignment=1, textColor=GREY,
                     spaceBefore=2, spaceAfter=8)


def P(t, s=cell):
    return Paragraph(t, s)


def table(rows, widths, header=True):
    data = [[P(c, cellb if (header and i == 0) else cell) if isinstance(c, str) else c for c in r]
            for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    st = [("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#B8C4D2")),
          ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
          ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5)]
    if header:
        st.append(("BACKGROUND", (0, 0), (-1, 0), LIGHT))
    t.setStyle(TableStyle(st))
    return t


def box(d, x, y, w, h, line1, line2="", fill=colors.white, stroke=colors.HexColor("#444444")):
    d.add(Rect(x, y, w, h, rx=4, ry=4, fillColor=fill, strokeColor=stroke, strokeWidth=0.8))
    if line2:
        d.add(String(x + w / 2, y + h - 12, line1, textAnchor="middle", fontName="Helvetica-Bold", fontSize=7.5))
        d.add(String(x + w / 2, y + 6, line2, textAnchor="middle", fontName="Helvetica", fontSize=6.5,
                     fillColor=GREY))
    else:
        d.add(String(x + w / 2, y + h / 2 - 3, line1, textAnchor="middle", fontName="Helvetica-Bold", fontSize=7.5))


def arrow(d, x1, y1, x2, y2, label="", lx=None, ly=None):
    d.add(Line(x1, y1, x2, y2, strokeColor=colors.HexColor("#444444"), strokeWidth=0.8))
    # arrow head
    import math
    a = math.atan2(y2 - y1, x2 - x1)
    s = 4.5
    d.add(Polygon([x2, y2, x2 - s * math.cos(a - 0.4), y2 - s * math.sin(a - 0.4),
                   x2 - s * math.cos(a + 0.4), y2 - s * math.sin(a + 0.4)],
                  fillColor=colors.HexColor("#444444"), strokeColor=colors.HexColor("#444444")))
    if label:
        d.add(String(lx if lx is not None else (x1 + x2) / 2, ly if ly is not None else (y1 + y2) / 2 + 3,
                     label, textAnchor="middle", fontName="Helvetica-Oblique", fontSize=6.5, fillColor=GREY))


def architecture():
    d = Drawing(500, 215)
    box(d, 5, 175, 105, 32, "Developer", "feature branch + PR")
    box(d, 190, 175, 105, 32, "GitHub", "SPE_Mini_Project repo")
    box(d, 385, 175, 110, 32, "Public tunnel", "webhook URL for Jenkins")
    arrow(d, 110, 191, 190, 191, "git push / merge")
    arrow(d, 295, 191, 385, 191, "webhook")
    # Jenkins container
    d.add(Rect(5, 80, 490, 78, rx=5, ry=5, fillColor=LIGHT, strokeColor=BLUE, strokeWidth=1))
    d.add(String(12, 147, "Jenkins (Windows service): declarative Jenkinsfile, trigger: githubPush()",
                 fontName="Helvetica-Bold", fontSize=7.5, fillColor=BLUE))
    stages = [("Checkout", "checkout scm"), ("Build", "mvn package"), ("Test", "mvn test + junit"),
              ("Docker Build", "tag :BUILD_NUMBER"), ("Push", "Docker Hub login"), ("Deploy", "compose up -d")]
    x = 12
    for n, sub in stages:
        box(d, x, 100, 72, 34, n, sub)
        x += 79
    d.add(String(12, 86, "post { success / failure }  ->  mail", fontName="Helvetica", fontSize=7, fillColor=GREY))
    arrow(d, 440, 175, 440, 158)
    # bottom row
    box(d, 5, 5, 105, 38, "Email notification", "SMTP: SUCCESS / FAILED #N")
    box(d, 175, 5, 115, 38, "Docker Hub", "harsh9163/calculator-api")
    d.add(Rect(325, 2, 170, 48, rx=5, ry=5, fillColor=colors.HexColor("#E6F4E6"),
               strokeColor=colors.HexColor("#3A7D3A"), strokeWidth=0.8))
    d.add(String(331, 40, "Compose stack (network calculator-net)", fontName="Helvetica-Bold", fontSize=6.5,
                 fillColor=colors.HexColor("#2C5F2C")))
    box(d, 333, 6, 70, 28, "nginx", "host :80")
    box(d, 415, 6, 72, 28, "calculator-api", ":8080 health")
    arrow(d, 40, 80, 40, 43, "on result", 58, 58)
    arrow(d, 232, 80, 232, 43, "push image", 262, 58)
    arrow(d, 410, 80, 410, 50, "deploy :N", 436, 62)
    return d


# Fraction of each screenshot's height to keep (trims blank terminal area; originals untouched).
CROP = {"A2_docker_ps_healthy.png": 0.25, "A3_api_responses_curl.png": 0.78}


def fit_image(path, max_w, max_h):
    from io import BytesIO
    from PIL import Image as PILImage
    im = PILImage.open(path).convert("RGB")
    keep = CROP.get(os.path.basename(path))
    if keep:
        im = im.crop((0, 0, im.width, int(im.height * keep)))
    buf = BytesIO()
    im.save(buf, "PNG")
    buf.seek(0)
    k = min(max_w / im.width, max_h / im.height)
    return Image(buf, width=im.width * k, height=im.height * k)


def shot(fname, caption, max_h=215 * mm / 1.0):
    p = os.path.join(SHOTS, fname)
    return KeepTogether([fit_image(p, 170 * mm, max_h), Paragraph(caption, cap)])


def footer(c, doc):
    c.saveState()
    c.setFont("Helvetica", 7.5)
    c.setFillColor(GREY)
    c.line(18 * mm, 13 * mm, A4[0] - 18 * mm, 13 * mm)
    c.drawString(18 * mm, 9 * mm, "CSE 816 Software Production Engineering - Mini-Project")
    c.drawRightString(A4[0] - 18 * mm, 9 * mm, "Page %d" % doc.page)
    c.restoreState()


def build():
    doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm,
                            topMargin=14 * mm, bottomMargin=18 * mm,
                            title="End-to-End CI/CD Pipeline for a Calculator REST API", author=NAME)
    W = A4[0] - 36 * mm
    s = []

    s += [Paragraph("End-to-End CI/CD Pipeline for a Calculator REST API", title),
          Paragraph("CSE 816 Software Production Engineering - Mini-Project &nbsp;|&nbsp; %s (%s) &nbsp;|&nbsp; %s"
                    % (NAME, ROLL, DATE), meta),
          Paragraph("Repository: <link href='%s' color='#1F4E79'>%s</link> &nbsp;|&nbsp; Image: "
                    "<link href='%s' color='#1F4E79'>%s</link>" % (REPO, REPO, HUB, HUB), meta)]

    s += [Paragraph("1. Overview", h1),
          Paragraph("A Spring Boot 3.3.4 (Java 17, Maven) REST service performs add, subtract, multiply and divide and "
                    "returns JSON. Every push to <b>main</b> on GitHub triggers a declarative Jenkins pipeline through a "
                    "webhook. The pipeline builds and tests the code, builds a multi-stage Docker image tagged with the "
                    "Jenkins build number, pushes it to Docker Hub and deploys it with Docker Compose behind an Nginx "
                    "reverse proxy, then verifies the deployment with a smoke test against the health endpoint. An email "
                    "reports success or failure. A code change reaches a running, health-checked deployment with no manual "
                    "steps (build #7 took 1 min 24 s end to end).", body)]

    s += [Paragraph("2. Pipeline architecture", h1), architecture(),
          Paragraph("Figure 1: Flow from a developer push to a health-checked deployment. Shaded green: containers "
                    "started by the Deploy stage.", cap)]

    s += [Paragraph("3. Application", h1),
          Paragraph("The code is split into layers: <b>CalculatorController</b> (HTTP only, constructor-injected service), "
                    "<b>CalculatorService</b> (the arithmetic, no web code), the DTOs <b>CalculatorResponse</b> and "
                    "<b>ErrorResponse</b> for the JSON shapes, and a <b>GlobalExceptionHandler</b> "
                    "(<i>@RestControllerAdvice</i>) that maps a custom <b>DivisionByZeroException</b>, missing and "
                    "mistyped parameters to HTTP 400. Spring Boot Actuator exposes <b>/actuator/health</b>, which "
                    "Docker Compose and the Deploy stage use.", body), Spacer(1, 4),
          table([["Request", "Response"],
                 ["GET /api/v1/add?a=10&amp;b=20", '200 {"operation":"add","a":10.0,"b":20.0,"result":30.0} '
                  "(subtract, multiply, divide alike)"],
                 ["GET /api/v1/divide?a=10&amp;b=0", '400 {"error":"Division by zero is not allowed","a":10.0,"b":0.0}'],
                 ["GET /api/v1/add?a=5", '400 {"error":"Missing required parameter: b", ...}'],
                 ["GET /api/v1/add?a=abc&amp;b=5", "400 {\"error\":\"Invalid value for parameter 'a': must be a number\", ...}"],
                 ["GET /actuator/health", '200 {"status":"UP", ...}']],
                [W * 0.36, W * 0.64]), Spacer(1, 4),
          Paragraph("<b>Tests (22, all passing):</b> 13 JUnit 5 unit tests for the service, covering every operation "
                    "plus divide by zero; and 9 Spring MVC integration tests (<i>MockMvc</i>) that send real requests "
                    "through the controller and exception handler and check status codes and JSON fields. Surefire "
                    "writes JUnit XML to <i>target/surefire-reports</i>, which Jenkins publishes.", body)]

    s += [Paragraph("4. Pipeline stages (Jenkinsfile)", h1),
          table([["Stage", "What it does", "Key detail"],
                 ["Checkout", "Fetches the commit that triggered the build.",
                  "<i>checkout scm</i>; the job uses Pipeline script from SCM, so the pipeline is versioned with the code."],
                 ["Build", "Compiles and packages the executable JAR.",
                  "<i>mvn clean package -DskipTests -B</i>; clean gives a fresh build in the reused workspace."],
                 ["Test", "Runs all tests, publishes results.",
                  "<i>mvn test -B</i>; a failing test makes Maven exit non-zero, which fails the stage. "
                  "<i>post { always { junit } }</i> publishes the XML."],
                 ["Docker Build", "Builds the image from the multi-stage Dockerfile.",
                  "Tagged <i>harsh9163/calculator-api:${BUILD_NUMBER}</i> and <i>:latest</i>."],
                 ["Push", "Publishes both tags to Docker Hub.",
                  "<i>withCredentials</i> reads the access token from the Jenkins Credentials store; "
                  "<i>--password-stdin</i> keeps it out of the logs."],
                 ["Deploy", "Starts the new version and verifies it.",
                  "<i>docker-compose up -d --force-recreate</i>, then <i>scripts/smoke_test.py</i> polls "
                  "/actuator/health and checks every endpoint through Nginx."],
                 ["post", "Notifies the developer.",
                  "<i>mail</i> sends SUCCESS or FAILED with the build number, image tag and console link; "
                  "<i>docker logout</i> always runs."]],
                [W * 0.13, W * 0.30, W * 0.57]), Spacer(1, 4),
          Paragraph("<b>Trigger:</b> <i>githubPush()</i>. GitHub posts to <i>/github-webhook/</i> on a publicly reachable "
                    "URL, since GitHub cannot reach localhost. Builds show &quot;Started by GitHub push by "
                    "Harsh-Mohta9163&quot;. <b>Idempotency:</b> <i>docker-compose up -d --force-recreate</i> replaces the "
                    "containers of the same Compose project each run, so re-running the pipeline never leaves a "
                    "half-deployed or duplicate stack.", body)]

    s += [Paragraph("5. Containerization and deployment", h1),
          Paragraph("<b>Dockerfile (multi-stage):</b> stage 1 (<i>maven:3.9.6-eclipse-temurin-17-alpine</i>) copies only "
                    "<i>pom.xml</i>, runs <i>dependency:go-offline</i>, then copies <i>src</i> and packages. Dependencies "
                    "form their own cached layer, so a code change rebuilds in seconds. Stage 2 "
                    "(<i>eclipse-temurin:17-jre-alpine</i>) creates a non-root system user <i>appuser</i>, copies only the "
                    "JAR, declares <i>EXPOSE 8080</i> and runs as <i>USER appuser</i>, with a <i>HEALTHCHECK</i> on "
                    "<i>/actuator/health</i>. The final image is about 109 MB compressed on Docker Hub and contains no "
                    "JDK, Maven or source code. <i>.dockerignore</i> excludes target/, .git/, docs and IDE files.", body),
          Spacer(1, 3),
          Paragraph("<b>docker-compose.yml:</b> two services on a user-defined bridge network <i>calculator-net</i>. "
                    "<i>calculator-api</i> has no published port, only <i>expose: 8080</i>, plus a health check, "
                    "<i>restart: unless-stopped</i> and environment variables (<i>SPRING_PROFILES_ACTIVE=prod</i>). "
                    "<i>nginx:alpine</i> is the only public entry point (host 80 to container 80) and reverse-proxies to "
                    "<i>calculator-api:8080</i> using Docker's service-name DNS. It starts only once the API is healthy "
                    "(<i>depends_on: condition: service_healthy</i>). One <i>docker compose up</i> starts the whole stack.",
                    body)]

    s += [Paragraph("6. Version control", h1),
          Paragraph("Work was done on feature branches (<i>feature/spring-boot-api</i>, <i>feature/docker-and-compose</i>, "
                    "<i>feature/jenkins-and-pipeline-deliverables</i>) and merged into <i>main</i> through GitHub pull "
                    "requests #1, #2 and #3, for a history of more than 30 small, descriptive commits. The Java/Maven "
                    ".gitignore excludes target/ and IDE files. No secrets are in the repository: the Docker Hub access "
                    "token lives only in the Jenkins Credentials store.", body)]

    s += [Paragraph("7. Challenges faced", h1),
          table([["Problem", "Root cause", "Resolution"],
                 ["Push failed: <i>unauthorized: incorrect username or password</i>",
                  "Docker Hub username is <i>harsh9163</i>, but the credential and image name used <i>harshmohta9163</i>; "
                  "the stored username also had a leading space.",
                  "Fixed the image namespace, created a Read &amp; Write access token and re-saved "
                  "<i>dockerhub-creds</i>; tested with <i>docker login</i> by hand first."],
                 ["Every build re-downloaded all Maven dependencies (~47 s)",
                  "<i>docker image prune -f</i> in the post step deleted the cached builder layers after each run.",
                  "Removed the prune; Docker Build dropped to about 1 s (see A1)."],
                 ["<i>docker login -p</i> warned that passing the token on the command line is insecure",
                  "The token was a command-line argument (and <i>echo | docker login</i> in cmd can add a trailing space).",
                  "Used <i>echo &quot;$DH_PASS&quot; | docker login --password-stdin</i> inside <i>withCredentials</i>."],
                 ["Port conflict on 8080",
                  "Jenkins already listens on 8080, the same default port as the Spring Boot app.",
                  "Only Nginx publishes a host port (80); the API is exposed inside the network only."],
                 ["Email notification failed with a connection error",
                  "Jenkins had no SMTP server configured (empty host, default port 25); Gmail also needs SSL and "
                  "an app password, not the account password.",
                  "Set <i>smtp.gmail.com</i>, port 465 with SSL and a Gmail app password under Manage Jenkins, "
                  "System, E-mail Notification; success and failure mails now arrive."]],
                [W * 0.27, W * 0.38, W * 0.35])]

    s += [PageBreak(), Paragraph("Appendix: Screenshots", h1),
          shot("A1_jenkins_stage_view_build7.png",
               "A1. Jenkins Stage View: build #7 green through all stages including Deploy (1 min 24 s).", 90 * mm),
          shot("A2_docker_ps_healthy.png",
               "A2. docker ps after the pipeline: calculator-api (healthy) behind calculator-nginx on host port 80.", 60 * mm),
          shot("A3_api_responses_curl.png",
               "A3. API responses through Nginx: health, four operations (200) and three error cases (400).", 110 * mm),
          shot("A4_dockerhub_tags.png",
               "A4. Docker Hub repository harsh9163/calculator-api with build-number (7) and latest tags.", 100 * mm),
          shot("A5_email_build7_success.png",
               "A5. Email notification for a successful build (#7).", 70 * mm),
          shot("A6_email_build6_failed.png",
               "A6. Email notification for a failed build (#6, the Deploy stage failure described in section 7).", 40 * mm)]

    doc.build(s, onFirstPage=footer, onLaterPages=footer)
    print("Wrote", OUT)


if __name__ == "__main__":
    build()
