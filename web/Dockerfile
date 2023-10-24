FROM node:18.17.1-alpine

WORKDIR /app
COPY . /app

RUN yarn install --frozen-lockfile

RUN npm install

EXPOSE 3000

CMD yarn dev
