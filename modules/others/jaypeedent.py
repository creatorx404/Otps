from O_tps.core import *
from O_tps.localuseragent import *


async def jaypeedent(phone, client, out):
    name = "jaypeedent"
    domain = "jaypeedent.com"
    frequent_rate_limit = False
    
    clean_phone = phone[-10:]
    
    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.7',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://jaypeedent.com',
        'Referer': 'https://jaypeedent.com/otp/',
        'X-Requested-With': 'XMLHttpRequest',
    }
    
    data = {
        'action': 'send_otp_ajax',
        'phone': clean_phone,
    }
    
    try:
        response = await client.post(
            'https://jaypeedent.com/wp-admin/admin-ajax.php',
            headers=headers,
            data=data,
        )
        
        response_text = response.text.strip().lower()
        
        if response_text == 'success' or 'success' in response_text:
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
