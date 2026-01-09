FROM python:3.11-slim

WORKDIR /app

# Copy only the essential files
COPY mini.py .
COPY server.py .

# Make server.py executable
RUN chmod +x server.py

# Expose the port
EXPOSE 8080

# Run the server by default
CMD ["python3", "server.py"]
