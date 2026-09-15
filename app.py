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
    clean_key = api_key.strip() if api_key else ""
    if not clean_key:
        st.warning("Please provide your Gemini API key.")
    elif not topic:
        st.warning("Please enter a topic.")
    else:
        with st.spinner("AI is finding the active model and crafting your content..."):
            try:
                client = genai.Client(api_key=clean_key)
                
                # Auto-detect available models for this key
                available_models = []
                try:
                    for m in client.models.list():
                        name = m.name or ""
                        actions = getattr(m, "supported_actions", None) or getattr(m, "supported_generation_methods", None)
                        if actions is None or "generateContent" in actions:
                            available_models.append(name.replace("models/", ""))
                except Exception:
                    pass

                # Select the best flash model or first available
                selected_model = None
                for name in available_models:
                    if "flash" in name.lower():
                        selected_model = name
                        break
                
                if not selected_model and available_models:
                    selected_model = available_models[0]
                
                # Default fallback
                if not selected_model:
                    selected_model = "gemini-2.5-flash"

                prompt = (
                    f"You are a professional creator. Write an engaging, well-structured {content_type} "
                    f"about the following topic: '{topic}'. Keep the tone clear, informative, and captivating."
                )
                
                response = client.models.generate_content(
                    model=selected_model,
                    contents=prompt,
                )
                st.success(f"Completed using model: {selected_model}")
                st.markdown("### Output:")
                st.write(response.text)
            except Exception as e:
                st.error(f"Error: {e}")
                
