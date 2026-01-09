from O_tps.core import *
from O_tps.localuseragent import *
import subprocess
import os


async def zomato(phone, client, out):
    name = "zomato"
    domain = "zomato.com"
    frequent_rate_limit = False
    
    clean_phone = phone[-10:]
    
    try:
        # Path to playwright helper
        helper_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'playwright_helper.py')
        
        # Run playwright in subprocess
        result = subprocess.run(
            ['python3', helper_path, 'zomato', clean_phone],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        output = result.stdout.strip()
        
        if output == "SUCCESS":
            out.append({
                "name": name,
                "domain": domain,
                "frequent_rate_limit": frequent_rate_limit,
                "rateLimit": False,
                "sent": True,
                "error": False
            })
        elif "rate" in output.lower() or "limit" in output.lower():
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
            
    except subprocess.TimeoutExpired:
        out.append({
            "name": name,
            "domain": domain,
            "frequent_rate_limit": frequent_rate_limit,
            "rateLimit": False,
            "sent": False,
            "error": True
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
