from O_tps.core import *
from O_tps.localuseragent import *


async def redbus(phone, client, out):
    name = "redbus"
    domain = "redbus.in"
    frequent_rate_limit = False

    headers = {
        "User-Agent": random.choice(ua["browsers"]["chrome"]),
        "Referer": "https://m.redbus.in/",
        "Origin": "https://m.redbus.in",
        "Content-Type": "application/json"
    }

    params = {
        "number": phone,
        "cc": "91",  # Assuming the default country code
        "whatsAppOpted": True  # Enabling WhatsApp request
    }

    try:
        response = await client.get(
            "https://m.redbus.in/api/getOtp",
            params=params,
            headers=headers
        )

        if response.status_code == 200 and "200" in response.text:
            out.append({
                "name": name,
                "domain": domain,
                "rateLimit": False,
                "sent": True,
                "error": False
            })
        else:
            out.append({
                "name": name,
                "domain": domain,
                "rateLimit": False,
                "sent": False,
                "error": False
            })
    except Exception as e:
        print(f"Error in module {name}: {e}")
        out.append({
            "name": name,
            "domain": domain,
            "rateLimit": False,
            "sent": False,
            "error": True
        })
