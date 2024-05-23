FROM node:14-alpine

WORKDIR /app

COPY public public
COPY src src

EXPOSE 8080

CMD ["npx", "http-server", "public"]
