from selenium import webdriver
from selenium.webdriver.common.by import By
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import textwrap
import time
import os


def save_text_to_pdf(text, output_filename):
    """
    Save the extracted text to a PDF file with proper formatting
    """
    c = canvas.Canvas(output_filename, pagesize=letter)
    width, height = letter
    margin = 72  # 1 inch margin
    y = height - margin

    # Set font and size
    c.setFont("Helvetica", 11)

    # Split text into lines that fit within margins
    wrapped_text = textwrap.fill(text, width=80)
    lines = wrapped_text.split('\n')

    for line in lines:
        # If we're near the bottom of the page, start a new page
        if y < margin:
            c.showPage()
            y = height - margin
            c.setFont("Helvetica", 11)

        # Write the line
        c.drawString(margin, y, line)
        y -= 15  # Move down for next line

    c.save()


def scrape_and_save_to_pdf(url,output_directory, output_filename):
    """
    Scrape website content and save to PDF
    """
    try:

        # Create full output path
        output_path = os.path.join(output_directory, output_filename)

        # Set up the WebDriver
        driver = webdriver.Chrome()

        # Open the webpage
        driver.get(url)
        time.sleep(5)  # Wait for page to load

        # Get all elements on the page
        elements = driver.find_element(By.TAG_NAME, "main")
        ele = elements.find_elements(By.XPATH, './*')

        # Initialize an empty list to store the meaningful text
        text_list = []

        # Iterate through each element and extract text
        for element in ele:
            # Skip elements that usually contain non-informative text
            if element.tag_name not in ["a", "button", "script", "style",
                                        "meta", "link", "header", "footer", "nav"]:
                text = element.text.strip()
                if text:  # Only add non-empty text
                    text_list.append(text)

        # Join all the collected text into a single string
        page_text = "\n".join(text_list)
        # print(page_text)

        # Save to PDF
        save_text_to_pdf(page_text, output_path)

        print(f"Successfully saved content to {output_path}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        # Always close the browser
        driver.quit()


if __name__ == "__main__":
    url = "https://investors.nov.com/company-overview"
    output_filename = f"nov_{url.split("/")[-1]}_page.pdf"
    output_directory = "../data/other"
    scrape_and_save_to_pdf(url, output_directory ,output_filename)