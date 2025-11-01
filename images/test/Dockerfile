from horsecatdog/bedrock:latest

ARG PROJECT
ARG THEME
ARG DB_NAME
ARG DB_USER
ARG DB_PASSWORD
ARG WP_VERSION

ENV PROJECT_NAME=$PROJECT
ENV THEME_NAME=$THEME
ENV BEDROCK_ROOT=/www/srv
ENV PROJECT_ROOT=/www/srv/$PROJECT
ENV THEME_ROOT=/www/srv/$PROJECT/web/app/themes/$THEME

COPY ./scripts /app/scripts
RUN bash /app/scripts/install_wp_tests_custom.sh $DB_NAME $DB_USER $DB_PASS db $PROJECT WP_VERSION


ENTRYPOINT ["bash", "/app/scripts/entrypoint.sh"]
