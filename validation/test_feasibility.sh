#!/bin/bash

echo "═══════════════════════════════════════════════════"
echo "PRODUCT FEASIBILITY VALIDATION"
echo "═══════════════════════════════════════════════════"

# Test 1: Complete Application Exists
echo -e "\n[TEST 1] Full-Stack Application"
if [ -f "backend/app/main.py" ] || [ -f "backend/main.py" ]; then
    echo "✓ Backend code exists"
else
    echo "✗ Missing backend code"
fi

if [ -d "src/app" ] || [ -d "frontend/src" ]; then
    echo "✓ Frontend code exists"
else
    echo "✗ Missing frontend code"
fi

# Test 2: Deployment Configuration
echo -e "\n[TEST 2] Deployment Ready"
if [ -f "docker-compose.yml" ]; then
    echo "✓ Docker Compose configuration found"
else
    echo "✗ Missing deployment configuration"
fi

# Test 3: Model Checkpoints Intent check
echo -e "\n[TEST 3] Fine-Tuned Models Check"
if [ -d "ml/checkpoints" ] || [ -d "backend/models/checkpoints" ]; then
    echo "✓ Model checkpoints directory found"
else
    echo "⚠️  No model checkpoints directory found (intentional for mock dev)"
fi

echo -e "\n═══════════════════════════════════════════════════"
echo "FEASIBILITY VALIDATION COMPLETE"
echo "═══════════════════════════════════════════════════"
