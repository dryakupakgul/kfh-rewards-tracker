#!/usr/bin/env python3
"""
KFH Rewards Tracker Backend
Scrapes real-time data from KFH Rewards website and serves it via API
"""

from flask import Flask, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import re
import time
import os
from datetime import datetime
import logging

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Deal configuration
DEALS = [
    {
        'id': '113316',
        'title': '5 KD Off from Talabat',
        'url': 'https://rewards.kfh/redemption/dealdetails/113316/3-KD-Off-from-Talabat',
        'points': '3000 KP'
    },
    {
        'id': '113005',
        'title': '10 KD Off from Talabat',
        'url': 'https://rewards.kfh/redemption/dealdetails/113005/10-KD-Off-from-Talabat',
        'points': '10000 KP'
    },
    {
        'id': '115708',
        'title': '12 KD off from Keeta',
        'url': 'https://rewards.kfh/redemption/dealdetails/115708/Get-12-KD-off-from-Keeta',
        'points': '12000 KP'
    },
    {
        'id': '115707',
        'title': '6 KD off from Keeta',
        'url': 'https://rewards.kfh/redemption/dealdetails/115707/Get-6-KD-off-from-Keeta',
        'points': '6000 KP'
    },
    {
        'id': '115706',
        'title': '3 KD off from Keeta',
        'url': 'https://rewards.kfh/redemption/dealdetails/115706/Get-3-KD-off-from-Keeta',
        'points': '3000 KP'
    },
    {
        'id': '112772',
        'title': '5 KD Deliveroo Wallet recharge',
        'url': 'https://rewards.kfh/redemption/dealdetails/112772/5-KD-Deliveroo-Wallet-recharge',
        'points': '5000 KP'
    },
    {
        'id': '112773',
        'title': '3 KD Deliveroo Wallet recharge',
        'url': 'https://rewards.kfh/redemption/dealdetails/112773/3-KD-Deliveroo-Wallet-recharge',
        'points': '3000 KP'
    },
    {
        'id': '115631',
        'title': '3 KD Off from Bleems',
        'url': 'https://rewards.kfh/redemption/dealdetails/115631/3-KD-Off-from-Bleems',
        'points': '3000 KP'
    },
    {
        'id': '115482',
        'title': '3 KD Off from Cari',
        'url': 'https://rewards.kfh/redemption/dealdetails/115482/3-KD-Off-from-Cari',
        'points': '3000 KP'
    },
    {
        'id': '115622',
        'title': '6 Months talabat pro Subscription',
        'url': 'https://rewards.kfh/redemption/dealdetails/115622/6-Months-talabat-pro-Subscription',
        'points': '3000 KP'
    },
    {
        'id': '115685',
        'title': '5 KD Off from Caribou Coffee',
        'url': 'https://rewards.kfh/redemption/dealdetails/115685/5-KD-Off-from-Caribou-Coffee',
        'points': '5000 KP'
    },
    {
        'id': '115684',
        'title': '3 KD Off from Caribou Coffee',
        'url': 'https://rewards.kfh/redemption/dealdetails/115684/3-KD-Off-from-Caribou-Coffee',
        'points': '3000 KP'
    },
    {
        'id': '113244',
        'title': '5 KD gift card from COFE App',
        'url': 'https://rewards.kfh/redemption/dealdetails/113244/Get-a-5-KD-gift-card-from-COFE-App',
        'points': '5000 KP'
    },
    {
        'id': '115078',
        'title': '30% off from Caldo Restaurant',
        'url': 'https://rewards.kfh/redemption/dealdetails/115078/30-off-from-Caldo-Restaurant',
        'points': '100 KP'
    },
    {
        'id': '113947',
        'title': '9 KD off on Shrimp Mumawash box from The Ranch',
        'url': 'https://rewards.kfh/redemption/dealdetails/113947/9-KD-off-on-Shrimp-Mumawash-box',
        'points': '9000 KP'
    },
    {
        'id': '113943',
        'title': '10 KD Off Catering from BBQ Burger',
        'url': 'https://rewards.kfh/redemption/dealdetails/113943/10-KD-Off-Catering-burger--catering-from-BBQ-Burger-store--website',
        'points': '10000 KP'
    },
    {
        'id': '113942',
        'title': '5 KD Off Burger Box from BBQ Burger',
        'url': 'https://rewards.kfh/redemption/dealdetails/113942/5-KD-Off-Burger-Box-or-Mashawi-orders-from-BBQ-Burger-store--website',
        'points': '5000 KP'
    },
    {
        'id': '113330',
        'title': '3 KD Off from Shawarma Elestez',
        'url': 'https://rewards.kfh/redemption/dealdetails/113330/3-KD-Off-from-Shawarma-Elestez-website',
        'points': '3000 KP'
    },
    {
        'id': '115396',
        'title': '16 KD Off from Al Rifai',
        'url': 'https://rewards.kfh/redemption/dealdetails/115396/16-KD-Off-from-Al-Rifai-On-the-Go-Minis-Bundle-',
        'points': '16000 KP'
    },
    {
        'id': '113256',
        'title': '10 KD Off from Al Rifai',
        'url': 'https://rewards.kfh/redemption/dealdetails/113256/10-KD-Off-from-Al-Rifai',
        'points': '10000 KP'
    },
    {
        'id': '115315',
        'title': '$10 iTunes Gift Card',
        'url': 'https://rewards.kfh/redemption/dealdetails/115315/10-iTunes-Gift-Card',
        'points': '3500 KP'
    },
    {
        'id': '112845',
        'title': '$5 iTunes Gift Card',
        'url': 'https://rewards.kfh/redemption/dealdetails/112845/5-iTunes-Gift-Card',
        'points': '2000 KP'
    },
    {
        'id': '115336',
        'title': '$10 Google Play Gift Card',
        'url': 'https://rewards.kfh/redemption/dealdetails/115336/10-Google-Play-Gift-Card',
        'points': '3500 KP'
    },
    {
        'id': '115346',
        'title': '$10 Amazon USA Gift Card',
        'url': 'https://rewards.kfh/redemption/dealdetails/115346/Amazon-10-USA-Gift-Card',
        'points': '3500 KP'
    },
    {
        'id': '115391',
        'title': '$10 Nintendo USA Gift Card',
        'url': 'https://rewards.kfh/redemption/dealdetails/115391/Nintendo-10-USA-Gift-Card',
        'points': '3500 KP'
    },
    {
        'id': '115395',
        'title': '$25 XBOX USA Gift Card',
        'url': 'https://rewards.kfh/redemption/dealdetails/115395/XBOX-25-USA-Gift-Card',
        'points': '8000 KP'
    },
    {
        'id': '115394',
        'title': 'Xbox Live 3 months subscription',
        'url': 'https://rewards.kfh/redemption/dealdetails/115394/Xbox-Live-3-months-free-subscription',
        'points': '8000 KP'
    },
    {
        'id': '115357',
        'title': '5 KD from Zain',
        'url': 'https://rewards.kfh/redemption/dealdetails/115357/5KD-from-Zain',
        'points': '5000 KP'
    },
    {
        'id': '115371',
        'title': '5 KD from STC',
        'url': 'https://rewards.kfh/redemption/dealdetails/115371/5KD-from-STC',
        'points': '5000 KP'
    },
    {
        'id': '115147',
        'title': '3 KD Off on Starzplay Sports',
        'url': 'https://rewards.kfh/redemption/dealdetails/115147/3-KD-Off-on-Starzplay--Sports-Package',
        'points': '3000 KP'
    },
    {
        'id': '113933',
        'title': '5 KD Off from AlFuhood App',
        'url': 'https://rewards.kfh/redemption/dealdetails/113933/5-KD-Off-from-AlFuhood-App--website',
        'points': '5000 KP'
    },
    {
        'id': '115667',
        'title': '5 KD voucher from Blue outdoors',
        'url': 'https://rewards.kfh/redemption/dealdetails/115667/5-KD-voucher-from-Blue-outdoors',
        'points': '5000 KP'
    },
    {
        'id': '115490',
        'title': '50 KD off from Flowers & Beyond',
        'url': 'https://rewards.kfh/redemption/dealdetails/115490/50-KD-off-from-Flowers--Beyond',
        'points': '50000 KP'
    },
    {
        'id': '112920',
        'title': '20 KD Off from Best Al-Yousifi',
        'url': 'https://rewards.kfh/redemption/dealdetails/112920/20-KD-Off-from-Best-Al-Yousifi',
        'points': '20000 KP'
    },
    {
        'id': '113150',
        'title': '20 KD Off from H&S Store',
        'url': 'https://rewards.kfh/redemption/dealdetails/113150/20-KD-Off-from-HS-Store',
        'points': '20000 KP'
    },
    {
        'id': '115173',
        'title': '10 KD voucher from Usim',
        'url': 'https://rewards.kfh/redemption/dealdetails/115173/Get-10KD-voucher-from-Usim',
        'points': '10000 KP'
    },
    {
        'id': '112804',
        'title': '15% discount from Pharmatee',
        'url': 'https://rewards.kfh/redemption/dealdetails/112804/15-discount-from-Pharmatee',
        'points': '100 KP'
    }
]

# Cache for deal data
deal_cache = {}
cache_timestamp = None
CACHE_DURATION = 300  # 5 minutes in seconds


def scrape_deal_quantity(deal_url, deal_id):
    """
    Scrape the quantity remaining for a specific deal from KFH website
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        }
        
        logger.info(f"Fetching deal {deal_id} from {deal_url}")
        response = requests.get(deal_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for quantity patterns in the page
        text_content = soup.get_text()
        match = re.search(r'(\d+)\s+vouchers?\s+left', text_content, re.IGNORECASE)
        
        if match:
            quantity = int(match.group(1))
            logger.info(f"Deal {deal_id}: Found {quantity} vouchers")
            return quantity
        
        logger.warning(f"Deal {deal_id}: Could not parse quantity")
        return None
        
    except requests.RequestException as e:
        logger.error(f"Error fetching deal {deal_id}: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error for deal {deal_id}: {e}")
        return None


def fetch_all_deals():
    """
    Fetch quantities for all deals
    """
    global deal_cache, cache_timestamp
    
    results = []
    for deal in DEALS:
        quantity = scrape_deal_quantity(deal['url'], deal['id'])
        
        deal_data = {
            'id': deal['id'],
            'title': deal['title'],
            'url': deal['url'],
            'points': deal['points'],
            'quantity': quantity if quantity is not None else 0,
            'last_updated': datetime.now().isoformat()
        }
        results.append(deal_data)
        deal_cache[deal['id']] = deal_data
        
        # Be nice to the server - add small delay between requests
        time.sleep(1)
    
    cache_timestamp = time.time()
    return results


@app.route('/api/deals', methods=['GET'])
def get_deals():
    """
    API endpoint to get current deal data
    Returns cached data if recent, otherwise fetches fresh data
    """
    global deal_cache, cache_timestamp
    
    # Check if cache is still valid
    if cache_timestamp and (time.time() - cache_timestamp) < CACHE_DURATION:
        logger.info("Returning cached data")
        return jsonify({
            'deals': list(deal_cache.values()),
            'timestamp': datetime.now().isoformat(),
            'cached': True,
            'cache_age_seconds': int(time.time() - cache_timestamp)
        })
    
    # Fetch fresh data
    logger.info("Fetching fresh data from KFH website")
    try:
        deals_data = fetch_all_deals()
        return jsonify({
            'deals': deals_data,
            'timestamp': datetime.now().isoformat(),
            'cached': False
        })
    except Exception as e:
        logger.error(f"Error fetching deals: {e}")
        # Return cached data if available, even if stale
        if deal_cache:
            return jsonify({
                'deals': list(deal_cache.values()),
                'timestamp': datetime.now().isoformat(),
                'cached': True,
                'error': str(e)
            }), 200
        else:
            return jsonify({
                'error': 'Failed to fetch deals and no cache available',
                'message': str(e)
            }), 500


@app.route('/api/deals/<deal_id>', methods=['GET'])
def get_deal(deal_id):
    """
    API endpoint to get a specific deal
    """
    deal_config = next((d for d in DEALS if d['id'] == deal_id), None)
    
    if not deal_config:
        return jsonify({'error': 'Deal not found'}), 404
    
    # Check cache first
    if deal_id in deal_cache:
        cache_age = time.time() - cache_timestamp if cache_timestamp else float('inf')
        if cache_age < CACHE_DURATION:
            return jsonify({
                'deal': deal_cache[deal_id],
                'cached': True
            })
    
    # Fetch fresh data for this deal
    quantity = scrape_deal_quantity(deal_config['url'], deal_id)
    
    deal_data = {
        'id': deal_config['id'],
        'title': deal_config['title'],
        'url': deal_config['url'],
        'points': deal_config['points'],
        'quantity': quantity if quantity is not None else 0,
        'last_updated': datetime.now().isoformat()
    }
    
    deal_cache[deal_id] = deal_data
    
    return jsonify({
        'deal': deal_data,
        'cached': False
    })


@app.route('/api/refresh', methods=['POST'])
def force_refresh():
    """
    Force refresh all deals (bypass cache)
    """
    global cache_timestamp
    cache_timestamp = None  # Invalidate cache
    
    try:
        deals_data = fetch_all_deals()
        return jsonify({
            'deals': deals_data,
            'timestamp': datetime.now().isoformat(),
            'message': 'Data refreshed successfully'
        })
    except Exception as e:
        logger.error(f"Error refreshing deals: {e}")
        return jsonify({
            'error': 'Failed to refresh deals',
            'message': str(e)
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    """
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'cache_age_seconds': int(time.time() - cache_timestamp) if cache_timestamp else None,
        'cached_deals': len(deal_cache)
    })


@app.route('/', methods=['GET'])
def index():
    """
    API information page
    """
    return jsonify({
        'name': 'KFH Rewards Tracker API',
        'version': '1.0.0',
        'endpoints': {
            '/api/deals': 'GET all deals',
            '/api/deals/<deal_id>': 'GET specific deal',
            '/api/refresh': 'POST to force refresh',
            '/api/health': 'GET health status'
        },
        'deals_tracked': len(DEALS)
    })


if __name__ == '__main__':
    # Fetch initial data
    logger.info("Starting KFH Rewards Tracker API...")
    logger.info("Fetching initial data...")
    try:
        fetch_all_deals()
        logger.info("Initial data loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load initial data: {e}")
    
    # Get port from environment variable (for Heroku, Railway, etc.)
    port = int(os.environ.get('PORT', 5000))
    
    # Start server
    logger.info(f"Starting Flask server on http://0.0.0.0:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
