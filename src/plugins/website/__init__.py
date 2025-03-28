from ..base_plugin import BasePlugin
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
import io

class Website(BasePlugin):
    def __init__(self, config=None):
        super().__init__(config)
        self.url = config.get('url', 'https://example.com')
        self.width = config.get('width', 800)
        self.height = config.get('height', 600)

    def get_config_options(self):
        return {
            'url': {
                'type': 'string',
                'label': 'Website URL',
                'default': 'https://example.com'
            },
            'width': {
                'type': 'number',
                'label': 'Width',
                'default': 800
            },
            'height': {
                'type': 'number',
                'label': 'Height',
                'default': 600
            }
        }

    def render(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument(f'--window-size={self.width},{self.height}')
        
        driver = webdriver.Chrome(options=options)
        try:
            driver.get(self.url)
            # Wait for page to load
            driver.implicitly_wait(5)
            
            # Take screenshot
            screenshot = driver.get_screenshot_as_png()
            image = Image.open(io.BytesIO(screenshot))
            
            return image
        finally:
            driver.quit()

    def get_update_interval(self):
        # Update every hour by default
        return 3600 