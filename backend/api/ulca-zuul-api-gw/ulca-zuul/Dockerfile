# Build stage
FROM docker.io/maven:3.9.6-eclipse-temurin-11 AS build
WORKDIR /src
COPY pom.xml .
COPY src ./src
RUN mvn -q -DskipTests clean package

# Runtime
FROM docker.io/eclipse-temurin:11-jre
WORKDIR /app
COPY --from=build /src/target/ulca-zuul-gw-0.0.1-SNAPSHOT.jar /app/app.jar
ENV SPRING_CONFIG_ADDITIONAL_LOCATION=file:/app/config/
COPY src/main/resources/application.properties /app/config/application.properties
EXPOSE 8080
ENTRYPOINT ["sh","-c","exec java $JAVA_OPTS -jar /app/app.jar"]

