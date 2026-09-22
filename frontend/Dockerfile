# syntax=docker/dockerfile:1
FROM nginx:1.27-alpine

COPY frontend/nginx.conf /etc/nginx/nginx.conf
COPY frontend/index.html /usr/share/nginx/html/index.html
COPY frontend/images /usr/share/nginx/html/images

EXPOSE 80
