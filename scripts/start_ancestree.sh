#!/bin/bash
# AncesTree Startup Script
# This script starts AncesTree using Docker

echo "🌳 Starting AncesTree..."
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker is not installed"
    echo ""
    echo "Please install Docker Desktop from:"
    echo "https://www.docker.com/products/docker-desktop"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "❌ Error: Docker is not running"
    echo ""
    echo "Please start Docker Desktop and try again"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

echo "✅ Docker is ready"
echo ""

# Start Docker Compose
echo "🚀 Starting services..."
echo "This may take a few minutes on first run..."
echo ""

docker-compose up -d

# Wait for services to be ready
echo ""
echo "⏳ Waiting for services to start..."
sleep 10

# Check if services are running
if docker-compose ps | grep -q "Up"; then
    echo ""
    echo "✅ AncesTree is running!"
    echo ""
    echo "Opening in your browser..."
    echo ""

    # Open browser
    if command -v open &> /dev/null; then
        open http://localhost:3000
    elif command -v xdg-open &> /dev/null; then
        xdg-open http://localhost:3000
    else
        echo "Please open http://localhost:3000 in your browser"
    fi

    echo ""
    echo "📝 Access points:"
    echo "   - Application: http://localhost:3000"
    echo "   - API Documentation: http://localhost:8000/docs"
    echo ""
    echo "To stop AncesTree, run: ./stop_ancestree.sh"
    echo "Or run: docker-compose down"
    echo ""
else
    echo ""
    echo "❌ Error: Services failed to start"
    echo ""
    echo "View logs with: docker-compose logs"
    echo ""
fi
