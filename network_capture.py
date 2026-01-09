#!/usr/bin/env python3
"""
Network Interceptor - Captures actual API calls that send OTP
This shows you the REAL endpoint, headers, and data
"""
import sys
import asyncio
import json
from playwright.async_api import async_playwright


async def capture_paytm_api(phone):
    """
    Captures the actual API request when Paytm sends OTP
    """
    captured_requests = []
    
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        # ==========================================
        # CAPTURE ALL NETWORK REQUESTS
        # ==========================================
        async def handle_request(request):
            # Look for API calls related to OTP/SMS/login
            url = request.url
            method = request.method
            
            # Keywords that indicate OTP endpoints
            otp_keywords = ['otp', 'sms', 'send', 'verify', 'login', 'auth', 'mobile']
            
            if any(keyword in url.lower() for keyword in otp_keywords):
                request_data = {
                    'url': url,
                    'method': method,
                    'headers': request.headers,
                    'post_data': request.post_data if method == 'POST' else None
                }
                captured_requests.append(request_data)
                print(f"\n🔍 CAPTURED REQUEST:")
                print(f"   URL: {url}")
                print(f"   Method: {method}")
                if method == 'POST':
                    print(f"   POST Data: {request.post_data}")
        
        async def handle_response(response):
            url = response.url
            otp_keywords = ['otp', 'sms', 'send', 'verify', 'login', 'auth', 'mobile']
            
            if any(keyword in url.lower() for keyword in otp_keywords):
                try:
                    body = await response.text()
                    print(f"\n📥 RESPONSE from {url}:")
                    print(f"   Status: {response.status}")
                    print(f"   Body: {body[:500]}")  # First 500 chars
                except:
                    pass
        
        page.on("request", handle_request)
        page.on("response", handle_response)
        
        print("="*70)
        print("🎯 NETWORK INTERCEPTOR - Paytm")
        print("="*70)
        print("\n📡 Monitoring network traffic...")
        print("👉 MANUALLY interact with the page:")
        print("   1. Click login button")
        print("   2. Enter phone number:", phone)
        print("   3. Click 'Send OTP' button")
        print("   4. Wait for API calls to be captured")
        print("\n⏳ Waiting 60 seconds for you to interact...")
        print("="*70)
        
        # Go to Paytm
        await page.goto('https://paytm.com/', timeout=60000)
        
        # Wait for manual interaction
        await page.wait_for_timeout(60000)  # 60 seconds
        
        await browser.close()
        
        # Print summary
        print("\n" + "="*70)
        print("📊 CAPTURED API CALLS SUMMARY")
        print("="*70)
        
        if captured_requests:
            for i, req in enumerate(captured_requests, 1):
                print(f"\n🔹 Request #{i}:")
                print(f"   URL: {req['url']}")
                print(f"   Method: {req['method']}")
                print(f"   Headers:")
                for key, value in req['headers'].items():
                    if key.lower() in ['content-type', 'authorization', 'x-', 'api']:
                        print(f"      {key}: {value}")
                if req['post_data']:
                    print(f"   POST Data: {req['post_data']}")
        else:
            print("⚠️  No OTP-related API calls captured")
            print("💡 Try again and make sure to:")
            print("   - Click login")
            print("   - Enter phone number")
            print("   - Click send OTP")
        
        return captured_requests


async def capture_zomato_api(phone):
    """
    Captures the actual API request when Zomato sends OTP
    """
    captured_requests = []
    
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        async def handle_request(request):
            url = request.url
            method = request.method
            
            otp_keywords = ['otp', 'sms', 'send', 'verify', 'login', 'auth', 'phone']
            
            if any(keyword in url.lower() for keyword in otp_keywords):
                request_data = {
                    'url': url,
                    'method': method,
                    'headers': request.headers,
                    'post_data': request.post_data if method == 'POST' else None
                }
                captured_requests.append(request_data)
                print(f"\n🔍 CAPTURED REQUEST:")
                print(f"   URL: {url}")
                print(f"   Method: {method}")
                if method == 'POST':
                    print(f"   POST Data: {request.post_data}")
        
        async def handle_response(response):
            url = response.url
            otp_keywords = ['otp', 'sms', 'send', 'verify', 'login', 'auth', 'phone']
            
            if any(keyword in url.lower() for keyword in otp_keywords):
                try:
                    body = await response.text()
                    print(f"\n📥 RESPONSE from {url}:")
                    print(f"   Status: {response.status}")
                    print(f"   Body: {body[:500]}")
                except:
                    pass
        
        page.on("request", handle_request)
        page.on("response", handle_response)
        
        print("="*70)
        print("🎯 NETWORK INTERCEPTOR - Zomato")
        print("="*70)
        print("\n📡 Monitoring network traffic...")
        print("👉 MANUALLY interact with the page:")
        print("   1. Click login button")
        print("   2. Enter phone number:", phone)
        print("   3. Click 'Send OTP' button")
        print("\n⏳ Waiting 60 seconds for you to interact...")
        print("="*70)
        
        await page.goto('https://www.zomato.com/', timeout=60000)
        await page.wait_for_timeout(60000)
        
        await browser.close()
        
        print("\n" + "="*70)
        print("📊 CAPTURED API CALLS SUMMARY")
        print("="*70)
        
        if captured_requests:
            for i, req in enumerate(captured_requests, 1):
                print(f"\n🔹 Request #{i}:")
                print(f"   URL: {req['url']}")
                print(f"   Method: {req['method']}")
                print(f"   Headers:")
                for key, value in req['headers'].items():
                    if key.lower() in ['content-type', 'authorization', 'x-', 'api']:
                        print(f"      {key}: {value}")
                if req['post_data']:
                    print(f"   POST Data: {req['post_data']}")
        else:
            print("⚠️  No OTP-related API calls captured")
        
        return captured_requests


async def capture_any_site(site_url):
    """
    Generic capture for any website - captures ALL requests
    """
    all_requests = []
    
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        async def handle_request(request):
            url = request.url
            method = request.method
            
            # Capture ALL POST requests
            if method == 'POST':
                request_data = {
                    'url': url,
                    'method': method,
                    'headers': dict(request.headers),
                    'post_data': request.post_data
                }
                all_requests.append(request_data)
                print(f"\n📤 POST: {url}")
                if request.post_data:
                    print(f"   Data: {request.post_data[:200]}")
        
        page.on("request", handle_request)
        
        print("="*70)
        print("🎯 GENERIC NETWORK INTERCEPTOR")
        print("="*70)
        print(f"\n📡 Going to: {site_url}")
        print("👉 Interact with the page manually")
        print("⏳ Monitoring for 90 seconds...")
        print("="*70)
        
        await page.goto(site_url, timeout=60000)
        await page.wait_for_timeout(90000)  # 90 seconds
        
        await browser.close()
        
        print("\n" + "="*70)
        print("📊 ALL POST REQUESTS CAPTURED")
        print("="*70)
        
        for i, req in enumerate(all_requests, 1):
            print(f"\n🔹 Request #{i}:")
            print(f"   URL: {req['url']}")
            print(f"   Method: {req['method']}")
            if req['post_data']:
                print(f"   POST Data: {req['post_data']}")
            print(f"   Key Headers:")
            for key in ['content-type', 'authorization', 'x-auth-token', 'api-key']:
                if key in req['headers']:
                    print(f"      {key}: {req['headers'][key]}")
        
        # Save to file
        with open('captured_requests.json', 'w') as f:
            json.dump(all_requests, f, indent=2)
        print(f"\n💾 Full data saved to: captured_requests.json")
        
        return all_requests


async def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python network_capture.py paytm [phone]")
        print("  python network_capture.py zomato [phone]")
        print("  python network_capture.py url <website-url>")
        sys.exit(1)
    
    site = sys.argv[1].lower()
    
    if site == "paytm":
        phone = sys.argv[2] if len(sys.argv) > 2 else "9876543210"
        await capture_paytm_api(phone)
    elif site == "zomato":
        phone = sys.argv[2] if len(sys.argv) > 2 else "9876543210"
        await capture_zomato_api(phone)
    elif site == "url":
        if len(sys.argv) < 3:
            print("Please provide URL: python network_capture.py url https://example.com")
            sys.exit(1)
        url = sys.argv[2]
        await capture_any_site(url)
    else:
        print(f"Unknown site: {site}")
        print("Available: paytm, zomato, url")


if __name__ == "__main__":
    asyncio.run(main())
