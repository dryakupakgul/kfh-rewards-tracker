# KFH Rewards Tracker 🎯

Real-time tracker for Kuwait Finance House (KFH) Rewards deals with live stock monitoring, notifications, and auto-refresh capabilities.

![Dashboard Preview](https://img.shields.io/badge/Status-Live-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🌟 Features

- ✅ **Real-time data** scraped from KFH Rewards website
- 📊 **Beautiful dashboard** with color-coded status indicators
- 🔔 **Smart notifications** for out-of-stock and low-stock deals
- ⚡ **Auto-refresh** with configurable intervals
- 🎨 **Modern UI** with cyberpunk-inspired design
- 📱 **Responsive** - works on desktop and mobile
- 🔄 **Automatic updates** via GitHub Actions (optional)

## 📸 Screenshots

### Dashboard View
The tracker shows all deals with their current stock levels, points required, and status.

### Notifications
Get instant alerts when deals go out of stock or run low.

## 🚀 Quick Start

### Option 1: Run Locally (Recommended for Testing)

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/kfh-rewards-tracker.git
   cd kfh-rewards-tracker
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the backend**
   ```bash
   python kfh_backend.py
   ```

4. **Open the dashboard**
   - Open `kfh-tracker-live.html` in your browser
   - Or visit `http://localhost:5000` if you deployed the static files

### Option 2: Deploy to GitHub Pages (Frontend Only)

The HTML dashboard can be hosted on GitHub Pages. You'll need to deploy the backend separately.

1. **Enable GitHub Pages**
   - Go to repository Settings → Pages
   - Source: Deploy from a branch
   - Branch: `main` → `/docs` folder
   - Click Save

2. **Access your dashboard**
   - Visit: `https://YOUR_USERNAME.github.io/kfh-rewards-tracker/`
   - Update API URL to point to your deployed backend

### Option 3: Deploy Full Stack to Cloud

Deploy both frontend and backend to a cloud platform:

- **Heroku**: See [Heroku Deployment Guide](#heroku-deployment)
- **Railway**: See [Railway Deployment Guide](#railway-deployment)
- **DigitalOcean**: See [VPS Deployment Guide](#vps-deployment)
- **AWS**: Deploy backend to Lambda, frontend to S3

## 📁 Repository Structure

```
kfh-rewards-tracker/
├── kfh_backend.py           # Flask API backend
├── kfh-tracker-live.html    # Frontend dashboard
├── requirements.txt         # Python dependencies
├── README.md                # This file
├── SETUP-GUIDE.md          # Detailed setup instructions
├── .github/
│   └── workflows/
│       └── update-deals.yml # GitHub Actions workflow
├── docs/
│   └── index.html          # GitHub Pages version
├── .gitignore
└── LICENSE
```

## 🔧 Configuration

### Tracked Deals

Edit the `DEALS` array in `kfh_backend.py` to add or remove deals:

```python
DEALS = [
    {
        'id': '113316',
        'title': '5 KD Off from Talabat',
        'url': 'https://rewards.kfh/redemption/dealdetails/113316/...',
        'points': '3000 KP'
    },
    # Add more deals here
]
```

### Cache Duration

Adjust how often the backend refreshes data from KFH:

```python
CACHE_DURATION = 300  # seconds (5 minutes)
```

### Auto-Refresh Interval

Users can configure refresh interval in the dashboard (5min, 10min, 30min, 1 hour).

## 🌐 Deployment Guides

### Heroku Deployment

1. **Create a Heroku app**
   ```bash
   heroku create kfh-rewards-tracker
   ```

2. **Create a `Procfile`**
   ```
   web: python kfh_backend.py
   ```

3. **Update `kfh_backend.py`** to use PORT from environment
   ```python
   import os
   port = int(os.environ.get('PORT', 5000))
   app.run(host='0.0.0.0', port=port)
   ```

4. **Deploy**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

5. **Update frontend API URL**
   - Change API URL in `kfh-tracker-live.html` to: `https://your-app.herokuapp.com`

### Railway Deployment

1. **Connect GitHub repository** to Railway
2. **Railway auto-detects** Python and installs dependencies
3. **Set environment variables** (if needed)
4. **Deploy** - Railway provides a URL automatically
5. **Update API URL** in the dashboard to your Railway URL

### VPS Deployment (DigitalOcean, Linode, etc.)

1. **SSH into your server**
   ```bash
   ssh root@your_server_ip
   ```

2. **Install dependencies**
   ```bash
   apt update && apt upgrade -y
   apt install python3 python3-pip git -y
   ```

3. **Clone repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/kfh-rewards-tracker.git
   cd kfh-rewards-tracker
   pip3 install -r requirements.txt
   ```

4. **Create systemd service**
   ```bash
   sudo nano /etc/systemd/system/kfh-tracker.service
   ```

   Add:
   ```ini
   [Unit]
   Description=KFH Rewards Tracker
   After=network.target

   [Service]
   Type=simple
   User=root
   WorkingDirectory=/root/kfh-rewards-tracker
   ExecStart=/usr/bin/python3 kfh_backend.py
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

5. **Enable and start**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable kfh-tracker
   sudo systemctl start kfh-tracker
   ```

6. **Setup Nginx** (optional, for production)
   ```bash
   apt install nginx -y
   ```

   Configure reverse proxy in `/etc/nginx/sites-available/kfh-tracker`:
   ```nginx
   server {
       listen 80;
       server_name your_domain.com;

       location / {
           proxy_pass http://localhost:5000;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection 'upgrade';
           proxy_set_header Host $host;
           proxy_cache_bypass $http_upgrade;
       }
   }
   ```

### Docker Deployment

1. **Create `Dockerfile`**
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   COPY . .
   EXPOSE 5000
   CMD ["python", "kfh_backend.py"]
   ```

2. **Build and run**
   ```bash
   docker build -t kfh-tracker .
   docker run -d -p 5000:5000 --name kfh-tracker kfh-tracker
   ```

3. **Or use Docker Compose**
   ```yaml
   version: '3.8'
   services:
     kfh-tracker:
       build: .
       ports:
         - "5000:5000"
       restart: unless-stopped
   ```

## 🤖 GitHub Actions (Automated Updates)

Enable automatic deal monitoring with GitHub Actions:

1. **The workflow file** (`.github/workflows/update-deals.yml`) is already included
2. **It runs every 10 minutes** to check deal status
3. **Sends notifications** if deals go out of stock
4. **Stores data** in repository for historical tracking

To enable:
- Go to Actions tab in your GitHub repository
- Enable workflows
- (Optional) Add notification webhook secrets

## 🔔 Notifications Setup

### Browser Notifications
Automatically requested when you open the dashboard. Click "Allow" to enable.

### Email Notifications

Add to `kfh_backend.py`:

```python
import smtplib
from email.mime.text import MIMEText

def send_email_alert(deal):
    msg = MIMEText(f"{deal['title']} is out of stock!")
    msg['Subject'] = 'KFH Rewards Alert'
    msg['From'] = 'your-email@gmail.com'
    msg['To'] = 'recipient@example.com'
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login('your-email@gmail.com', 'app-password')
        server.send_message(msg)
```

### Telegram Notifications

1. Create a bot with [@BotFather](https://t.me/botfather)
2. Get your chat ID from [@userinfobot](https://t.me/userinfobot)
3. Add to `kfh_backend.py`:

```python
import requests

def send_telegram(deal):
    bot_token = 'YOUR_BOT_TOKEN'
    chat_id = 'YOUR_CHAT_ID'
    message = f"🚨 {deal['title']} is out of stock!"
    
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    requests.post(url, json={'chat_id': chat_id, 'text': message})
```

## 📊 API Documentation

### Endpoints

#### `GET /api/deals`
Get all tracked deals with current quantities.

**Response:**
```json
{
  "deals": [
    {
      "id": "113316",
      "title": "5 KD Off from Talabat",
      "url": "https://rewards.kfh/...",
      "points": "3000 KP",
      "quantity": 1150,
      "last_updated": "2024-12-16T10:30:00"
    }
  ],
  "timestamp": "2024-12-16T10:30:00",
  "cached": false
}
```

#### `GET /api/deals/<deal_id>`
Get a specific deal by ID.

#### `POST /api/refresh`
Force refresh all deals (bypass cache).

#### `GET /api/health`
Health check endpoint.

## 🛠️ Development

### Running Tests
```bash
python -m pytest tests/
```

### Code Style
```bash
black kfh_backend.py
flake8 kfh_backend.py
```

### Debug Mode
Set `debug=True` in `app.run()` for development.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 To-Do

- [ ] Add historical data tracking
- [ ] Create data visualization charts
- [ ] Mobile app version
- [ ] SMS notifications
- [ ] Support for more merchants
- [ ] Deal comparison features
- [ ] Price tracking over time
- [ ] Export data to CSV/Excel

## ⚠️ Disclaimer

This is an unofficial tracker for educational purposes. Use responsibly and respect KFH's terms of service. Do not overload their servers with excessive requests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Kuwait Finance House for the Rewards program
- Flask and BeautifulSoup communities
- All contributors to this project

## 📧 Contact

Have questions or suggestions? Open an issue or reach out!

---

**Made with ❤️ for KFH Rewards users**

⭐ Star this repository if you find it helpful!
