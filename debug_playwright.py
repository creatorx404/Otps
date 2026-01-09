#!/usr/bin/env python3
import sys
import asyncio
from playwright.async_api import async_playwright


async def paytm_otp_debug(phone):
    """
    DEBUG VERSION - Shows browser and takes screenshots
    """
    try:
        async with async_playwright() as p:
            # headless=False so you can SEE what's happening
            browser = await p.firefox.launch(
                headless=False,  # Changed to False to see browser
                args=['--no-sandbox']
            )
            
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
                viewport={'width': 1920, 'height': 1080},
            )
            
            page = await context.new_page()
            
            print("🌐 Step 1: Going to Paytm...")
            await page.goto('https://paytm.com/', timeout=60000)
            await page.wait_for_timeout(5000)  # Wait longer
            
            # Take screenshot of homepage
            await page.screenshot(path='debug_1_homepage.png')
            print("📸 Screenshot saved: debug_1_homepage.png")
            
            # Try to close popups
            print("🔍 Step 2: Looking for popups...")
            try:
                await page.click('button:has-text("Accept")', timeout=2000)
                print("✓ Closed 'Accept' popup")
            except:
                print("⚠ No 'Accept' popup found")
            
            # Look for login button
            print("🔍 Step 3: Looking for Login button...")
            login_clicked = False
            login_selectors = [
                'text="Login/Signup"',
                'text="Login"',
                'text="Sign In"',
                'a:has-text("Login")',
                'button:has-text("Login")',
                '[data-testid="login"]',
            ]
            
            for selector in login_selectors:
                try:
                    print(f"  Trying selector: {selector}")
                    await page.click(selector, timeout=3000)
                    login_clicked = True
                    print(f"✓ Clicked login with: {selector}")
                    await page.wait_for_timeout(3000)
                    break
                except Exception as e:
                    print(f"  ✗ Failed: {selector}")
                    continue
            
            if not login_clicked:
                # Take screenshot before giving up
                await page.screenshot(path='debug_2_no_login.png')
                print("📸 Screenshot saved: debug_2_no_login.png")
                print("\n❌ Could not find login button")
                
                # Print available text on page
                page_text = await page.text_content('body')
                print("\n📄 Page contains these keywords:")
                for keyword in ['login', 'sign', 'account', 'profile']:
                    if keyword.lower() in page_text.lower():
                        print(f"  ✓ Found: {keyword}")
                
                await browser.close()
                return "ERROR:Could not find login button"
            
            # Take screenshot after clicking login
            await page.screenshot(path='debug_3_after_login_click.png')
            print("📸 Screenshot saved: debug_3_after_login_click.png")
            
            # Look for phone input
            print("🔍 Step 4: Looking for phone input...")
            phone_filled = False
            phone_selectors = [
                'input[type="tel"]',
                'input[type="text"]',
                'input[name="mobile"]',
                'input[name="phone"]',
                'input[placeholder*="Mobile"]',
                'input[placeholder*="Phone"]',
                'input[placeholder*="Number"]',
                '#phoneNumber',
                '#mobile',
                'input[maxlength="10"]',
            ]
            
            for selector in phone_selectors:
                try:
                    print(f"  Trying selector: {selector}")
                    await page.fill(selector, phone, timeout=3000)
                    phone_filled = True
                    print(f"✓ Filled phone with: {selector}")
                    break
                except Exception as e:
                    print(f"  ✗ Failed: {selector}")
                    continue
            
            if not phone_filled:
                # Take screenshot and get HTML
                await page.screenshot(path='debug_4_no_phone_input.png')
                print("📸 Screenshot saved: debug_4_no_phone_input.png")
                
                # Try to get all input fields
                print("\n🔍 All input fields found on page:")
                inputs = await page.query_selector_all('input')
                for i, inp in enumerate(inputs):
                    input_type = await inp.get_attribute('type')
                    input_name = await inp.get_attribute('name')
                    input_placeholder = await inp.get_attribute('placeholder')
                    input_id = await inp.get_attribute('id')
                    print(f"  Input {i+1}: type={input_type}, name={input_name}, placeholder={input_placeholder}, id={input_id}")
                
                await browser.close()
                return "ERROR:Could not find phone input"
            
            await page.wait_for_timeout(2000)
            
            # Take screenshot after filling phone
            await page.screenshot(path='debug_5_phone_filled.png')
            print("📸 Screenshot saved: debug_5_phone_filled.png")
            
            # Look for submit button
            print("🔍 Step 5: Looking for submit button...")
            button_clicked = False
            button_selectors = [
                'button:has-text("Send OTP")',
                'button:has-text("Proceed")',
                'button:has-text("Continue")',
                'button:has-text("Get OTP")',
                'button:has-text("Next")',
                'button[type="submit"]',
                'input[type="submit"]',
            ]
            
            for selector in button_selectors:
                try:
                    print(f"  Trying selector: {selector}")
                    await page.click(selector, timeout=3000)
                    button_clicked = True
                    print(f"✓ Clicked button with: {selector}")
                    break
                except Exception as e:
                    print(f"  ✗ Failed: {selector}")
                    continue
            
            if not button_clicked:
                await page.screenshot(path='debug_6_no_button.png')
                print("📸 Screenshot saved: debug_6_no_button.png")
                
                # Find all buttons
                print("\n🔍 All buttons found on page:")
                buttons = await page.query_selector_all('button')
                for i, btn in enumerate(buttons):
                    btn_text = await btn.text_content()
                    btn_type = await btn.get_attribute('type')
                    print(f"  Button {i+1}: text='{btn_text}', type={btn_type}")
                
                await browser.close()
                return "ERROR:Could not find submit button"
            
            # Wait for response
            print("⏳ Step 6: Waiting for response...")
            await page.wait_for_timeout(5000)
            
            # Take final screenshot
            await page.screenshot(path='debug_7_final.png')
            print("📸 Screenshot saved: debug_7_final.png")
            
            # Check result
            page_content = await page.content()
            page_lower = page_content.lower()
            
            print("\n🔍 Checking for success indicators...")
            if any(x in page_lower for x in ['enter otp', 'otp sent', 'verify otp']):
                print("✅ SUCCESS - OTP page detected!")
                await browser.close()
                return "SUCCESS"
            elif any(x in page_lower for x in ['too many', 'limit', 'wait']):
                print("⚠️ RATE_LIMIT detected")
                await browser.close()
                return "RATE_LIMIT"
            else:
                print("❓ UNKNOWN response")
                # Print some page content
                print("\n📄 Page keywords found:")
                for word in ['otp', 'verify', 'error', 'invalid', 'limit']:
                    if word in page_lower:
                        print(f"  ✓ Found: {word}")
                await browser.close()
                return "UNKNOWN"
            
    except Exception as e:
        print(f"\n❌ EXCEPTION: {str(e)}")
        return f"ERROR:{str(e)}"


async def zomato_otp_debug(phone):
    """
    DEBUG VERSION for Zomato
    """
    try:
        async with async_playwright() as p:
            browser = await p.firefox.launch(headless=False)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
            )
            page = await context.new_page()
            
            print("🌐 Step 1: Going to Zomato...")
            await page.goto('https://www.zomato.com/', timeout=60000)
            await page.wait_for_timeout(5000)
            
            await page.screenshot(path='debug_zomato_1_homepage.png')
            print("📸 Screenshot: debug_zomato_1_homepage.png")
            
            print("🔍 Step 2: Looking for Login button...")
            login_selectors = ['text=Log in', 'text=Login', 'text=Sign in', 'text=Sign In']
            login_clicked = False
            
            for selector in login_selectors:
                try:
                    print(f"  Trying: {selector}")
                    await page.click(selector, timeout=5000)
                    login_clicked = True
                    print(f"✓ Clicked: {selector}")
                    await page.wait_for_timeout(3000)
                    break
                except:
                    print(f"  ✗ Failed: {selector}")
            
            if not login_clicked:
                print("⚠️ No login button found, continuing anyway...")
            
            await page.screenshot(path='debug_zomato_2_after_login.png')
            print("📸 Screenshot: debug_zomato_2_after_login.png")
            
            print("🔍 Step 3: Looking for phone input...")
            phone_selectors = [
                'input[type="tel"]',
                'input[type="text"]',
                'input[name="phone"]',
                'input[placeholder*="phone"]',
                'input[placeholder*="Phone"]',
                'input[placeholder*="number"]',
            ]
            
            phone_filled = False
            for selector in phone_selectors:
                try:
                    print(f"  Trying: {selector}")
                    await page.fill(selector, phone, timeout=5000)
                    phone_filled = True
                    print(f"✓ Filled phone: {selector}")
                    break
                except:
                    print(f"  ✗ Failed: {selector}")
            
            if not phone_filled:
                print("\n🔍 All inputs on page:")
                inputs = await page.query_selector_all('input')
                for i, inp in enumerate(inputs):
                    input_type = await inp.get_attribute('type')
                    input_placeholder = await inp.get_attribute('placeholder')
                    print(f"  Input {i+1}: type={input_type}, placeholder={input_placeholder}")
                
                await browser.close()
                return "ERROR:Could not find phone input"
            
            await page.wait_for_timeout(1000)
            await page.screenshot(path='debug_zomato_3_phone_filled.png')
            
            print("🔍 Step 4: Looking for Send button...")
            button_selectors = [
                'button:has-text("Send")',
                'button:has-text("Continue")',
                'button:has-text("Proceed")',
                'button[type="submit"]',
            ]
            
            for selector in button_selectors:
                try:
                    print(f"  Trying: {selector}")
                    await page.click(selector, timeout=3000)
                    print(f"✓ Clicked: {selector}")
                    break
                except:
                    print(f"  ✗ Failed: {selector}")
            
            await page.wait_for_timeout(5000)
            await page.screenshot(path='debug_zomato_4_final.png')
            print("📸 Screenshot: debug_zomato_4_final.png")
            
            content = await page.content()
            if 'otp' in content.lower() or 'verify' in content.lower():
                print("✅ SUCCESS")
                await browser.close()
                return "SUCCESS"
            
            print("❓ FAILED or UNKNOWN")
            await browser.close()
            return "FAILED"
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return f"ERROR:{e}"


async def main():
    if len(sys.argv) < 3:
        print("Usage: python debug_playwright.py <site> <phone>")
        print("Available sites: paytm, zomato")
        sys.exit(1)
    
    site = sys.argv[1].lower()
    phone = sys.argv[2][-10:]
    
    print(f"\n{'='*60}")
    print(f"🔍 DEBUG MODE - Testing {site.upper()}")
    print(f"{'='*60}\n")
    
    if site == "paytm":
        result = await paytm_otp_debug(phone)
    elif site == "zomato":
        result = await zomato_otp_debug(phone)
    else:
        result = "ERROR:Unknown site"
    
    print(f"\n{'='*60}")
    print(f"📊 FINAL RESULT: {result}")
    print(f"{'='*60}\n")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
