from playwright.async_api import async_playwright
import argparse, random, asyncio
"""
    Primeiras versões de códigos futuros, esse aqui é pra entender o que é necessário para trabalhar com certa visão 
                                        utilizando automação de Browsers
"""


class initialize:
    def __init__(self):
        self.arguments = self._getArguments()

    def _getArguments(self):
        arguments = argparse.ArgumentParser()
        scrap_informations = arguments.add_argument("-i", "--informations", nargs="+", required=False)
        return arguments.parse_args()

    def run(self):
        data = asyncio.run(scrapper().Process())

class scrapper:
    def __init__(self):
        self.results = None
        self.selector_for_first_open = "div[class='column areatemplate-esquerda large-15 large-offset-0 xlarge-14 xlarge-offset-1 float-left']"
        self.bs4_scrap_is_running =  True
        self.website_pointers = [
            "img[class='bstn-fd-picture-image']",
            "p[elementtiming='text-csr']",
            "div[class='column medium-20 medium-offset-2 medium-pull-2 large-8 large-offset-0 large-pull-0 xlarge-7 xlarge-offset-1 xlarge-pull-1 float-right areatemplate-direita']"
        ]
        self.mouse_last_position = (0, 0)

    async def Process(self):
        async with async_playwright() as p:
            browser = await p.firefox.launch(headless=False)
            self.g1_page = await browser.new_page()
            await self.g1_page.goto("https://g1.globo.com/mundo/")
            await self.g1_page.wait_for_selector(self.selector_for_first_open)
            await self.g1_page.wait_for_timeout(3000)
            for x in range(10):
                await self.g1_page.mouse.wheel(0, 2000)
                await self.g1_page.wait_for_timeout(random.randint(150, 400))

            task1 = asyncio.create_task(self.humanEmulation())
            await asyncio.gather(task1)

    async def move_mouse_with_imperfections(self, start_x, start_y, end_x, end_y, steps=20):
        for step in range(steps):
            progress = step / float(steps - 1)
            
            target_x = start_x + (end_x - start_x) * progress
            target_y = start_y + (end_y - start_y) * progress
            
            jitter_x = random.randint(-5, 5)
            jitter_y = random.randint(-5, 5)
            
            move_x = target_x + jitter_x
            move_y = target_y + jitter_y
            
            await self.g1_page.mouse.move(move_x, move_y, steps=1)
            await asyncio.sleep(random.uniform(0.01, 0.05))

    async def humanEmulation(self):
        await self.g1_page.mouse.move(self.mouse_last_position[0], self.mouse_last_position[1])

        while self.bs4_scrap_is_running:
            await asyncio.sleep(random.randint(2, 5))

            action = random.choice(("up", "stop", "down"))
            mouse_action = random.choice(("selector", "random")) 
            mouse_selector = random.choice(self.website_pointers)
            mouse_random_move = (random.randint(232, 722), random.randint(232, 722))

            print(action, mouse_action, mouse_selector, mouse_random_move)

            if action == "up":
                for x in range(random.randint(15, 25)):
                    await self.g1_page.mouse.wheel(0, -x)
                    await asyncio.sleep(random.uniform(0.03, 0.07))

            if action == "down":
                for x in range(random.randint(15, 25)):
                    await self.g1_page.mouse.wheel(0, x)
                    await asyncio.sleep(random.uniform(0.03, 0.07))

            if mouse_action == "selector":
                border_box = await self.g1_page.query_selector(mouse_selector)
                if border_box:
                    box = await border_box.bounding_box()
                    if box:
                        await self.move_mouse_with_imperfections(self.mouse_last_position[0], self.mouse_last_position[1], box['x'], box['y'], steps=64)
                        self.mouse_last_position = (box['x'], box['y'])

            elif mouse_action == "random":
                await self.move_mouse_with_imperfections(self.mouse_last_position[0], self.mouse_last_position[1], mouse_random_move[0], mouse_random_move[1], steps=64)
                self.mouse_last_position = mouse_random_move  



initialize().run()
