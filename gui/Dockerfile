# Use Node.js for building the frontend
FROM node:20

# Set the working directory inside the container
WORKDIR /app

# Copy everything in gui/ into the container
COPY . .

# Install dependencies and build the app
RUN npm install
RUN npm run build

# Install `serve` to host the static site
RUN npm install -g serve

# Expose the port you'll serve the frontend on
EXPOSE 3000

# Serve the built app
CMD ["serve", "-s", "dist", "-l", "3000"]
