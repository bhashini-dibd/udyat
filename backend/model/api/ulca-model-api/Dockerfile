
# ---------- Build stage ----------
FROM maven:3.9.6-eclipse-temurin-11 AS builder
WORKDIR /build
COPY pom.xml .
COPY src ./src
RUN mvn clean package -DskipTests

# ---------- Runtime stage ----------
FROM eclipse-temurin:11-jre-jammy
RUN groupadd -r appgroup && useradd -r -g appgroup appuser
WORKDIR /app
COPY --from=builder /build/target/*jar app.jar
USER appuser
EXPOSE 8080
ENTRYPOINT ["java","-jar","/app/app.jar"]

