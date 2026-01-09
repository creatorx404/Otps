from O_tps.core import *
from O_tps.localuseragent import *


async def trainingonline(phone, client, out):
    name = "trainingonline"
    domain = "trainingonline.gov.in"
    frequent_rate_limit = False
    
    clean_phone = phone[-10:]
    
    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://trainingonline.gov.in',
        'Referer': 'https://trainingonline.gov.in/preCheckTraineeDetails.htm',
    }
    
    data = {
        'mobileNo': clean_phone,
    }
    
    try:
        response = await client.post(
            'https://trainingonline.gov.in/preCheckTraineeDetails.htm',
            headers=headers,
            data=data,
        )
        
        response_text = response.text.lower()
        
        if 'otp' in response_text or 'sent' in response_text or 'success' in response_text or 'verify' in response_text:
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
