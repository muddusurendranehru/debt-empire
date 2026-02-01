#!/bin/bash
# Push Debt Empire v2.0 to GitHub

echo "=================================="
echo "PUSHING TO GITHUB"
echo "=================================="

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "Initializing git repository..."
    git init
fi

# Add all files
echo "Adding files..."
git add .

# Check if there are changes
if git diff --staged --quiet; then
    echo "No changes to commit."
else
    # Commit
    echo "Committing changes..."
    git commit -m "Initial commit: Debt Empire v2.0 full-stack application

- FastAPI backend (port 8000)
- Next.js frontend (port 3000)
- 8-step monthly ritual CLI
- Safety checks and validation
- One-click startup scripts"
fi

# Check if remote exists
if git remote get-url origin > /dev/null 2>&1; then
    echo "Remote 'origin' already exists."
else
    echo "Adding remote 'origin'..."
    git remote add origin https://github.com/muddusurendranehru/debt-empire.git
fi

# Push to GitHub
echo "Pushing to GitHub..."
git branch -M main
git push -u origin main

echo ""
echo "=================================="
echo "SUCCESS!"
echo "=================================="
echo "Repository: https://github.com/muddusurendranehru/debt-empire"
echo ""
