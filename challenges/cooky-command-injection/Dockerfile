FROM php:8.0-apache
WORKDIR /var/www/html

COPY index.php index.php
RUN mkdir -p /var/www/html/backups
RUN echo "c00ky_c0mm4nd_1nj3cti0n" > /var/www/html/flag
run chown www-data:www-data /var/www/html/backups
EXPOSE 80
