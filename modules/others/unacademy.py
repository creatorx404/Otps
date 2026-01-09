from O_tps.core import *
from O_tps.localuseragent import *


async def unacademy(phone, client, out):
    name = "unacademy"
    domain = "unacademy.com"
    frequent_rate_limit = False

    data = {
        "phone": phone
    }

    try:
        response = await client.post(
            "https://unacademy.com/api/v1/user/get_app_link/",
            json=data
        )

        if response.status_code == 200 and "sent" in response.text:
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
