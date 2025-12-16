# KFH Rewards Live Tracker - Setup Guide

This guide will help you set up the KFH Rewards tracker with **real-time data** from the KFH website.

## System Overview

The system has two components:
1. **Backend API** (Python Flask) - Scrapes KFH website for real data
2. **Frontend Dashboard** (HTML) - Displays the data beautifully

## Quick Start (5 minutes)

### Step 1: Install Python Dependencies

```bash
# Navigate to the directory with the files
cd /path/to/kfh-tracker

# Install required packages
pip install flask flask-cors requests beautifulsoup4 lxml
```

Or use the requirements file:
```bash
pip install -r requirements.txt
```

### Step 2: Start the Backend API

```bash
python kfh_backend.py
```

You should see:
```
Starting KFH Rewards Tracker API...
Fetching initial data...
Deal 113316: Found 1150 vouchers
Deal 115315: Found 798 vouchers
Deal 112772: Found 294 vouchers
Deal 112773: Found 108 vouchers
Initial data loaded successfully
Starting Flask server on http://0.0.0.0:5000
```

### Step 3: Open the Dashboard

Open `kfh-tracker-live.html` in your web browser. The dashboard will automatically connect to the API and display real data!

---

## Files Included

1. **kfh_backend.py** - Python backend that scrapes KFH website
2. **kfh-tracker-live.html** - HTML dashboard with real data integration
3. **requirements.txt** - Python dependencies
4. **README.md** - This file

---

## How It Works

### Backend (kfh_backend.py)

The backend:
1. **Scrapes** the KFH Rewards website to extract voucher quantities
2. **Caches** the data for 5 minutes to avoid overloading KFH servers
3. **Serves** the data via REST API endpoints

**API Endpoints:**
- `GET /api/deals` - Get all deals with quantities
- `GET /api/deals/<deal_id>` - Get specific deal
- `POST /api/refresh` - Force refresh (bypass cache)
- `GET /api/health` - Check API health

### Frontend (kfh-tracker-live.html)

The dashboard:
1. **Fetches** data from the backend API
2. **Displays** deals with color-coded status (green/orange/red)
3. **Auto-refreshes** at configurable intervals
4. **Sends notifications** when deals go out of stock or low

---

## Configuration

### Change API URL

If running the backend on a different machine or port, update the API URL in the dashboard:

```html
<input type="text" id="apiUrl" value="http://localhost:5000">
```

Or change it directly in the dashboard interface.

### Adjust Refresh Intervals

In `kfh_backend.py`, change cache duration:
```python
CACHE_DURATION = 300  # seconds (5 minutes)
```

In the dashboard, users can select: 5 min, 10 min, 30 min, or 1 hour.

### Modify Deals

To track different deals, edit the `DEALS` array in `kfh_backend.py`:

```python
DEALS = [
    {
        'id': '113316',  # Deal ID from URL
        'title': '5 KD Off from Talabat',
        'url': 'https://rewards.kfh/redemption/dealdetails/113316/...',
        'points': '3000 KP'
    },
    # Add more deals here
]
```

---

## Deployment Options

### Option 1: Run Locally (Easiest)

Just run the Python script and open the HTML file. Perfect for personal use.

```bash
python kfh_backend.py
# Then open kfh-tracker-live.html in browser
```

### Option 2: Deploy on VPS (Recommended)

Deploy the backend on a cloud server so it runs 24/7:

```bash
# On your VPS (Ubuntu/Debian):
sudo apt update
sudo apt install python3-pip

# Install dependencies
pip3 install flask flask-cors requests beautifulsoup4 lxml

# Run with nohup (keeps running after logout)
nohup python3 kfh_backend.py > kfh.log 2>&1 &
```

Then update the dashboard API URL to your VPS IP:
```
http://YOUR_VPS_IP:5000
```

### Option 3: Deploy with Docker

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY kfh_backend.py .

EXPOSE 5000

CMD ["python", "kfh_backend.py"]
```

Build and run:
```bash
docker build -t kfh-tracker .
docker run -d -p 5000:5000 --name kfh-tracker kfh-tracker
```

### Option 4: Deploy to Heroku

```bash
# Install Heroku CLI, then:
heroku create kfh-rewards-tracker
git init
git add .
git commit -m "Initial commit"
git push heroku master
```

Create `Procfile`:
```
web: python kfh_backend.py
```

---

## Running as a Service (Linux)

To run the backend automatically on system startup:

Create `/etc/systemd/system/kfh-tracker.service`:

```ini
[Unit]
Description=KFH Rewards Tracker API
After=network.target

[Service]
Type=simple
User=yourusername
WorkingDirectory=/path/to/kfh-tracker
ExecStart=/usr/bin/python3 /path/to/kfh-tracker/kfh_backend.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable kfh-tracker
sudo systemctl start kfh-tracker
sudo systemctl status kfh-tracker
```

---

## Troubleshooting

### Problem: "Connection refused" or "Failed to connect to API"

**Solution:**
1. Make sure the backend is running: `python kfh_backend.py`
2. Check if port 5000 is open: `netstat -an | grep 5000`
3. Verify the API URL in the dashboard matches where backend is running
4. Check firewall settings if running on VPS

### Problem: "CORS error" in browser console

**Solution:**
The backend already includes CORS headers (`flask-cors`). If you still see errors:
1. Make sure `flask-cors` is installed: `pip install flask-cors`
2. Try accessing the API directly in browser: `http://localhost:5000/api/deals`

### Problem: Quantities showing as 0

**Solution:**
1. Check backend logs for scraping errors
2. KFH website structure may have changed - inspect the HTML manually
3. The regex pattern in `scrape_deal_quantity()` may need adjustment

### Problem: "ModuleNotFoundError"

**Solution:**
Install missing dependencies:
```bash
pip install flask flask-cors requests beautifulsoup4 lxml
```

---

## Advanced: Customizing the Scraper

If KFH changes their website structure, you may need to update the scraping logic in `kfh_backend.py`.

Current pattern:
```python
match = re.search(r'(\d+)\s+vouchers?\s+left', text_content, re.IGNORECASE)
```

To debug:
1. Visit the deal page in your browser
2. View page source (Ctrl+U)
3. Find where the quantity is displayed
4. Update the regex pattern accordingly

Example if they change to "X remaining":
```python
match = re.search(r'(\d+)\s+remaining', text_content, re.IGNORECASE)
```

---

## Notifications

### Browser Notifications

The dashboard requests notification permission on first load. Click "Allow" to receive desktop notifications when deals go out of stock.

### Email Notifications (Optional)

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
        server.login('your-email@gmail.com', 'your-app-password')
        server.send_message(msg)
```

### Telegram Notifications (Optional)

```python
import requests

def send_telegram(deal):
    bot_token = 'YOUR_BOT_TOKEN'
    chat_id = 'YOUR_CHAT_ID'
    message = f"🚨 {deal['title']} is out of stock!"
    
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    requests.post(url, json={'chat_id': chat_id, 'text': message})
```

---

## Monitoring

### Check Backend Health

```bash
curl http://localhost:5000/api/health
```

Response:
```json
{
  "status": "healthy",
  "timestamp": "2024-12-16T10:30:00",
  "cache_age_seconds": 120,
  "cached_deals": 4
}
```

### View Logs

```bash
# If running as service
sudo journalctl -u kfh-tracker -f

# If running with nohup
tail -f kfh.log
```

---

## Performance Tips

1. **Increase cache duration** to reduce load on KFH servers
2. **Use a VPS** instead of running locally for 24/7 availability
3. **Add rate limiting** if tracking many deals
4. **Use Redis** for better caching in production

---

## Security Notes

1. **Don't expose the API publicly** without authentication
2. **Use environment variables** for sensitive data
3. **Add rate limiting** to prevent abuse
4. **Use HTTPS** in production

---

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review backend logs for errors
3. Test API endpoints directly in browser
4. Verify KFH website hasn't changed structure

---

## Example: Complete Setup on Fresh Ubuntu Server

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip -y

# Create directory
mkdir ~/kfh-tracker
cd ~/kfh-tracker

# Upload files (kfh_backend.py, requirements.txt, kfh-tracker-live.html)

# Install dependencies
pip3 install -r requirements.txt

# Run backend
python3 kfh_backend.py
```

Then access from any device on your network: `http://SERVER_IP:5000`

---

## What's Next?

- Add more deals to track
- Set up email/SMS notifications
- Deploy to cloud for 24/7 monitoring
- Add historical data tracking
- Create mobile app version

Enjoy your KFH Rewards tracker! 🎉
