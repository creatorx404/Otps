from O_tps.core import *
from O_tps.localuseragent import *


async def moneyview(phone, client, out):
    name = "moneyview"
    domain = "moneyview.in"
    frequent_rate_limit = False
    
    clean_phone = phone[-10:]
    
    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Origin': 'https://moneyview.in',
        'Referer': 'https://moneyview.in/',
    }
    
    # Multipart form data
    boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
    
    body = f'''------WebKitFormBoundary7MA4YWxkTrZu0gW\r
Content-Disposition: form-data; name="key"\r
\r
MOBILE\r
------WebKitFormBoundary7MA4YWxkTrZu0gW\r
Content-Disposition: form-data; name="mobile"\r
\r
{clean_phone}\r
------WebKitFormBoundary7MA4YWxkTrZu0gW\r
Content-Disposition: form-data; name="source"\r
\r
pwa\r
------WebKitFormBoundary7MA4YWxkTrZu0gW--\r
'''
    
    headers['Content-Type'] = f'multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW'
    
    try:
        response = await client.post(
            'https://pwa.gw.moneyview.in/uis/pwa/generate-otp',
            headers=headers,
            content=body,
        )
        
        response_text = response.text.lower()
        
        try:
            response_data = response.json()
        except:
            response_data = {}
        
        status = response_data.get('status', '')
        otp_id = response_data.get('data', {}).get('otpId', '') if response_data.get('data') else ''
        
        if status == 'SUCCESS' or otp_id or 'success' in response_text:
            out.append({
                "name": name,
                "domain": domain,
                "frequent_rate_limit": frequent_rate_limit,
                "rateLimit": False,
                "sent": True,
                "error": False
            })
            return None
        
        elif 'rate' in response_text or 'limit' in response_text or 'too many' in response_text:
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
