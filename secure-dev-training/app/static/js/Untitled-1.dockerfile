FROM ubuntu:latest
RUN apt update && \
    apt install -y php apache2 && \
    apt clean
RUN mkdir -p /var/www/html
WORKDIR /var/www/html
COPY index.php index.php
CMD ["apachectl", "-D", "FOREGROUND"]
