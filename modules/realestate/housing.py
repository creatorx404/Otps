from O_tps.core import *
from O_tps.localuseragent import *


async def housing(phone, client, out):
    name = "housing"
    domain = "login.housing.com"
    frequent_rate_limit = False

    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
    }

    data = {
        'phone': phone,
    }

    response = await client.post(
        'https://login.housing.com/api/v2/send-otp',
        headers=headers,
        data=data,
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
