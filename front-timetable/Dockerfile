FROM node:9.11.1

RUN npm install
RUN npm i -g npm to update

RUN npm install --global nodemon
RUN npm install --quiet --global vue-cli

RUN mkdir -p /front-timetable

COPY ./package.json /front-timetable/package.json

WORKDIR /front-timetable

RUN npm install --quiet
RUN npm i
