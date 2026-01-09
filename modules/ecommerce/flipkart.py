from O_tps.core import *
from O_tps.localuseragent import *
import httpx


async def flipkart(phone, client, out):
    name = "flipkart"
    domain = "flipkart.com"
    frequent_rate_limit = False
    
    clean_phone = phone[-10:]
    
    try:
        async with httpx.AsyncClient(timeout=15, follow_redirects=True) as session:
            
            otp_headers = {
                'User-Agent': random.choice(ua["browsers"]["chrome"]),
                'Accept': '*/*',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Origin': 'https://www.flipkart.com',
                'Referer': 'https://www.flipkart.com/',
                'X-User-Agent': 'Mozilla/5.0 FKUA/website/42/website/Desktop',
            }
            
            data = f'loginId=%2B91{clean_phone}'
            
            response = await session.post(
                'https://1.rome.api.flipkart.com/api/5/user/otp/generate',
                headers=otp_headers,
                content=data,
            )
            
            try:
                response_data = response.json()
                status_code = response_data.get('STATUS_CODE', 0)
                resp_obj = response_data.get('RESPONSE', {}) or {}
                remaining = resp_obj.get('remainingAttempts', -1)
                request_id = resp_obj.get('requestId', '')
                error_code = resp_obj.get('errorCode', '')
            except:
                status_code = 0
                remaining = -1
                request_id = ''
                error_code = ''
            
            # SUCCESS
            if status_code == 200 and (request_id or remaining > 0):
                out.append({
                    "name": name,
                    "domain": domain,
                    "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": False,
                    "sent": True,
                    "error": False
                })
                return None
            
            # RATE LIMIT
            elif remaining == 0 or error_code == 'LOGIN_1004' or 'maximum' in str(resp_obj).lower():
                out.append({
                    "name": name,
                    "domain": domain,
                    "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": True,
                    "sent": False,
                    "error": False
                })
                return None
            
            # OTHER
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
