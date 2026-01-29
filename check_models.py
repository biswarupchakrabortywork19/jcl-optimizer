import google.generativeai as genai

# PASTE YOUR API KEY HERE (between the quotes)
API_KEY = "AIzaSyCkD-5UXz_C0Qu_v_qyXdVgVR66eZxBYXE"  # Replace with your actual key

genai.configure(api_key=API_KEY)

print("🔍 Checking available Gemini models...\n")

try:
    models = genai.list_models()
    print("✅ Available models that support generateContent:\n")
    
    for model in models:
        if 'generateContent' in model.supported_generation_methods:
            print(f"✓ {model.name}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\n⚠️ Check if your API key is correct!")