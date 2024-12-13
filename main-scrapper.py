import os
import threading
import json
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.core.window import Window
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time  # To measure inactivity time

# WebDriver config
edge_driver_path = r"C:\Users\pecor\Downloads\edgedriver_win64\msedgedriver.exe"
options = Options()
service = Service(executable_path=edge_driver_path)

# Result and progress file paths
result_file = "film-results.txt"
progress_file = "progress.json"

class ScraperApp(App):
    def build(self):
        Window.size = (800, 600)
        self.title = "Film data Scraper - by pecorio"
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.status_label = Label(text="Click Start to begin scraping...", font_size=22, size_hint=(1, 0.1), color=(1, 1, 1, 1))
        self.layout.add_widget(self.status_label)

        self.progress_bar = ProgressBar(max=960, size_hint=(1, 0.05))
        self.layout.add_widget(self.progress_bar)

        self.log_output = TextInput(size_hint=(1, 0.5), readonly=True, background_color=(0.2, 0.2, 0.2, 1), foreground_color=(1, 1, 1, 1), font_size=14)
        scrollview = ScrollView(size_hint=(1, 0.5))
        scrollview.add_widget(self.log_output)
        self.layout.add_widget(scrollview)

        button_size_hint = (1, 0.1)

        self.start_button = Button(text="Start Scraping", size_hint=button_size_hint, background_color=(0, 0.7, 0, 1), color=(1, 1, 1, 1), font_size=18)
        self.start_button.bind(on_press=self.start_scraping)
        self.layout.add_widget(self.start_button)

        self.stop_button = Button(text="Stop Scraping", size_hint=button_size_hint, background_color=(0.8, 0, 0, 1), color=(1, 1, 1, 1), font_size=18)
        self.stop_button.bind(on_press=self.stop_scraping)
        self.stop_button.disabled = True
        self.layout.add_widget(self.stop_button)

        # Initialize progress values
        self.current_page = 1
        self.current_film = 0

        # Load progress from the JSON file
        self.load_progress()

        return self.layout

    def load_progress(self):
        """Load progress from progress.json file."""
        if os.path.exists(progress_file):
            with open(progress_file, 'r') as file:
                data = json.load(file)
                self.current_page = data.get('current_page', 1)
                self.current_film = data.get('current_film', 0)
                self.update_log(f"Resuming from page {self.current_page} and film {self.current_film}...")
        else:
            self.current_page = 1
            self.current_film = 0

    def save_progress(self):
        """Save progress to progress.json file."""
        progress_data = {
            'current_page': self.current_page,
            'current_film': self.current_film
        }
        with open(progress_file, 'w') as file:
            json.dump(progress_data, file)

    def update_log(self, message):
        """Update the log output in the GUI."""
        self.log_output.text += message + "\n"
        self.log_output.cursor = (len(self.log_output.text), 0)  # Auto scroll to the bottom

    def update_progress(self, value):
        """Update the progress bar."""
        self.progress_bar.value = value

    def start_scraping(self, instance):
        """Start the scraping process in a separate thread."""
        self.stop_button.disabled = False
        self.start_button.disabled = True
        self.status_label.text = "Scraping in progress..."

        # Start a new thread to run the scraper
        self.scraping_thread = threading.Thread(target=self.scrape_films)
        self.scraping_thread.start()

    def stop_scraping(self, instance):
        """Stop the scraping process."""
        self.stop_button.disabled = True
        self.start_button.disabled = False
        self.status_label.text = "Scraping stopped by user."
        self.stop_scraping_flag = True

    def scrape_films(self):
        """Perform the web scraping and update GUI."""
        driver = webdriver.Edge(service=service, options=options)
        base_url = "https://www.cpasmieux.is/filmstreaming/"
        total_pages = 960

        self.stop_scraping_flag = False  # Reset stop flag

        try:
            # Continue from the last page
            for page_num in range(self.current_page, total_pages + 1):
                if self.stop_scraping_flag:
                    break  # Stop if user presses stop

                page_url = f"{base_url}{page_num}/"

                # Update GUI from the thread
                Clock.schedule_once(lambda dt, p=page_num: self.update_log(f"Scraping page: {page_url}"))
                Clock.schedule_once(lambda dt, p=page_num: self.update_progress(p))

                # Wait until page is fully loaded
                driver.get(page_url)
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'mi2-img'))
                )

                film_elements = driver.find_elements(By.CLASS_NAME, 'mi2-img')

                # Start scraping from the last film if resuming
                start_index = self.current_film if page_num == self.current_page else 0

                for film_index in range(start_index, len(film_elements)):
                    if self.stop_scraping_flag:
                        break
                    film_element = film_elements[film_index]

                    # Scrape individual film info, with inactivity handling
                    self.scrape_film_info(driver, film_element)

                    # Add a delay to slow down the scraping process
                    time.sleep(0.5)  # Pause for 0.5 seconds between film scrapes

                # Save progress after each page
                self.current_page = page_num
                self.current_film = len(film_elements)  # Set current film to the last scraped on this page
                self.save_progress()

                # Add a delay to slow down the page transition
                time.sleep(1)  # Pause for 1 second after each page

            Clock.schedule_once(lambda dt: self.update_log("Scraping completed!"))
            Clock.schedule_once(lambda dt: self.update_progress(total_pages))
            Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', "Scraping completed."))

        except Exception as e:
            Clock.schedule_once(lambda dt: self.update_log(f"Error: {str(e)}"))

        finally:
            driver.quit()
            self.save_progress()
            Clock.schedule_once(lambda dt: self.stop_scraping(None))

    def scrape_film_info(self, driver, film_element):
        """Scrape individual film details, with retry if page doesn't change after click."""
        try:
            # Ensure the film's image is present before interacting with it
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, 'img'))
            )
            film_image_element = film_element.find_element(By.TAG_NAME, 'img')
            film_title = film_image_element.get_attribute('alt')
            film_image_url = film_image_element.get_attribute('src')

            # Click to access the film's page
            current_url = driver.current_url
            film_image_element.click()

            # Check for inactivity by monitoring the time difference after click
            start_time = time.time()
            try:
                WebDriverWait(driver, 5).until(EC.url_changes(current_url))
            except:
                # If URL does not change, reload the page and retry if more than 1 second inactive
                inactivity_duration = time.time() - start_time
                if inactivity_duration > 1:
                    self.update_log(f"Page inactive for {inactivity_duration:.2f} seconds after clicking on {film_title}. Reloading...")
                    driver.refresh()  # Reload the page
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'mi2-img'))
                    )
                    # Retry clicking on the same film after reload
                    film_elements_retry = driver.find_elements(By.CLASS_NAME, 'mi2-img')
                    film_image_element_retry = film_elements_retry[self.current_film].find_element(By.TAG_NAME, 'img')
                    film_image_element_retry.click()
                    WebDriverWait(driver, 5).until(EC.url_changes(current_url))

            # Wait for the play button to become clickable
            try:
                play_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[@id='click_me_ser' and @class='material-icons']"))
                )
                play_button.click()

                # Wait for the video iframe to load
                iframe_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, 'videoplay'))
                )
                film_link = iframe_element.get_attribute('src')

                self.save_result(film_title, film_link, film_image_url)
                driver.back()

                # Update film count and save progress
                self.current_film += 1  # Increment to the next film
                self.save_progress()

            except Exception as e:
                self.update_log(f"Error loading film link for {film_title}: {str(e)}")
                driver.back()  # Go back to the film list regardless of the error

        except Exception as e:
            Clock.schedule_once(lambda dt: self.update_log(f"Error scraping film: {str(e)}"))
            driver.back()  # Ensure we go back to the list of films

    def save_result(self, film_title, film_link, film_image_url):
        """Save the scraped film data."""
        with open(result_file, 'a', encoding='utf-8') as file:
            file.write(f"{film_title} ----- {film_link} ----- {film_image_url}\n")

if __name__ == "__main__":
    ScraperApp().run()
