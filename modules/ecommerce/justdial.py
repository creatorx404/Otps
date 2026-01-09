from O_tps.core import *
from O_tps.localuseragent import *


async def justdial(phone, client, out):
    name = "justdial"
    domain = "t.justdial.com"
    frequent_rate_limit = False

    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
    }

    params = {
        'mobile': phone,
    }

    response = await client.get(
        'https://t.justdial.com/api/india_api_write/18july2018/sendvcode.php',
        headers=headers,
        params=params,
    )

    try:
        response_data = response.json()
        if "sent" in str(response_data).lower() or response_data.get("success") == True or response_data.get("msg") == "success":
            out.append({
                "name": name,
                "domain": domain,
                "frequent_rate_limit": frequent_rate_limit,
                "rateLimit": False,
                "sent": True,
                "error": False
            })
            return None

        elif "rate" in str(response_data).lower() or "limit" in str(response_data).lower() or "wait" in str(response_data).lower():
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
            print(f"Error: Unexpected response from {name}: {response_data}")
            return None

    except Exception:
        out.append({
            "name": name,
            "domain": domain,
            "frequent_rate_limit": frequent_rate_limit,
            "rateLimit": False,
            "sent": False,
            "error": True
        })
        return None
