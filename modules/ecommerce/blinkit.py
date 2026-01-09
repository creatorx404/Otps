from O_tps.core import *
from O_tps.localuseragent import *
import subprocess
import json

async def blinkit(phone, client, out):
    name = "blinkit"
    domain = "blinkit.com"
    frequent_rate_limit = False

    # Use shell=True and pass as single string to preserve quotes and structure
    cmd = (
        "curl -s -X POST 'https://blinkit.com/v2/accounts/' "
        "-H 'accept: */*' "
        "-H 'accept-language: en-US,en;q=0.7' "
        "-H 'app_client: consumer_web' "
        "-H 'app_version: 52434332' "
        "-H 'auth_key: c761ec3633c22afad934fb17a66385c1c06c5472b4898b866b7306186d0bb477' "
        "-H 'content-type: application/x-www-form-urlencoded' "
        "-H 'device_id: a4e9874108a96c71' "
        "-H 'lat: 28.4465616' "
        "-H 'lon: 77.040489' "
        "-H 'origin: https://blinkit.com' "
        "-H 'platform: desktop_web' "
        "-H 'priority: u=1, i' "
        "-H 'referer: https://blinkit.com/' "
        "-H 'rn_bundle_version: 1009003012' "
        "-H 'sec-ch-ua: \"Brave\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"' "
        "-H 'sec-ch-ua-mobile: ?0' "
        "-H 'sec-ch-ua-platform: \"Windows\"' "
        "-H 'sec-fetch-dest: empty' "
        "-H 'sec-fetch-mode: cors' "
        "-H 'sec-fetch-site: same-origin' "
        "-H 'sec-gpc: 1' "
        "-H 'session_uuid: fe5c724a-f058-4cc9-ad47-1745bc2c5f29' "
        "-H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36' "
        "-H 'web_app_version: 1008010016' "
        "-b 'gr_1_deviceId=0f2b645f-2617-40fe-9cfc-ea30e928072d; city=Gurgaon; __cfruid=278c1535fc41e61b34faee2c52b5db3f951ba54f-1766053718; _cfuvid=TM7LnyzbXlsDK9UGiYAklBYHMovguKogRqCG_zDGx74-1766053718646-0.0.1.1-604800000; __cf_bm=jXws308g072szvYXvhOws2yrnaVG3uXitDp2nlqx8pU-1766061774-1.0.1.1-znczAyHM7ivruPLgNk14pYylf6Vq7EEbzB50A1XEHHtO0HypMylY7Efzt4OCGbliyzUhKB48NMofDtoQWTm_ZTOG.jPXfpDkgAAUBp9kVjk; gr_1_lat=18.9690247; gr_1_lon=72.8205292; gr_1_locality=Mumbai; gr_1_landmark=Mumbai%20Central%2C%20Mumbai%2C%20Maharashtra%2C%20India' "
        "--data-raw 'user_phone=7533707322'"
    )

    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)

        if result.returncode != 0:
            print(f"[ERROR] curl failed: {result.stderr}")
            out.append({"name": name, "domain": domain, "frequent_rate_limit": frequent_rate_limit, "rateLimit": False, "sent": False, "error": True})
            return

        if not result.stdout.strip():
            print("[ERROR] Empty response from curl")
            out.append({"name": name, "domain": domain, "frequent_rate_limit": frequent_rate_limit, "rateLimit": False, "sent": False, "error": True})
            return

        response_data = json.loads(result.stdout)

        if response_data.get("sms_sent") == True and response_data.get("success") == True:
            out.append({
                "name": name,
                "domain": domain,
                "frequent_rate_limit": frequent_rate_limit,
                "rateLimit": False,
                "sent": True,
                "error": False
            })
        elif "rate" in str(response_data).lower() or "limit" in str(response_data).lower():
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

    except Exception as e:
        print(f"[EXCEPTION] {e}")
        out.append({
            "name": name,
            "domain": domain,
            "frequent_rate_limit": frequent_rate_limit,
            "rateLimit": False,
            "sent": False,
            "error": True
        })
