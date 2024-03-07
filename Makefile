# Makefile for simplifying build and run processes

# Project variables
PROJECT_NAME=my_fastapi_app
DOCKER_TAG=my_fastapi_app
HOST_PORT=8000
DOCKER_PORT=8000

# Uvicorn run command
run:
	uvicorn app.main:app --host 0.0.0.0 --port $(HOST_PORT) --reload

# Docker build command
build:
	docker build -t $(DOCKER_TAG) .

# Docker run command
start:
	docker run -d -p $(HOST_PORT):$(DOCKER_PORT) $(DOCKER_TAG)
	
# Help command to display callable targets
help:
	@echo "Available commands:"
	@echo "  run   - Run the FastAPI application using Uvicorn (must have uvicorn installed in python venv)\n"
	@echo "  build - Build the Docker image for the application (must have Docker daemon running)\n"
	@echo "  start - Run a Docker container from the image (only after running "make build")"
