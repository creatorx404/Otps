from O_tps.core import *
from O_tps.localuseragent import *
import httpx


async def mccpropertytax(phone, client, out):
    name = "mccpropertytax"
    domain = "mccpropertytax.in"
    frequent_rate_limit = False
    
    clean_phone = phone[-10:]
    
    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Origin': 'https://www.mccpropertytax.in',
        'Referer': 'https://www.mccpropertytax.in/',
    }
    
    try:
        # Create new client with SSL verification disabled
        async with httpx.AsyncClient(verify=False, timeout=10) as insecure_client:
            response = await insecure_client.get(
                f'https://mccpropertytax.in/API/api/Otp?number={clean_phone}',
                headers=headers,
            )
            
            response_text = response.text.strip().lower()
            
            if 'success' in response_text or 'sent' in response_text or response.status_code == 200:
                out.append({
                    "name": name,
                    "domain": domain,
                    "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": False,
                    "sent": True,
                    "error": False
                })
                return None
            
            elif 'rate' in response_text or 'limit' in response_text or 'wait' in response_text:
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
