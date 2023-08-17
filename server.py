from flask import Flask, jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route("/trends", methods=["GET"])
def get_trends():
    pinterest_links = get_pinterest_trends()
    flipkart_links = get_flipkart_trends()
    combined_links = pinterest_links + flipkart_links
    return jsonify(combined_links)

def get_pinterest_trends():
    # Fetch trends from Pinterest and extract image links
    pinterest_url = "https://www.pinterest.com/search/pins/?q=fashion%20trends"
    response = requests.get(pinterest_url)
    soup = BeautifulSoup(response.text, "html.parser")
    image_elements = soup.find_all("img")
    image_links = [img.get("src") for img in image_elements]
    if not image_links:
        print("no in pinterst")
    return image_links

def get_flipkart_trends():
    # Fetch trends from Flipkart and extract image links
    flipkart_url = "https://www.flipkart.com/clothing-and-accessories/fashion-trends~brand/pr?sid=clo"
    response = requests.get(flipkart_url)
    soup = BeautifulSoup(response.text, "html.parser")
    image_elements = soup.find_all("img")
    image_links = [img.get("src") for img in image_elements if img.get("src").startswith("https://") and img.get("src").endswith(".jpeg?q=90")]
    return image_links

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=3001)
