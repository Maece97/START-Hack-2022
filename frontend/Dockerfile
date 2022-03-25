FROM node:14.17 AS development

WORKDIR /opt/app

ENV VUE_APP_API_URL=http://localhost:8080
ENV VUE_APP_WEBSOCKET_URL=ws://localhost:8080

COPY package.json yarn.lock tsconfig.json .eslintrc.js tailwind.config.js /opt/app/
RUN yarn
COPY src /opt/app/src

CMD yarn serve

# staging stage
FROM nginx:stable-alpine AS staging
RUN mkdir /app
COPY /dist /app
COPY /nginx.conf /etc/nginx/nginx.conf