import streamlit as st
from google import genai

# Page Setup
st.set_page_config(page_title="AI Script & Content Generator", page_icon="⚡")
st.title("⚡ AI Script & Content Generator")
st.caption("Generate high-quality video scripts, blogs, and posts in seconds.")

# User Inputs
api_key = st.text_input("Enter Gemini API Key:", type="password")
topic = st.text_input("Enter Topic / Concept:", placeholder="e.g., Blood clotting mechanism, Mystery story")
content_type = st.selectbox(
    "Choose Format:",
    ["YouTube Video Script", "Instagram/Facebook Post", "Study Summary", "Step-by-step Guide"]
)

# Generation Logic
if st.button("Generate Now"):
    if not api_key:
        st.warning("Please provide your Gemini API key.")
    elif not topic:
        st.warning("Please enter a topic.")
    else:
        with st.spinner("AI is crafting your content..."):
            try:
                client = genai.Client(api_key=api_key)
                prompt = (
                    f"You are a professional creator. Write an engaging, well-structured {content_type} "
                    f"about the following topic: '{topic}'. Keep the tone clear, informative, and captivating."
                )
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                )
                st.success("Completed!")
                st.markdown("### Output:")
                st.write(response.text)
            except Exception as e:
                st.error(f"Error: {e}")
