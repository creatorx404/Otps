# Module: indialends
# URL: https://indialends.com/internal/a/mobile-verification_v2.ashx
# Method: POST

from O_tps.core import *
from O_tps.localuseragent import *


async def indialends(phone, client, out):
    name = "indialends"
    domain = "indialends"
    frequent_rate_limit = False

    headers = {
        'user-agent': random.choice(ua["browsers"]["chrome"]),
        'Referer': 'https://indialends.com/personal-loan',
    }

    cookies = {
        '_ga': 'GA1.2.1483885314.1559157646',
        '_fbp': 'fb.1.1559157647161.1989205138',
        'TiPMix': '91.9909185226964',
        'gcb_t_track': 'SEO - Google',
        'gcb_t_keyword': '',
        'gcb_t_l_url': 'https://www.google.com/',
        'gcb_utm_medium': '',
        'gcb_utm_campaign': '',
        'ASP.NET_SessionId': 'ioqkek5lbgvldlq4i3cmijcs',
        'web_app_landing_utm_source': '',
        'web_app_landing_url': '/personal-loan',
        'webapp_landing_referral_url': 'https://www.google.com/',
        'ARRAffinity': '747e0c2664f5cb6179583963d834f4899eee9f6c8dcc773fc05ce45fa06b2417',
        '_gid': 'GA1.2.969623705.1560660444',
        '_gat': '1',
        'current_url': 'https://indialends.com/personal-loan',
        'cookies_plbt': '0',
    }

    data = {
        'aeyder03teaeare': '1',
        'ertysvfj74sje': phone,
        'jfsdfu14hkgertd': phone,
        'lj80gertdfg': '0',
    }

    try:
        response = await client.post(
            'https://indialends.com/internal/a/mobile-verification_v2.ashx',
            headers=headers,
            cookies=cookies,
            data=data,
        )

        # Success identifier: '1'
        if '1' in response.text.lower():
            out.append({
                "name": name,
                "domain": domain,
                "frequent_rate_limit": frequent_rate_limit,
                "rateLimit": False,
                "sent": True,
                "error": False
            })
            return None

        elif response.status_code == 429 or 'rate' in response.text.lower() or 'limit' in response.text.lower() or 'wait' in response.text.lower():
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