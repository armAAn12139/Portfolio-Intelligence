FROM openjdk:8-jdk-alpine
RUN apk update
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser
WORKDIR /home/appuser
COPY --chown=appuser:appgroup . .
RUN ./mvnw clean package -DskipTests
ADD target/spring-boot-docker.jar spring-boot-docker.jar
EXPOSE 8080
ENTRYPOINT ["java","-jar","spring-boot-docker.jar"]