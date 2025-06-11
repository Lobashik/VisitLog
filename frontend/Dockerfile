FROM node:18-alpine AS builder

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm --force install 

COPY . .

RUN npm run build

CMD ["npm", "start"]