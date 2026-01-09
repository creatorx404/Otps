from O_tps.core import *
from O_tps.localuseragent import *


async def citymall(phone, client, out):
    name = "citymall"
    domain = "citymall.live"
    frequent_rate_limit = False
    
    clean_phone = phone[-10:]
    
    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.6',
        'Content-Type': 'application/json',
        'Origin': 'https://citymall.live',
        'Referer': 'https://citymall.live/',
        'x-app-name': 'WEB',
        'x-platform-os': 'WEB2',
        'x-requested-with': 'WEB',
    }
    
    json_data = {
        'phone_number': clean_phone,
    }
    
    try:
        response = await client.post(
            'https://citymall.live/api/gateway/cl-user/auth/get-otp',
            headers=headers,
            json=json_data,
        )
        
        try:
            response_data = response.json()
        except:
            response_data = {}
        
        if response_data.get('message') == 'success' or response.status_code == 200:
            out.append({
                "name": name,
                "domain": domain,
                "frequent_rate_limit": frequent_rate_limit,
                "rateLimit": False,
                "sent": True,
                "error": False
            })
            return None
        
        elif 'rate' in str(response_data).lower() or 'limit' in str(response_data).lower() or 'wait' in str(response_data).lower():
            out.append({
                "name": name,
                "domain": domain,
                "frequent_rate_limit": frequent_rate_limit,
                "rateLimit": True,
                "sent": False,
                "error": False
            })
            return None
        
        else:
            out.append({
                "name": name,
                "domain": domain,
                "frequent_rate_limit": frequent_rate_limit,
                "rateLimit": False,
                "sent": False,
                "error": False
            })
            return None
            
    except Exception as e:
        out.append({
            "name": name,
            "domain": domain,
            "frequent_rate_limit": frequent_rate_limit,
            "rateLimit": False,
            "sent": False,
            "error": True
        })
        return None
