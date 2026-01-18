# Stage 1: Build the static site
FROM python:3.11-slim as builder

WORKDIR /app

# Copy generation script and assets
COPY generate_site.py .
COPY style.css .

# Run the generation script
# We set DEMO_LIMIT=0 to ensure the full site is generated for production
ENV DEMO_LIMIT=0
RUN python generate_site.py

# Stage 2: Serve with Nginx
FROM nginx:alpine

# Remove default nginx static assets
RUN rm -rf /usr/share/nginx/html/*

# Copy generated site from builder stage
COPY --from=builder /app/site /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
