#!/bin/bash

# KFH Rewards Tracker - Quick GitHub Setup Script
# This script helps you quickly set up the repository on GitHub

echo "🎯 KFH Rewards Tracker - GitHub Setup"
echo "======================================"
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    echo "   Visit: https://git-scm.com/downloads"
    exit 1
fi

echo "✅ Git is installed"
echo ""

# Get GitHub username
read -p "Enter your GitHub username: " GITHUB_USER

if [ -z "$GITHUB_USER" ]; then
    echo "❌ GitHub username is required"
    exit 1
fi

echo ""
read -p "Enter repository name (default: kfh-rewards-tracker): " REPO_NAME
REPO_NAME=${REPO_NAME:-kfh-rewards-tracker}

echo ""
echo "📦 Setting up repository: $GITHUB_USER/$REPO_NAME"
echo ""

# Initialize git if not already initialized
if [ ! -d .git ]; then
    echo "🔧 Initializing git repository..."
    git init
    echo "✅ Git initialized"
else
    echo "✅ Git repository already initialized"
fi

# Check if README.md exists
if [ ! -f README.md ]; then
    echo "❌ README.md not found. Are you in the correct directory?"
    exit 1
fi

echo ""
echo "🔗 Setting up remote..."

# Remove existing origin if it exists
git remote remove origin 2>/dev/null

# Add GitHub remote
git remote add origin "https://github.com/$GITHUB_USER/$REPO_NAME.git"
echo "✅ Remote added: https://github.com/$GITHUB_USER/$REPO_NAME.git"

echo ""
echo "📝 Preparing files for commit..."

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit - KFH Rewards Tracker" 2>/dev/null || echo "⚠️  No changes to commit (repository might already be set up)"

echo ""
echo "📤 Ready to push to GitHub!"
echo ""
echo "⚠️  IMPORTANT: Before running the push command:"
echo "   1. Go to GitHub.com and log in"
echo "   2. Create a new repository named: $REPO_NAME"
echo "   3. DON'T initialize with README, .gitignore, or license"
echo "   4. Come back here and press ENTER to continue"
echo ""
read -p "Press ENTER when you've created the GitHub repository..."

echo ""
echo "🚀 Pushing to GitHub..."

# Set main as default branch
git branch -M main

# Push to GitHub
if git push -u origin main; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo ""
    echo "🎉 Your repository is now live at:"
    echo "   https://github.com/$GITHUB_USER/$REPO_NAME"
    echo ""
    echo "📋 Next steps:"
    echo "   1. Enable GitHub Pages (Settings → Pages → Source: main → /docs)"
    echo "   2. Deploy backend to Heroku or Railway"
    echo "   3. Read GITHUB-SETUP.md for detailed instructions"
    echo ""
else
    echo ""
    echo "❌ Failed to push to GitHub"
    echo ""
    echo "Possible reasons:"
    echo "   1. Repository doesn't exist on GitHub"
    echo "   2. Authentication failed (you may need to configure Git credentials)"
    echo "   3. Repository already has content"
    echo ""
    echo "📖 For help, see: GITHUB-SETUP.md"
fi
