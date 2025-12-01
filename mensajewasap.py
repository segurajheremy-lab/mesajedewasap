from dotenv import load_dotenv
import os
import asyncio
from playwright.async_api import async_playwright
load_dotenv("datospersonales.env")
CONTACTO = os.getenv("CONTACTO")
MENSAJE = os.getenv("MENSAJE")
async def main():
    if not CONTACTO or not MENSAJE:
        print("no definiste bien el contacto o el mensaje")
        return
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://web.whatsapp.com")
        print("escanea en QR manito y dale al enter")
        input()
        search_selector = 'div[contenteditable="true"][data-tab="3"]'
        await page.wait_for_selector(search_selector)
        await page.fill(search_selector, CONTACTO)
        await page.wait_for_selector(f"text={CONTACTO}")
        await page.click(f"text={CONTACTO}")
        msg_selector = 'div[aria-placeholder="Escribe un mensaje"]'
        await page.wait_for_selector(msg_selector)
        await page.fill(msg_selector, MENSAJE)
        await page.keyboard.press("Enter")
        print("ya esta queloque")
        await page.wait_for_timeout(1500)
        await browser.close()
        if __name__== "__main__":
            asyncio.run(main())
