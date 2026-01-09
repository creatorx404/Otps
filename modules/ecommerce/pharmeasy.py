from O_tps.core import *
from O_tps.localuseragent import *


async def pharmeasy(phone, client, out):
    name = "pharmeasy"
    domain = "pharmeasy.in"
    frequent_rate_limit = False

    data = {
        "contactNumber": phone
    }

    try:
        response = await client.post(
            "https://pharmeasy.in/api/auth/requestOTP",
            json=data
        )

        if "resendSmsCounter" in response.text:
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
