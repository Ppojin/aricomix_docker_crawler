FROM nimmis/apache-php5:latest

# 언어 설정
ENV LANG ko_KR.UTF-8
ENV LANGUAGE ko_KR.UTF-8
ENV LC_ALL ko_KR.UTF-8

# TimeZone 설정
ENV TZ Asia/Seoul

RUN mkdir /var/www/comix-server
COPY ./song31-comix-server-9d2630a/handler.php /var/www/comix-server
COPY ./song31-comix-server-9d2630a/index.php /var/www/comix-server
COPY ./song31-comix-server-9d2630a/welcome.php /var/www/comix-server
COPY ./song31-comix-server-9d2630a/conf/httpd.conf-comix /etc/apache2/sites-enabled/httpd-comix.conf

# RUN mkdir /volume1
# RUN mkdir /volume1/comics
VOLUME ["/volume1/comics"]

# CMD ["apache2ctl", "start"]