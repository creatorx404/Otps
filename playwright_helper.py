#!/usr/bin/env python3
import sys
import asyncio
import random
from playwright.async_api import async_playwright


async def airtel_otp(phone):
    try:
        async with async_playwright() as p:
            browser = await p.firefox.launch(headless=True, args=['--no-sandbox'])
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
                viewport={'width': 1920, 'height': 1080},
            )
            page = await context.new_page()
            
            await page.goto('https://www.airtel.in/manage-account/login', timeout=60000)
            await page.wait_for_timeout(3000)
            
            for sel in ['button:has-text("Accept")', '[aria-label="Close"]']:
                try:
                    await page.click(sel, timeout=2000)
                except:
                    pass
            
            phone_filled = False
            for selector in ['input[type="tel"]', 'input[name="mobile"]', 'input[placeholder*="Mobile"]', 'input[maxlength="10"]']:
                try:
                    await page.fill(selector, phone, timeout=3000)
                    phone_filled = True
                    break
                except:
                    continue
            
            if not phone_filled:
                await browser.close()
                return "ERROR:Could not find phone input"
            
            await page.wait_for_timeout(1000)
            
            for selector in ['button:has-text("Get OTP")', 'button:has-text("GET OTP")', 'button:has-text("Continue")', 'button[type="submit"]']:
                try:
                    await page.click(selector, timeout=3000)
                    break
                except:
                    continue
            
            await page.wait_for_timeout(5000)
            content = (await page.content()).lower()
            await browser.close()
            
            if any(x in content for x in ['enter otp', 'otp sent', 'otp has been sent', 'verify otp', 'verification code']):
                return "SUCCESS"
            elif any(x in content for x in ['too many', 'try again later', 'limit reached', 'maximum attempts']):
                return "RATE_LIMIT"
            return "FAILED"
    except Exception as e:
        return f"ERROR:{str(e)}"


async def digilocker_otp(phone):
    try:
        async with async_playwright() as p:
            browser = await p.firefox.launch(headless=True, args=['--no-sandbox'])
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
                viewport={'width': 1920, 'height': 1080},
            )
            page = await context.new_page()
            
            await page.goto('https://www.digilocker.gov.in/', timeout=60000)
            await page.wait_for_timeout(3000)
            
            for selector in ['text=Sign In', 'text=Login', 'a:has-text("Sign In")', 'button:has-text("Sign In")']:
                try:
                    await page.click(selector, timeout=3000)
                    await page.wait_for_timeout(2000)
                    break
                except:
                    continue
            
            await page.wait_for_timeout(2000)
            
            phone_filled = False
            for selector in ['input[type="tel"]', 'input[name="mobile"]', 'input[name="mobile_number"]', 'input[placeholder*="Mobile"]', 'input[maxlength="10"]']:
                try:
                    await page.fill(selector, phone, timeout=3000)
                    phone_filled = True
                    break
                except:
                    continue
            
            if not phone_filled:
                await browser.close()
                return "ERROR:Could not find phone input"
            
            await page.wait_for_timeout(1000)
            
            for selector in ['button:has-text("Send OTP")', 'button:has-text("Get OTP")', 'button:has-text("Continue")', 'button[type="submit"]']:
                try:
                    await page.click(selector, timeout=3000)
                    break
                except:
                    continue
            
            await page.wait_for_timeout(5000)
            content = (await page.content()).lower()
            await browser.close()
            
            if any(x in content for x in ['enter otp', 'otp sent', 'verify otp', 'verification', 'redirecting']):
                return "SUCCESS"
            elif any(x in content for x in ['too many', 'limit', 'try again', 'maximum']):
                return "RATE_LIMIT"
            return "FAILED"
    except Exception as e:
        return f"ERROR:{e}"


async def paisabazaar_otp(phone, channel="sms"):
    try:
        async with async_playwright() as p:
            browser = await p.firefox.launch(headless=True, args=['--no-sandbox'])
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
                viewport={'width': 1920, 'height': 1080},
            )
            page = await context.new_page()
            
            await page.goto('https://accounts1.paisabazaar.com/login?client_id=6dff40ff-65e4-40fe-8b40-01be8b1698d6&source_site_id=b9df9faa-0bab-4c6c-bb77-ebe87bc9b2da&redirect_uri=https://creditreport.paisabazaar.com/bureau/report-analysis&auth_type=otp&screen_type=2&journey_type=REDIRECT&version=1', timeout=60000)
            await page.wait_for_timeout(5000)
            
            for sel in ['button:has-text("Accept")', '[aria-label="Close"]']:
                try:
                    await page.click(sel, timeout=2000)
                except:
                    pass
            
            phone_filled = False
            for selector in ['input[placeholder*="mobile number"]', 'input[placeholder*="Mobile"]', 'input[type="tel"]', 'input[type="number"]', 'input[maxlength="10"]']:
                try:
                    await page.fill(selector, phone, timeout=3000)
                    phone_filled = True
                    break
                except:
                    continue
            
            if not phone_filled:
                await browser.close()
                return "ERROR:Could not find phone input"
            
            await page.wait_for_timeout(1000)
            
            if channel.lower() == "whatsapp":
                for selector in ['text=WhatsApp', 'text=Whatsapp', 'label:has-text("WhatsApp")', 'span:has-text("WhatsApp")']:
                    try:
                        await page.click(selector, timeout=2000)
                        break
                    except:
                        continue
            
            await page.wait_for_timeout(500)
            
            for selector in ['button:has-text("Get OTP")', 'button:has-text("GET OTP")', 'button:has-text("Send OTP")', 'button[type="submit"]']:
                try:
                    await page.click(selector, timeout=3000)
                    break
                except:
                    continue
            
            await page.wait_for_timeout(5000)
            content = (await page.content()).lower()
            await browser.close()
            
            if any(x in content for x in ['enter otp', 'otp sent', 'verify otp', 'verification', 'we have sent']):
                return "SUCCESS"
            elif any(x in content for x in ['too many', 'limit', 'try again', 'maximum']):
                return "RATE_LIMIT"
            return "FAILED"
    except Exception as e:
        return f"ERROR:{e}"


async def bajajfinserv_otp(phone):
    try:
        async with async_playwright() as p:
            browser = await p.firefox.launch(headless=True, args=['--no-sandbox'])
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
                viewport={'width': 1920, 'height': 1080},
            )
            page = await context.new_page()
            
            await page.goto('https://www.bajajfinserv.in/myaccountlogin', timeout=60000)
            await page.wait_for_timeout(5000)
            
            for sel in ['button:has-text("Accept")', '[aria-label="Close"]', 'button.close', 'button:has-text("OK")']:
                try:
                    await page.click(sel, timeout=2000)
                except:
                    pass
            
            await page.wait_for_timeout(2000)
            
            phone_filled = False
            for selector in ['input[type="tel"]', 'input[type="text"]', 'input[type="number"]', 'input[name="mobile"]', 'input[placeholder*="Mobile"]', 'input[placeholder*="mobile"]', 'input[maxlength="10"]']:
                try:
                    await page.fill(selector, phone, timeout=3000)
                    phone_filled = True
                    break
                except:
                    continue
            
            if not phone_filled:
                await browser.close()
                return "ERROR:Could not find phone input"
            
            await page.wait_for_timeout(1000)
            
            for selector in ['button:has-text("Get OTP")', 'button:has-text("GET OTP")', 'button:has-text("Send OTP")', 'button:has-text("Continue")', 'button:has-text("Proceed")', 'button[type="submit"]']:
                try:
                    await page.click(selector, timeout=3000)
                    break
                except:
                    continue
            
            await page.wait_for_timeout(5000)
            content = (await page.content()).lower()
            await browser.close()
            
            if any(x in content for x in ['enter otp', 'otp sent', 'verify otp', 'verification', 'we have sent']):
                return "SUCCESS"
            elif any(x in content for x in ['too many', 'limit', 'try again', 'maximum']):
                return "RATE_LIMIT"
            return "FAILED"
    except Exception as e:
        return f"ERROR:{e}"


async def hdfcbank_otp(phone):
    """HDFC Bank Xpressway OTP - with random DOB (18+ years)"""
    try:
        async with async_playwright() as p:
            browser = await p.firefox.launch(headless=True, args=['--no-sandbox'])
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
                viewport={'width': 1920, 'height': 1080},
            )
            page = await context.new_page()
            
            await page.goto('https://applyonline.hdfcbank.com/xpressway.html', timeout=60000)
            await page.wait_for_timeout(8000)
            
            # Fill phone
            tel_input = page.locator('input[type="tel"]:visible').first
            await tel_input.click()
            await tel_input.press_sequentially(phone, delay=100)
            
            await page.wait_for_timeout(1000)
            
            # Random DOB (18+ years)
            day = str(random.randint(1, 28)).zfill(2)
            month = str(random.randint(1, 12)).zfill(2)
            year = str(random.randint(1970, 2006))
            
            # Day
            day_input = page.locator('input[placeholder=" DD "]')
            await day_input.click()
            await page.wait_for_timeout(200)
            await day_input.press_sequentially(day, delay=150)
            
            await page.wait_for_timeout(500)
            
            # Month
            month_input = page.locator('input[placeholder=" MM "]')
            await month_input.click()
            await page.wait_for_timeout(200)
            await month_input.press_sequentially(month, delay=150)
            
            await page.wait_for_timeout(500)
            
            # Year
            year_input = page.locator('input[placeholder=" YYYY"]')
            await year_input.click()
            await page.wait_for_timeout(300)
            await year_input.click(click_count=3)
            await page.wait_for_timeout(200)
            await year_input.press_sequentially(year, delay=200)
            
            await page.wait_for_timeout(1500)
            await page.click('body')
            await page.wait_for_timeout(1000)
            
            # Click Request OTP
            await page.click('button:has-text("Request OTP")')
            
            await page.wait_for_timeout(5000)
            
            content = (await page.content()).lower()
            await browser.close()
            
            if any(x in content for x in ['resend', 'enter otp', 'otp sent', 'verify otp', 'submit']):
                return "SUCCESS"
            elif any(x in content for x in ['too many', 'limit', 'try again', 'maximum']):
                return "RATE_LIMIT"
            return "FAILED"
            
    except Exception as e:
        return f"ERROR:{e}"


async def mobikwik_otp(phone):
    """Mobikwik OTP via browser automation"""
    try:
        async with async_playwright() as p:
            browser = await p.firefox.launch(headless=True, args=['--no-sandbox'])
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
                viewport={'width': 1920, 'height': 1080},
            )
            page = await context.new_page()
            
            await page.goto('https://www.mobikwik.com/login', timeout=60000)
            await page.wait_for_timeout(5000)
            
            # Close popups
            for sel in ['button:has-text("Accept")', '[aria-label="Close"]', 'button.close', 'button:has-text("×")']:
                try:
                    await page.click(sel, timeout=2000)
                except:
                    pass
            
            await page.wait_for_timeout(2000)
            
            # Fill phone
            phone_filled = False
            for selector in [
                'input[type="tel"]',
                'input[type="text"]',
                'input[type="number"]',
                'input[name="mobile"]',
                'input[name="phone"]',
                'input[placeholder*="Mobile"]',
                'input[placeholder*="mobile"]',
                'input[placeholder*="Phone"]',
                'input[placeholder*="phone"]',
                'input[placeholder*="Enter"]',
                'input[maxlength="10"]',
            ]:
                try:
                    inp = page.locator(selector).first
                    if await inp.is_visible():
                        await inp.click()
                        await inp.press_sequentially(phone, delay=100)
                        phone_filled = True
                        break
                except:
                    continue
            
            if not phone_filled:
                await browser.close()
                return "ERROR:Could not find phone input"
            
            await page.wait_for_timeout(1000)
            
            # Click Continue/Get OTP
            for selector in [
                'button:has-text("Continue")',
                'button:has-text("CONTINUE")',
                'button:has-text("Get OTP")',
                'button:has-text("GET OTP")',
                'button:has-text("Send OTP")',
                'button:has-text("Proceed")',
                'button[type="submit"]',
            ]:
                try:
                    btn = page.locator(selector)
                    if await btn.is_visible():
                        await btn.click()
                        break
                except:
                    continue
            
            await page.wait_for_timeout(5000)
            
            content = (await page.content()).lower()
            await browser.close()
            
            if any(x in content for x in ['enter otp', 'otp sent', 'verify otp', 'verification', 'we have sent', 'resend']):
                return "SUCCESS"
            elif any(x in content for x in ['too many', 'limit', 'try again', 'maximum']):
                return "RATE_LIMIT"
            return "FAILED"
            
    except Exception as e:
        return f"ERROR:{e}"


async def main():
    if len(sys.argv) < 3:
        print("ERROR:Usage: python playwright_helper.py <site> <phone>")
        print("Available: airtel, digilocker, paisabazaar, paisabazaar_whatsapp, bajajfinserv, hdfcbank, mobikwik")
        sys.exit(1)
    
    site = sys.argv[1].lower()
    phone = sys.argv[2][-10:]
    
    sites = {
        'airtel': lambda p: airtel_otp(p),
        'digilocker': lambda p: digilocker_otp(p),
        'paisabazaar': lambda p: paisabazaar_otp(p, "sms"),
        'paisabazaar_whatsapp': lambda p: paisabazaar_otp(p, "whatsapp"),
        'bajajfinserv': lambda p: bajajfinserv_otp(p),
        'hdfcbank': lambda p: hdfcbank_otp(p),
        'mobikwik': lambda p: mobikwik_otp(p),
    }
    
    if site in sites:
        result = await sites[site](phone)
    else:
        result = f"ERROR:Unknown site. Available: {', '.join(sites.keys())}"
    
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
