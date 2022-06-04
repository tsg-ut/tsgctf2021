FROM node:14-slim

WORKDIR /app
ADD . /app
RUN npm install

ENTRYPOINT ["npx", "ts-node", "solver.ts"]

