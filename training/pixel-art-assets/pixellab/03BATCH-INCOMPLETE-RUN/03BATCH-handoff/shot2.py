import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width":1240,"height":1400})
        html = open('/mnt/user-data/outputs/convergence/convergence_codex.html').read()
        await pg.set_content('<!doctype html><html><head><meta charset="utf-8"></head><body>'+html+'</body></html>', wait_until='load')
        await pg.wait_for_timeout(4000)
        await pg.screenshot(path='codex_shot.png', full_page=False)
        await b.close()
asyncio.run(main())
