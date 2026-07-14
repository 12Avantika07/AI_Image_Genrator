import streamlit as st
import requests
from urllib.parse import quote

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Image Generator",
    page_icon="🎨",
    layout="centered"
)

st.title("🎨 MY AI IMAGE GENERATOR")
st.write("Generate AI images using Pollinations AI")

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.header("⚙️ Settings")

art_style = st.sidebar.selectbox(
    "Select Art Style",
    [
        "Photorealistic",
        "Anime",
        "Vintage Victorian",
        "Sketch",
        "3D Render",
        "Cyberpunk",
        "Fantasy",
        "Watercolor",
        "Oil Painting",
        "Pixar Style"
    ]
)

width = st.sidebar.slider(
    "Image Width",
    min_value=256,
    max_value=1024,
    value=768,
    step=64
)

height = st.sidebar.slider(
    "Image Height",
    min_value=256,
    max_value=1024,
    value=768,
    step=64
)

# -----------------------------
# Prompt
# -----------------------------
user_prompt = st.text_area(
    "Describe the image",
    placeholder="Example: A futuristic city at sunset"
)

# -----------------------------
# Generate Button
# -----------------------------
if st.button("🚀 Generate Image"):

    if user_prompt.strip() == "":
        st.warning("Please enter a prompt.")
        st.stop()

    with st.spinner("Generating image..."):

        full_prompt = (
            f"{user_prompt}, "
            f"high quality, {art_style}, "
            f"masterpiece, detailed"
        )

        encoded_prompt = quote(full_prompt)

        url = (
            f"https://image.pollinations.ai/prompt/"
            f"{encoded_prompt}"
            f"?width={width}&height={height}"
        )

        try:
            response = requests.get(url, timeout=90)

            st.write(f"Status Code: {response.status_code}")

            if response.status_code == 200:

                st.success("✅ Image Generated Successfully!")

                st.image(
                    response.content,
                    caption=full_prompt,
                    use_container_width=True
                )

                st.download_button(
                    label="⬇ Download Image",
                    data=response.content,
                    file_name="generated_image.jpg",
                    mime="image/jpeg"
                )

            else:
                st.error(f"API Error: {response.status_code}")
                st.text(response.text)

        except requests.exceptions.Timeout:
            st.error("Request timed out. Please try again.")

        except requests.exceptions.ConnectionError:
            st.error("Unable to connect to Pollinations AI.")

        except Exception as e:
            st.error(f"Error: {e}")