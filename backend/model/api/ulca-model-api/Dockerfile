FROM docker.io/openjdk:11.0.4-jre-slim

# create user/group
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

WORKDIR /app

# copy as root, then drop privileges
COPY target/ulca-model-api.jar /app/ulca-model-api.jar

USER appuser

EXPOSE 8080
ENTRYPOINT ["java","-jar","/app/ulca-model-api.jar"]

