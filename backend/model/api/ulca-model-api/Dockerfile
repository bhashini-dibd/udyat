MODEL-API
# ---------- Build stage ----------
FROM docker.io/maven:3.9.9-eclipse-temurin-11 AS builder
WORKDIR /build
COPY pom.xml .
COPY src ./src
RUN mvn clean package -DskipTests

# ---------- Runtime stage ----------
FROM docker.io/openjdk:11.0.4-jre-slim
RUN groupadd -r appgroup && useradd -r -g appgroup appuser
WORKDIR /app
COPY --from=builder /build/target/ulca-model-api.jar /app/ulca-model-api.jar
USER appuser
EXPOSE 8080
ENTRYPOINT ["java","-jar","/app/app.jar"]

