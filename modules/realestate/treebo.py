from O_tps.core import *
from O_tps.localuseragent import *


async def treebo(phone, client, out):
    name = "treebo"
    domain = "treebo.com"
    frequent_rate_limit = False

    data = {
        "phone_number": phone
    }

    try:
        response = await client.post(
            "https://www.treebo.com/api/v2/auth/login/otp/",
            json=data
        )

        if "sent" in response.text:
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
