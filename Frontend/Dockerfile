# Build stage
FROM node:18-alpine as builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy application code
COPY . .

# Build the application
RUN npm run build

# Development stage
FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy built application from builder
COPY --from=builder /app/dist ./dist

# Copy source files
COPY . .

# Expose port
EXPOSE 5173

# Run the development server
CMD ["npm", "run", "dev"]
