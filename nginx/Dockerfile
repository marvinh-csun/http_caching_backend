FROM nginx:1.13-alpine
USER 0
RUN mkdir -p /tmp/nginx/cache
USER $CONTINAER_USER_ID
COPY default.conf /etc/nginx/conf.d/default.conf