#!/bin/bash
# AncesTree Stop Script
# This script stops AncesTree services

echo "🛑 Stopping AncesTree..."
echo ""

docker-compose down

echo ""
echo "✅ AncesTree has been stopped"
echo ""
echo "Your data is safe and will be available next time you start"
echo ""
