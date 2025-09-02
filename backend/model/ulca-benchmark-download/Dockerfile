# ----------- Build stage -----------
FROM docker.io/maven:3.9-eclipse-temurin-11 AS build

# Set workdir inside container
WORKDIR /app

# Copy pom.xml and download dependencies first (better caching)
COPY pom.xml .
RUN mvn -B -q -DskipTests dependency:go-offline

# Copy the source code
COPY src ./src

# Package the jar (skip tests to speed up)
RUN mvn -B -q -DskipTests package

# ----------- Runtime stage -----------
FROM docker.io/openjdk:11.0.4-jre-slim

# Create non-root user
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

WORKDIR /app

# Copy the built jar from the build stage
COPY --from=build /app/target/*.jar /app/app.jar

USER appuser

ENTRYPOINT ["java", "-jar", "/app/app.jar"]

