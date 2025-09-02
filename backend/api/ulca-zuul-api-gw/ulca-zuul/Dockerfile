# Use your existing base (kept as-is)
FROM docker.io/openjdk:11.0

# Workdir
WORKDIR /app

# Copy the fat jar
COPY target/ulca-zuul-gw-0.0.1-SNAPSHOT.jar /app/app.jar

# Tell Spring Boot to also read configs from /app/config (takes precedence over the one inside the JAR)
ENV SPRING_CONFIG_ADDITIONAL_LOCATION=file:/app/config/

# (Optional) set active profile via build arg or env at runtime
ARG SPRING_PROFILES_ACTIVE=default
ENV SPRING_PROFILES_ACTIVE=${SPRING_PROFILES_ACTIVE}

# Copy your corrected application.properties into /app/config
# (If you prefer mounting via ConfigMap/volume at runtime, you can remove this COPY line.)
COPY src/main/resources/application.properties /app/config/application.properties

EXPOSE 8080
ENTRYPOINT ["sh","-c","exec java $JAVA_OPTS -jar /app/app.jar"]

