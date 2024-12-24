import streamlit as st
from bs4 import BeautifulSoup
import json
import os
import requests
# Load API secrets
from dotenv import load_dotenv
load_dotenv()
CLOUDFLARE_ACCOUNT_ID = 'bf167460d09308a3f294727186c2c8b5'
CLOUDFLARE_API_TOKEN = '--aXd8RnXPWjGLpIoAm370QRWtsVHUpzI7pD_8nc'
url = f'https://api.cloudflare.com/client/v4/accounts/{CLOUDFLARE_ACCOUNT_ID}/ai/run/@cf/mistral/mistral-7b-instruct-v0.1'

def main():
    st.markdown("""
        <style>
            .big-font {
                font-size:40px !important;
                color:green;
            }
        </style>
    """, unsafe_allow_html=True)
    st.markdown('<p class="big-font"<p>AI🤖 News🗞️ Summarizer</p>', unsafe_allow_html=True)
    st.write(":blue[This Python🐍 web🕸️ app is built👩🏻‍💻 w/ [Streamlit](https://streamlit.io/) && [Cloudflare Workers AI](https://ai.cloudflare.com/)]")

    news_link = st.text_input('Please enter a news link to summarize') # news_link = "https://www.npr.org/2024/07/08/g-s1-8731/emma-navarro-coco-gauff-wimbeldon"
    tone = st.selectbox(
        ':green[What tone do you want the news summary to take?]',
        ('humorous🤣', 'majestic🌊', 'academic📚', '✨inspirational✨', 'dramatic🎭', 'gen z👧🏻')
    )
    st.write("You selected: ", tone)
    if st.button('Enter') and tone is not None and news_link is not None:
        with st.spinner('Processing📈...'):
            resp1 = requests.get(news_link)
            soup = BeautifulSoup(resp1.text, 'html.parser')

            # Extract text data from website
            text_data = ''
            for tag in soup.find_all(['p']):
                text_data += tag.get_text()

            print('text_data' , text_data)

            # Define the headers
            headers = {
                'Authorization': f'Bearer {CLOUDFLARE_API_TOKEN}',
                'Content-Type': 'application/json'
            }

            # Define the data
            data = {
                "messages": [
                    {
                        "role": "user",
                        "content": f"Summarize the following content from a news article in a {tone} tone: {text_data}"
                    }
                ],
                "lora": "cf-public-cnn-summarization"
            }

            # Make the POST request
            response = requests.post(url, headers=headers, data=json.dumps(data))

            # Parse the response
            response_data = response.json()
            summary = response_data["result"]["response"]
            print("summary ", summary)
        html_str = f"""
        <p style="font-family:Comic Sans; color:Pink; font-size: 18px;">{summary}</p>
        """
        st.markdown(html_str, unsafe_allow_html=True)

    st.write("Made w/ ❤️ in SF 🌁 || ✅ out the [👩🏻‍💻GitHub repo](https://github.com/elizabethsiegle/cf-ai-lora-news-summarizer)")

if __name__ == "__main__":
    main()
