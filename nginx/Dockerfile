FROM nginx:1.21-alpine

# Удаляем стандартную конфигурацию
RUN rm /etc/nginx/conf.d/default.conf

# Копируем кастомные конфигурационные файлы
COPY nginx.conf /etc/nginx/nginx.conf
COPY servers/proxy_params /etc/nginx/servers/proxy_params
COPY servers/site.conf /etc/nginx/servers/site.conf
