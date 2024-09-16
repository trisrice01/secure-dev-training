#john:mariam

FROM php:8.0-apache
WORKDIR /var/www/html
COPY index.php index.php
COPY menu.html menu.html
COPY home.html home.html
COPY style.css style.css
COPY admin admin/
ENV APACHE_RUN_USER www-data
ENV APACHE_RUN_GROUP www-data
ENV APACHE_LOG_DIR /var/log/apache2
RUN apt update && apt install openssh-server sudo -y
RUN useradd -rm -d /home/john -s /bin/bash -u 1001 john
RUN echo 'john:mariam' | chpasswd
RUN echo 'l4zy_l0c4al_file_1nclusi0n' > /home/john/flag
RUN service ssh start
EXPOSE 80
EXPOSE 22
ADD ./startup.sh /opt/startup.sh
RUN chmod +x /opt/startup.sh
ENTRYPOINT ["/opt/startup.sh"]