# ============================================================
# Stage 1: Build Application (Maven + JDK 17)
# ============================================================
FROM maven:3.9.6-eclipse-temurin-17-alpine AS builder

WORKDIR /build

# Leverage Docker layer caching: resolve dependencies before copying source
COPY pom.xml .
RUN mvn dependency:go-offline -B

# Copy application source code
COPY src ./src

# Compile and package application (skip tests as CI runs them separately)
RUN mvn clean package -DskipTests -B

# ============================================================
# Stage 2: Production Runtime (Minimal Temurin JRE 17 Alpine)
# ============================================================
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Install curl for container health check probes
# Create non-root system user and group for container security compliance
RUN apk add --no-cache curl \
    && addgroup -S appgroup \
    && adduser -S appuser -G appgroup

# Copy executable fat-JAR from the builder stage
COPY --from=builder /build/target/*.jar /app/app.jar

# Set ownership of the application directory to non-root user
RUN chown -R appuser:appgroup /app

# Run container as non-root user
USER appuser

# Expose Spring Boot default port
EXPOSE 8080

# Configure health check probe using Spring Actuator
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
  CMD curl -f http://localhost:8080/actuator/health || exit 1

# Launch the Spring Boot application
ENTRYPOINT ["java", "-jar", "/app/app.jar"]
