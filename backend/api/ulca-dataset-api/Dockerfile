# ---- Build stage ----
FROM docker.io/maven:3.9.7-eclipse-temurin-11 AS build
WORKDIR /src

# Copy Maven descriptor first and warm the cache
COPY pom.xml .
RUN mvn -q -B -DskipTests dependency:go-offline

# Copy sources and build
COPY src ./src
RUN mvn -B -DskipTests package

# ---- Runtime stage ----
FROM docker.io/eclipse-temurin:11-jre-jammy
# Create non-root user
RUN groupadd -r appgroup && useradd -r -g appgroup appuser && mkdir /app && chown -R appuser:appgroup /app
USER appuser
WORKDIR /app

# Copy the built JAR from the build stage (exactly one file should match)
COPY --from=build /src/target/*.jar /app/ulca-dataset-api.jar

ENTRYPOINT ["java","-jar","/app/ulca-dataset-api.jar"]

