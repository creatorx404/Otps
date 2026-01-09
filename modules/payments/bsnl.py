from O_tps.core import *
from O_tps.localuseragent import *


async def bsnl(phone, client, out):
    name = "bsnl"
    domain = "bsnl.co.in"
    frequent_rate_limit = False
    
    clean_phone = phone[-10:]
    
    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Referer': 'http://selfcareprepaidnz.bsnl.co.in/webselfcare/faces/login.jspx',
        'Upgrade-Insecure-Requests': '1',
    }
    
    try:
        # Step 1: GET login page to obtain session cookie and ViewState
        response = await client.get(
            'http://selfcareprepaidnz.bsnl.co.in/webselfcare/faces/login.jspx',
            headers=headers,
        )
        
        # Extract ViewState from HTML
        view_state = None
        if 'javax.faces.ViewState' in response.text:
            match = re.search(r'name="javax\.faces\.ViewState"\s+value="([^"]+)"', response.text)
            if match:
                view_state = match.group(1)
        
        if not view_state:
            # Try alternate pattern
            match = re.search(r'ViewState"\s*value="([^"]+)"', response.text)
            if match:
                view_state = match.group(1)
        
        if not view_state:
            print(f"[BSNL] Could not extract ViewState")
            out.append({
                "name": name,
                "domain": domain,
                "frequent_rate_limit": frequent_rate_limit,
                "rateLimit": False,
                "sent": False,
                "error": True
            })
            return None
        
        # Step 2: POST form with phone number
        form_data = {
            'j_id3': 'j_id3',
            'identifierID': clean_phone,
            'submitLoginID': 'submitLoginID',
            'org.apache.myfaces.trinidad.faces.FORM': 'j_id3',
            'javax.faces.ViewState': view_state,
        }
        
        post_headers = {
            'User-Agent': random.choice(ua["browsers"]["chrome"]),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'http://selfcareprepaidnz.bsnl.co.in',
            'Referer': 'http://selfcareprepaidnz.bsnl.co.in/webselfcare/faces/login.jspx',
        }
        
        response = await client.post(
            'http://selfcareprepaidnz.bsnl.co.in/webselfcare/faces/login.jspx',
            headers=post_headers,
            data=form_data,
        )
        
        # Check response - look for OTP page or success indicators
        response_text = response.text.lower()
        
        if 'otp' in response_text or 'verify' in response_text or 'sent' in response_text or 'enter otp' in response_text:
            out.append({
                "name": name,
                "domain": domain,
                "frequent_rate_limit": frequent_rate_limit,
                "rateLimit": False,
                "sent": True,
                "error": False
            })
            return None
        
        elif 'invalid' in response_text or 'error' in response_text or 'not found' in response_text:
            out.append({
                "name": name,
                "domain": domain,
                "frequent_rate_limit": frequent_rate_limit,
                "rateLimit": False,
                "sent": False,
                "error": False
            })
            print(f"[BSNL] Invalid number or error in response")
            return None
        
        else:
            # Might still have worked - check for redirect or page change
            out.append({
                "name": name,
                "domain": domain,
                "frequent_rate_limit": frequent_rate_limit,
                "rateLimit": False,
                "sent": False,
                "error": False
            })
            print(f"[BSNL] Unknown response, check manually")
            return None
            
    except Exception as e:
        print(f"[BSNL] Exception: {e}")
        out.append({
            "name": name,
            "domain": domain,
            "frequent_rate_limit": frequent_rate_limit,
            "rateLimit": False,
            "sent": False,
            "error": True
        })
        return None
