# ---- Build stage ----
FROM docker.io/maven:3.9-eclipse-temurin-11 AS build
WORKDIR /src
COPY pom.xml .
# go offline to cache deps
RUN mvn -q -e -B -DskipTests dependency:go-offline
COPY . .
RUN mvn -q -e -B -DskipTests package

# ---- Runtime stage ----
FROM docker.io/eclipse-temurin:11-jre-jammy
RUN groupadd -r appgroup && useradd -r -g appgroup appuser
WORKDIR /app
COPY --from=build /src/target/*.jar /app/app.jar
USER appuser
ENTRYPOINT ["java","-jar","/app/app.jar"]

