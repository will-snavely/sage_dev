from horsecatdog/bedrock:latest

ARG PROJECT
ARG THEME

ENV PROJECT_NAME=$PROJECT
ENV THEME_NAME=$THEME
ENV BEDROCK_ROOT=/www/srv
ENV PROJECT_ROOT=/www/srv/$PROJECT
ENV THEME_ROOT=/www/srv/$PROJECT/web/app/themes/$THEME

COPY ./projects/$PROJECT /www/srv/$PROJECT/
COPY ./scripts /app/scripts
WORKDIR /www/srv/$PROJECT
RUN composer update && composer install 

WORKDIR /www/srv/$PROJECT/web/app/themes/$THEME
RUN composer update && \
    composer install && \
    npm install && \
    npm run build

RUN chown -R www-data:www-data /www/srv/$PROJECT

ENTRYPOINT ["bash", "/app/scripts/entrypoint.sh"]
