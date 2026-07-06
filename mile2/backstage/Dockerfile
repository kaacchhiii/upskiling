# Backstage Dockerfile - Multi-stage build
FROM node:20-alpine AS base

# Install dependencies for native modules
RUN apk add --no-cache python3 make g++ git

WORKDIR /app

# ---- Dependencies ----
FROM base AS deps
COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile --network-timeout 300000

# ---- Builder ----
FROM base AS builder
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN yarn build

# ---- Runner ----
FROM node:20-alpine AS runner
WORKDIR /app

# Copy built artifacts
COPY --from=builder /app/packages/backend/dist ./packages/backend/dist
COPY --from=builder /app/packages/backend/dist/skeleton.tar.gz ./packages/backend/dist/skeleton.tar.gz
COPY --from=builder /app/app-config.yaml ./app-config.yaml

# Install only production dependencies
COPY package.json yarn.lock ./
RUN yarn install --production --frozen-lockfile --network-timeout 300000

# Non-root user
RUN addgroup -g 1000 backstage && \
    adduser -D -u 1000 -G backstage backstage && \
    chown -R backstage:backstage /app
USER backstage

EXPOSE 7007

CMD ["node", "packages/backend/dist/index.cjs"]