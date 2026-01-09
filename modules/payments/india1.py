from O_tps.core import *
from O_tps.localuseragent import *


async def india1(phone, client, out):
    name = "india1"
    domain = "india1.co.in"
    frequent_rate_limit = False
    
    clean_phone = phone[-10:]
    device_id = f"{uuid4()}-1.1-Web"
    
    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.6',
        'Content-Type': 'application/json',
        'Origin': 'https://digitalweb.india1.co.in',
        'Referer': 'https://digitalweb.india1.co.in/',
        'x-digital-api-key': '1234',
    }
    
    json_data = {
        'mobileNumber': clean_phone,
        'agreedToToc': True,
        'agreedToTocVersion': 'v1',
        'platform': 'Web',
        'deviceId': device_id,
        'appVersion': '1.0.45',
    }
    
    try:
        response = await client.post(
            'https://digitalapi.india1.co.in/v1/auth/send-otp',
            headers=headers,
            json=json_data,
        )
        
        response_text = response.text.lower()
        
        try:
            response_data = response.json()
        except:
            response_data = {}
        
        if response.status_code == 200 or 'success' in response_text or 'otp' in response_text or response_data.get('success') == True:
            out.append({
                "name": name,
                "domain": domain,
                "frequent_rate_limit": frequent_rate_limit,
                "rateLimit": False,
                "sent": True,
                "error": False
            })
            return None
        
        elif 'rate' in response_text or 'limit' in response_text or 'wait' in response_text or 'too many' in response_text:
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
