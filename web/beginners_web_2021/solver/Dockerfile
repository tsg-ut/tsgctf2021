FROM node:14-slim

WORKDIR /app
ADD . /app
RUN npm install

ENV NODE_OPTIONS --unhandled-rejections=strict

ENTRYPOINT ["npx", "ts-node", "solver.ts"]

