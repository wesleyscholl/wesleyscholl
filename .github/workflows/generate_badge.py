import requests
import random
import os

# Get Gemini API key from environment variable
GEMINI_API_KEY = os.environ.get("ENV_SECRET")
print(GEMINI_API_KEY)

# Gemini API endpoint
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GEMINI_API_KEY}" 

# Your color palette
COLOR_PALETTE = [
    "#77C7D9", "#72C0D3", "#6CB8CC", "#60A8BE", "#5499B0", 
    "#4889A2", "#3D7A94", "#316A86", "#255A78", "#194A6A" 
]

# --- Gemini Prompt Engineering ---
def generate_badge_prompt(seed):
    return f"""
    A digital badge with a coding, technology, or software theme. 
    Incorporate elements like code snippets, circuit boards, or abstract shapes.
    Use a color scheme primarily from these hex codes: {COLOR_PALETTE}.
    Ensure a high-resolution and visually appealing design. Send back the url to 
    the newly created image. Seed: {seed} Image size: 256x256
    """

# --- Badge Generation Logic ---
def generate_and_save_badge():
    # Generate a random seed for variation
    seed = random.randint(1, 10000)
    
    prompt = generate_badge_prompt(seed)

    # Prepare Gemini API payload
    payload = {
        "contents":[{"parts":[{"text": prompt}]}],
        "safetySettings": [{"category": "HARM_CATEGORY_DANGEROUS_CONTENT","threshold": "BLOCK_NONE"}],
    	"generationConfig": {
    		"temperature": 0.2,
    		"maxOutputTokens": 50
    	}
    }
    
    # Make API request to Gemini
    response = requests.post(GEMINI_API_URL, json=payload)

    if response.status_code == 200:
        print(response.json())
        image_url = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        print(image_url)

        # Download and save the image
        badge_filename = f"badge_{seed}.png"
        badge_path = os.path.join("badges", badge_filename)

        with open(badge_path, "wb") as f:
            f.write(requests.get(image_url).content)

        return badge_filename
    else:
        print(f"Error generating badge: {response.text}")
        return None

# --- Update README.md ---
def update_readme(badge_filename):
    with open("README.md", "r") as f:
        readme_content = f.read()

    # Find the badges section
    badges_section_start = readme_content.find("## 🎖️ Badges")

    if badges_section_start == -1:
        print("Badges section not found in README.md")
        return

    # Create the new badge markdown
    badge_url = f"https://raw.githubusercontent.com/wesleyscholl/wesleyscholl/main/badges/{badge_filename}"  
    new_badge_markdown = f"![Badge]({badge_url})\n"

    # Insert the new badge markdown after the badges section
    readme_content = (
        readme_content[:badges_section_start]
        + "## Badges\n"
        + new_badge_markdown
        + readme_content[badges_section_start:]
    )

    with open("README.md", "w") as f:
        f.write(readme_content)

if __name__ == "__main__":
    badge_filename = generate_and_save_badge()
    if badge_filename:
        update_readme(badge_filename)
