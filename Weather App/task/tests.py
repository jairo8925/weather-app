import asyncio

from hstest import FlaskTest, CheckResult, WrongAnswer
from hstest import dynamic_test
from hstest.dynamic.security.exit_handler import ExitHandler
from pyppeteer import launch


class FlaskProjectTest(FlaskTest):
    source = 'web.app'
    run_args = {
        "headless": False,
        "defaultViewport": None,
        "args": ['--start-maximized', '--disable-infobar'],
        "ignoreDefaultArgs": ['--enable-automation'],
    }

    async def launch_and_get_browser(self):
        try:
            return await launch(self.run_args)
        except Exception as error:
            raise WrongAnswer(str(error))

    async def close_browser(self, browser):
        try:
            await browser.close()
        except Exception as ex:
            print(ex)
            pass

    async def test_main_page_structure(self):
        browser = await self.launch_and_get_browser()
        page = await browser.newPage()

        await page.goto(self.get_url())
        html_code = await page.content()

        if "Hello, world!" not in html_code:
            raise WrongAnswer("'/' route should return 'Hello, world!' message!")

        await self.close_browser(browser)

    @dynamic_test()
    def test(self):
        ExitHandler.revert_exit()
        asyncio.get_event_loop().run_until_complete(self.test_main_page_structure())
        return CheckResult.correct()


if __name__ == '__main__':
    FlaskProjectTest().run_tests()
