from O_tps.core import *
from O_tps.localuseragent import *
import uuid


async def paytmmoney(phone, client, out):
    name = "paytmmoney"
    domain = "paytmmoney.com"
    frequent_rate_limit = False
    
    clean_phone = phone[-10:]
    
    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Content-Type': 'application/json',
        'Origin': 'https://login.paytmmoney.com',
        'Referer': 'https://login.paytmmoney.com/',
        'x-client-platform': 'web',
        'x-request-id': str(uuid.uuid4()),
    }
    
    payload = {
        "phone": clean_phone
    }
    
    try:
        response = await client.post(
            'https://login.paytmmoney.com/api/auth/login/sendOTP',
            headers=headers,
            json=payload,
        )
        
        response_text = response.text.lower()
        
        try:
            response_data = response.json()
        except:
            response_data = {}
        
        data = response_data.get('data', {})
        status = data.get('status', '')
        message = data.get('message', '')
        
        if status == 'SUCCESS' or 'otp sent' in message.lower():
            out.append({
                "name": name,
                "domain": domain,
                "frequent_rate_limit": frequent_rate_limit,
                "rateLimit": False,
                "sent": True,
                "error": False
            })
        elif 'rate' in response_text or 'limit' in response_text or 'too many' in response_text:
            out.append({
                "name": name,
                "domain": domain,
                "frequent_rate_limit": frequent_rate_limit,
                "rateLimit": True,
                "sent": False,
                "error": False
            })
        else:
            out.append({
                "name": name,
                "domain": domain,
                "frequent_rate_limit": frequent_rate_limit,
                "rateLimit": False,
                "sent": False,
                "error": False
            })
            
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
