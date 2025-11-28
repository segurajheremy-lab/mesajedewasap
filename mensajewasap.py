from dotenv import load_dotenv
import os
import asyncio
from playwright.async_api import async_playwright

# cargar variables desde datospersonales.env
load_dotenv("datospersonales.env")

CONTACTO = os.getenv("CONTACTO")
MENSAJE = os.getenv("MENSAJE")

async def main():
    if not CONTACTO or not MENSAJE:
        print("Error: CONTACTO o MENSAJE no estan definidos en el archivo .env")
        return

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://web.whatsapp.com")

        print("Escanea el QR y presiona Enter")
        input()

        # Buscar barra de busqueda
        search_selector = 'div[contenteditable="true"][data-tab="3"]'
        await page.wait_for_selector(search_selector)

        # Llenar el buscador con el nombre
        await page.fill(search_selector, CONTACTO)

        # Esperar a que aparezca el contacto
        await page.wait_for_selector(f"text={CONTACTO}")
        await page.click(f"text={CONTACTO}")

        # Selector del cuadro de mensaje
        msg_selector = 'div[aria-placeholder="Escribe un mensaje"]'
        await page.wait_for_selector(msg_selector)

        # Escribir mensaje
        await page.fill(msg_selector, MENSAJE)

        # Enviar
        await page.keyboard.press("Enter")

        print("Mensaje enviado correctamente")

        await page.wait_for_timeout(1500)
        await browser.close()

asyncio.run(main())
