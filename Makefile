.PHONY: all build start test clean docker-up docker-down dev-frontend dev-backend help

all: build test

help:
	@echo "AI-Powered Learning Management System (Enterprise SaaS LMS)"
	@echo ""
	@echo "Targets:"
	@echo "  make build          Build both frontend and backend"
	@echo "  make start          Start the complete platform via Docker Compose"
	@echo "  make test           Run frontend and backend automated tests"
	@echo "  make docker-up      Start PostgreSQL (pgvector), Redis, Backend, and Frontend"
	@echo "  make docker-down    Stop all running containers"
	@echo "  make dev-frontend   Start Vite React development server"
	@echo "  make dev-backend    Start Spring Boot backend application"
	@echo "  make clean          Clean build artifacts"

build:
	cd frontend && npm install && npm run build
	cd backend && mvn clean package -DskipTests

start: docker-up

docker-up:
	docker compose up -d --build

docker-down:
	docker compose down -v

test:
	cd backend && mvn test
	cd frontend && npm test -- --watchAll=false

dev-frontend:
	cd frontend && npm run dev

dev-backend:
	cd backend && mvn spring-boot:run

clean:
	rm -rf frontend/dist backend/target
