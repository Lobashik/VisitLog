FROM node:18-alpine AS builder

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm i --legacy-peer-deps

COPY . .

RUN npm run dev