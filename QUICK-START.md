# 🚀 KFH Rewards Tracker - GitHub Setup Summary

## What You Have

A complete GitHub repository ready to deploy with:

- ✅ **Backend API** (Python Flask) - scrapes real KFH data
- ✅ **Frontend Dashboard** (HTML) - beautiful, responsive UI
- ✅ **GitHub Actions** - automated monitoring every 10 minutes
- ✅ **Deployment configs** - Heroku, Railway, Docker ready
- ✅ **Documentation** - comprehensive setup guides

## 📁 Repository Structure

```
kfh-repo/
├── kfh_backend.py              ← Backend API (scrapes KFH website)
├── kfh-tracker-live.html       ← Dashboard (main file)
├── requirements.txt            ← Python dependencies
├── README.md                   ← Project overview
├── SETUP-GUIDE.md             ← Detailed local setup
├── GITHUB-SETUP.md            ← This guide (GitHub deployment)
├── LICENSE                     ← MIT License
├── .gitignore                  ← Git ignore rules
├── Procfile                    ← Heroku deployment
├── runtime.txt                 ← Python version for Heroku
├── setup-github.sh             ← Quick setup script
├── .github/
│   └── workflows/
│       └── update-deals.yml    ← Automated monitoring
├── docs/
│   └── index.html              ← GitHub Pages version
└── data/
    └── .gitkeep                ← Data storage folder
```

## 🎯 Three Ways to Use This

### Option 1: Quick & Easy (GitHub Pages + Heroku)
**Best for: Beginners, quick setup**

1. Upload to GitHub
2. Enable GitHub Pages for frontend
3. Deploy backend to Heroku (1-click)
4. Update API URL in dashboard

**Time: 10 minutes** | **Cost: Free**

### Option 2: Automated (GitHub + Railway + Actions)
**Best for: Set-it-and-forget-it monitoring**

1. Upload to GitHub
2. Connect to Railway (auto-deploys)
3. Enable GitHub Actions
4. Set up notifications

**Time: 15 minutes** | **Cost: Free**

### Option 3: Full Control (VPS + Custom Domain)
**Best for: Advanced users, production use**

1. Upload to GitHub
2. Deploy to your VPS
3. Set up Nginx reverse proxy
4. Add SSL certificate
5. Configure custom domain

**Time: 30-60 minutes** | **Cost: ~$5/month**

## 🚦 Step-by-Step: Recommended Setup

### Step 1: Upload to GitHub (5 minutes)

**Method A: Web Interface (Easiest)**

1. Go to GitHub.com → New repository
2. Name it: `kfh-rewards-tracker`
3. Click "uploading an existing file"
4. Drag all files from `kfh-repo` folder
5. Commit

**Method B: Command Line**

```bash
cd kfh-repo
chmod +x setup-github.sh
./setup-github.sh
```

### Step 2: Deploy Frontend (2 minutes)

1. Go to repository **Settings** → **Pages**
2. Source: **Deploy from branch**
3. Branch: `main` → Folder: `/docs`
4. Save

**Your dashboard will be live at:**
`https://YOUR_USERNAME.github.io/kfh-rewards-tracker/`

### Step 3: Deploy Backend (5 minutes)

**Option A: Railway (Recommended)**

1. Go to [railway.app](https://railway.app)
2. Sign in with GitHub
3. New Project → Deploy from GitHub
4. Select your repository
5. Wait 2 minutes ⏱️
6. Copy the generated URL

**Option B: Heroku**

```bash
cd kfh-repo
heroku login
heroku create kfh-tracker-YOUR_NAME
git push heroku main
heroku open
```

### Step 4: Connect Frontend to Backend (1 minute)

1. Edit `docs/index.html` in your GitHub repository
2. Find this line:
   ```html
   <input type="text" id="apiUrl" value="http://localhost:5000">
   ```
3. Change to your Railway/Heroku URL:
   ```html
   <input type="text" id="apiUrl" value="https://your-app.railway.app">
   ```
4. Commit the change

### Step 5: Enable Monitoring (Optional, 5 minutes)

1. Go to **Actions** tab in your repository
2. Enable **"Monitor KFH Deals"** workflow
3. Click **Run workflow** to test

Now it will check deals every 10 minutes automatically!

## 📲 Adding Notifications

### Discord (Easiest)

1. Create Discord webhook (Server Settings → Integrations)
2. Add to GitHub Secrets: `DISCORD_WEBHOOK`
3. Uncomment Discord section in `.github/workflows/update-deals.yml`
4. Commit

### Telegram

1. Message [@BotFather](https://t.me/botfather) → create bot
2. Message [@userinfobot](https://t.me/userinfobot) → get chat ID
3. Add to GitHub Secrets: `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`
4. Uncomment Telegram section in workflow
5. Commit

## 🎨 Customization

### Add More Deals

Edit `kfh_backend.py`:

```python
DEALS = [
    {
        'id': 'DEAL_ID',
        'title': 'Deal Name',
        'url': 'https://rewards.kfh/redemption/dealdetails/DEAL_ID/...',
        'points': '3000 KP'
    },
    # Add more here
]
```

### Change Refresh Intervals

**Backend cache:** Edit `CACHE_DURATION` in `kfh_backend.py`
**GitHub Actions:** Edit schedule in `.github/workflows/update-deals.yml`
**Dashboard:** Users can select 5min/10min/30min/1hr in UI

### Custom Styling

Edit the CSS in `kfh-tracker-live.html` or `docs/index.html`

## 🔧 Troubleshooting

### Dashboard shows "Disconnected"
- ✅ Make sure backend is deployed and running
- ✅ Check API URL in dashboard is correct
- ✅ Test API directly: `https://your-api-url/api/health`

### Backend crashes on Heroku
- ✅ Check logs: `heroku logs --tail`
- ✅ Verify `Procfile` and `requirements.txt` are correct
- ✅ Make sure Python version in `runtime.txt` is supported

### GitHub Actions failing
- ✅ Check Actions tab for error details
- ✅ Verify workflow file syntax
- ✅ Test if KFH website is accessible

### No data showing
- ✅ Wait 5 minutes for first scrape
- ✅ Check backend logs
- ✅ Verify deal URLs are correct
- ✅ Test URLs manually in browser

## 💡 Pro Tips

1. **Use Railway instead of Heroku** - better free tier, no sleep
2. **Enable GitHub Actions** - get automatic monitoring
3. **Set up notifications** - never miss a deal again
4. **Check Actions summary** - see historical data
5. **Star your repo** - easy to find later

## 📊 What Happens Next

Once set up, here's what runs automatically:

**Every 10 minutes:**
- GitHub Actions scrapes KFH website
- Saves quantities to `data/latest.json`
- Sends notification if deals are out of stock

**When you visit dashboard:**
- Fetches latest data from your API
- Shows color-coded status
- Auto-refreshes at your chosen interval

**When you push to GitHub:**
- GitHub Pages redeploys frontend (2-3 min)
- Railway redeploys backend automatically
- Heroku requires: `git push heroku main`

## 🎉 Success Checklist

- [ ] Repository created on GitHub
- [ ] All files uploaded
- [ ] GitHub Pages enabled and working
- [ ] Backend deployed (Railway/Heroku)
- [ ] Dashboard shows real data
- [ ] GitHub Actions enabled (optional)
- [ ] Notifications configured (optional)

## 🔗 Quick Links

After setup, bookmark these:

- **Your Dashboard:** `https://YOUR_USERNAME.github.io/kfh-rewards-tracker/`
- **Your API:** `https://your-app.railway.app/api/deals`
- **GitHub Repo:** `https://github.com/YOUR_USERNAME/kfh-rewards-tracker`
- **GitHub Actions:** `https://github.com/YOUR_USERNAME/kfh-rewards-tracker/actions`

## 🆘 Need Help?

1. **Check documentation:**
   - `README.md` - Project overview
   - `SETUP-GUIDE.md` - Local setup
   - `GITHUB-SETUP.md` - Detailed GitHub guide

2. **Test components:**
   - Backend: `https://your-api/api/health`
   - Frontend: Open browser console (F12)
   - Actions: Check Actions tab for errors

3. **Common issues:**
   - CORS errors → Backend needs `flask-cors`
   - 404 errors → Check file paths
   - No data → Wait 5 min or check scraping code

## 🚀 You're Ready!

Everything is set up and ready to deploy. Choose your preferred method above and you'll have a live KFH Rewards tracker in minutes!

**Recommended for beginners:**
1. Upload to GitHub (web interface)
2. Enable GitHub Pages
3. Deploy to Railway
4. Update API URL
5. Done! ✨

Good luck with your KFH Rewards tracking! 🎯
