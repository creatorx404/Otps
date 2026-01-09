from O_tps.core import *
from O_tps.localuseragent import *


async def unitty(phone, client, out):
    name = "unitty"
    domain = "unitty.in"
    frequent_rate_limit = False
    
    clean_phone = phone[-10:]
    
    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Content-Type': 'application/json',
        'Origin': 'https://www.unitty.in',
        'Referer': 'https://www.unitty.in/api_android_one/',
    }
    
    json_data = {
        'mobile': clean_phone,
    }
    
    try:
        response = await client.post(
            'https://www.unitty.in/api_android_one/send_otp.php',
            headers=headers,
            json=json_data,
        )
        
        try:
            response_data = response.json()
        except:
            response_data = {}
        
        if response_data.get('status') == 'success' or 'sent successfully' in str(response_data).lower():
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
