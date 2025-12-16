# GitHub Setup Guide for KFH Rewards Tracker

This guide walks you through setting up the KFH Rewards Tracker on GitHub with multiple deployment options.

## 📋 Table of Contents

1. [Initial GitHub Setup](#initial-github-setup)
2. [GitHub Pages Deployment](#github-pages-deployment)
3. [Heroku Deployment](#heroku-deployment)
4. [Railway Deployment](#railway-deployment)
5. [GitHub Actions Setup](#github-actions-setup)
6. [Adding Notifications](#adding-notifications)

---

## 1. Initial GitHub Setup

### Step 1: Create a New GitHub Repository

1. **Go to GitHub** and log in to your account
2. **Click the "+" icon** in the top right → "New repository"
3. **Fill in the details:**
   - Repository name: `kfh-rewards-tracker`
   - Description: "Real-time tracker for KFH Rewards deals"
   - Visibility: Public (or Private if you prefer)
   - ✅ Add a README file (we'll replace it)
   - ✅ Add .gitignore: Python
   - ✅ Choose a license: MIT
4. **Click "Create repository"**

### Step 2: Upload Files to GitHub

**Option A: Using GitHub Web Interface (Easiest)**

1. In your repository, click **"Add file"** → **"Upload files"**
2. **Drag and drop** all the files from the `kfh-repo` folder:
   - `kfh_backend.py`
   - `kfh-tracker-live.html`
   - `requirements.txt`
   - `README.md`
   - `SETUP-GUIDE.md`
   - `Procfile`
   - `runtime.txt`
   - `LICENSE`
   - `.gitignore`
3. **Also upload the folders:**
   - `.github/workflows/update-deals.yml`
   - `docs/index.html`
   - `data/.gitkeep`
4. **Commit changes** with message: "Initial commit - KFH Rewards Tracker"

**Option B: Using Git Command Line**

```bash
# Navigate to the kfh-repo folder
cd /path/to/kfh-repo

# Initialize git (if not already initialized)
git init

# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/kfh-rewards-tracker.git

# Add all files
git add .

# Commit
git commit -m "Initial commit - KFH Rewards Tracker"

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 3: Verify Upload

Visit your repository on GitHub and ensure all files are present:
- ✅ Root files (README.md, kfh_backend.py, etc.)
- ✅ `.github/workflows/` folder
- ✅ `docs/` folder
- ✅ `data/` folder

---

## 2. GitHub Pages Deployment

Host the frontend dashboard on GitHub Pages (free static hosting).

### Setup Steps:

1. **Go to your repository** on GitHub
2. **Click "Settings"** tab
3. **Scroll to "Pages"** in the left sidebar
4. **Configure GitHub Pages:**
   - Source: "Deploy from a branch"
   - Branch: `main`
   - Folder: `/docs`
   - Click **"Save"**

5. **Wait 2-3 minutes** for deployment

6. **Access your dashboard:**
   - URL: `https://YOUR_USERNAME.github.io/kfh-rewards-tracker/`

### Update API URL:

Since GitHub Pages only hosts static files, you need to deploy the backend separately (see Heroku or Railway sections below).

Once your backend is deployed, update the API URL in `docs/index.html`:

```html
<input type="text" id="apiUrl" value="https://your-backend-url.herokuapp.com">
```

Then commit and push the change.

---

## 3. Heroku Deployment

Deploy the backend API to Heroku (free tier available).

### Prerequisites:
- Heroku account (sign up at heroku.com)
- Heroku CLI installed

### Step 1: Install Heroku CLI

**Windows:**
Download from: https://devcenter.heroku.com/articles/heroku-cli

**Mac:**
```bash
brew tap heroku/brew && brew install heroku
```

**Linux:**
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

### Step 2: Login to Heroku

```bash
heroku login
```

### Step 3: Create Heroku App

```bash
# Navigate to your repository
cd /path/to/kfh-rewards-tracker

# Create app (choose a unique name)
heroku create kfh-rewards-tracker-YOUR_NAME

# Or let Heroku generate a random name
heroku create
```

### Step 4: Deploy to Heroku

```bash
# Push to Heroku
git push heroku main

# Check deployment logs
heroku logs --tail
```

### Step 5: Open Your App

```bash
heroku open
```

Your API should be live at: `https://your-app-name.herokuapp.com`

### Step 6: Test the API

Visit: `https://your-app-name.herokuapp.com/api/deals`

You should see JSON data with deal quantities.

### Step 7: Update Frontend

Update the API URL in your dashboard (GitHub Pages or local):

```html
<input type="text" id="apiUrl" value="https://your-app-name.herokuapp.com">
```

### Heroku Troubleshooting:

**Problem: App crashes after deployment**

Check logs:
```bash
heroku logs --tail
```

**Problem: "PORT already in use"**

The code already handles this - Heroku sets the PORT environment variable automatically.

**Problem: App sleeps after 30 minutes**

This is normal on Heroku free tier. The app will wake up on first request (takes ~10 seconds).

To prevent sleeping, consider:
- Upgrading to a paid dyno
- Using a service like UptimeRobot to ping your app every 25 minutes

---

## 4. Railway Deployment

Railway offers easier deployment than Heroku with a generous free tier.

### Step 1: Sign Up for Railway

1. Go to https://railway.app
2. Sign in with **GitHub**

### Step 2: Create New Project

1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. **Authorize Railway** to access your repositories
4. **Select your repository:** `kfh-rewards-tracker`

### Step 3: Configure Deployment

Railway automatically:
- ✅ Detects Python
- ✅ Installs dependencies from `requirements.txt`
- ✅ Runs `kfh_backend.py`

### Step 4: Get Your URL

1. Go to your project in Railway
2. Click **"Settings"**
3. Under **"Domains"**, click **"Generate Domain"**
4. Copy the generated URL (e.g., `kfh-tracker-production.up.railway.app`)

### Step 5: Update Frontend

Update the API URL in your dashboard:

```html
<input type="text" id="apiUrl" value="https://kfh-tracker-production.up.railway.app">
```

### Railway Advantages:

- ✅ No sleep on free tier
- ✅ Automatic deployments on git push
- ✅ Better free tier limits than Heroku
- ✅ Built-in monitoring

---

## 5. GitHub Actions Setup

Enable automated deal monitoring that runs every 10 minutes.

### Step 1: Enable GitHub Actions

1. Go to your repository on GitHub
2. Click the **"Actions"** tab
3. You should see the workflow: **"Monitor KFH Deals"**
4. If disabled, click **"Enable workflow"**

### Step 2: Trigger Manual Run

1. Click on **"Monitor KFH Deals"** workflow
2. Click **"Run workflow"** button
3. Select branch: `main`
4. Click **"Run workflow"**

### Step 3: Check Results

After the workflow runs:
1. Click on the workflow run
2. View the **Summary** tab to see deal status
3. Check the **"check-deals"** job for detailed logs

### What GitHub Actions Does:

- ✅ Runs every 10 minutes automatically
- ✅ Scrapes KFH website for deal quantities
- ✅ Saves data to `data/latest.json`
- ✅ Commits updated data to repository
- ✅ Sends notifications if deals go out of stock
- ✅ Shows summary in Actions tab

### View Historical Data:

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/kfh-rewards-tracker.git

# View historical data
cat data/latest.json
```

---

## 6. Adding Notifications

Configure notifications to be alerted when deals go out of stock.

### Option A: Discord Notifications

1. **Create Discord Webhook:**
   - Go to your Discord server
   - Server Settings → Integrations → Webhooks
   - Create webhook, copy URL

2. **Add to GitHub Secrets:**
   - Repository → Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `DISCORD_WEBHOOK`
   - Value: Your webhook URL
   - Click "Add secret"

3. **Uncomment in workflow:**
   Edit `.github/workflows/update-deals.yml` and uncomment the Discord section:
   
   ```yaml
   # Discord webhook
   curl -X POST "${{ secrets.DISCORD_WEBHOOK }}" \
     -H "Content-Type: application/json" \
     -d "{\"content\": \"🚨 KFH Rewards Alert: Out of stock deals detected!\n${{ steps.check_stock.outputs.out_of_stock }}\"}"
   ```

### Option B: Telegram Notifications

1. **Create Telegram Bot:**
   - Message [@BotFather](https://t.me/botfather)
   - Send `/newbot`
   - Follow instructions
   - Copy bot token

2. **Get Chat ID:**
   - Message [@userinfobot](https://t.me/userinfobot)
   - Copy your chat ID

3. **Add to GitHub Secrets:**
   - `TELEGRAM_BOT_TOKEN`: Your bot token
   - `TELEGRAM_CHAT_ID`: Your chat ID

4. **Uncomment in workflow:**
   
   ```yaml
   # Telegram
   curl -X POST "https://api.telegram.org/bot${{ secrets.TELEGRAM_BOT_TOKEN }}/sendMessage" \
     -d "chat_id=${{ secrets.TELEGRAM_CHAT_ID }}" \
     -d "text=🚨 KFH Rewards Alert: Out of stock deals detected!%0A${{ steps.check_stock.outputs.out_of_stock }}"
   ```

### Option C: Slack Notifications

1. **Create Slack Webhook:**
   - Go to https://api.slack.com/apps
   - Create app → Incoming Webhooks
   - Copy webhook URL

2. **Add to GitHub Secrets:**
   - Name: `SLACK_WEBHOOK`
   - Value: Your webhook URL

3. **Uncomment in workflow:**
   
   ```yaml
   # Slack webhook
   curl -X POST "${{ secrets.SLACK_WEBHOOK }}" \
     -H "Content-Type: application/json" \
     -d "{\"text\": \"🚨 KFH Rewards Alert: Out of stock deals detected!\n${{ steps.check_stock.outputs.out_of_stock }}\"}"
   ```

### Option D: Email Notifications (via SendGrid)

1. **Sign up for SendGrid** (free tier: 100 emails/day)
2. **Get API key** from SendGrid dashboard
3. **Add to backend code** (`kfh_backend.py`)
4. **Add API key to Heroku/Railway environment variables**

---

## 🎯 Complete Setup Checklist

### Basic Setup:
- [ ] Create GitHub repository
- [ ] Upload all files
- [ ] Enable GitHub Pages
- [ ] Deploy backend to Heroku/Railway
- [ ] Update API URL in frontend
- [ ] Test dashboard

### Advanced Setup:
- [ ] Enable GitHub Actions
- [ ] Configure notifications (Discord/Telegram/Slack)
- [ ] Set up custom domain (optional)
- [ ] Add more deals to track
- [ ] Customize refresh intervals

---

## 🚀 Quick Deploy Commands

### Heroku:
```bash
git clone https://github.com/YOUR_USERNAME/kfh-rewards-tracker.git
cd kfh-rewards-tracker
heroku create
git push heroku main
heroku open
```

### Railway:
Just connect your GitHub repo to Railway - it deploys automatically!

---

## 📊 Monitoring Your Deployment

### Check Heroku Logs:
```bash
heroku logs --tail
```

### Check Railway Logs:
Go to Railway dashboard → Your project → Deployments → View logs

### Check GitHub Actions:
Repository → Actions tab → View workflow runs

### Check API Health:
Visit: `https://your-backend-url.com/api/health`

---

## 🔧 Updating Your Deployment

When you make changes:

```bash
git add .
git commit -m "Description of changes"
git push origin main

# For Heroku, also push to heroku
git push heroku main
```

Railway and GitHub Pages deploy automatically on git push!

---

## 🆘 Troubleshooting

### GitHub Pages not working:
- Wait 2-3 minutes after enabling
- Check Settings → Pages shows green checkmark
- Verify `docs/index.html` exists

### Heroku app crashes:
- Check logs: `heroku logs --tail`
- Verify `Procfile` and `runtime.txt` exist
- Test locally first: `python kfh_backend.py`

### API returns errors:
- Check if KFH website structure changed
- Test URLs manually in browser
- Check backend logs for errors

### GitHub Actions failing:
- Check Actions tab for error messages
- Verify workflow file syntax
- Test scraping code locally

---

## 🎉 You're Done!

Your KFH Rewards Tracker is now live on GitHub!

- **Frontend:** `https://YOUR_USERNAME.github.io/kfh-rewards-tracker/`
- **Backend:** `https://your-app.herokuapp.com` or Railway URL
- **Repository:** `https://github.com/YOUR_USERNAME/kfh-rewards-tracker`

Share your tracker URL with friends who also use KFH Rewards! 🎊
