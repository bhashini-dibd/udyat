
# ---- build stage ----
FROM docker.io/maven:3.9-eclipse-temurin-11 AS build
WORKDIR /src

COPY pom.xml .
RUN mvn -q -DskipTests dependency:go-offline

COPY . .
RUN mvn -q -DskipTests clean package

# Find the first real app jar anywhere under */target and normalize the name
# Excludes sources/javadoc/original jars.
RUN sh -lc 'set -e; \
  JAR=$(find . -path "*/target/*.jar" \
        ! -name "*sources.jar" \
        ! -name "*javadoc.jar" \
        ! -name "*original*.jar" \
        | head -n1); \
  echo "Using JAR: $JAR"; \
  cp "$JAR" /src/app.jar'

# ---- runtime stage ----
FROM docker.io/eclipse-temurin:11-jre-jammy
RUN groupadd -r appgroup && useradd -r -g appgroup appuser && mkdir /app
WORKDIR /app

COPY --from=build /src/app.jar /app/app.jar

RUN chown -R appuser:appgroup /app
USER appuser

ENTRYPOINT ["java","-jar","/app/app.jar"]
