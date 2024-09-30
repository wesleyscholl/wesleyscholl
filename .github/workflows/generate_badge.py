import requests
import random
import os
import io

# Get the HF Inference API token from the environment
API_TOKEN = os.environ.get("ENV_SECRET")

API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

# Your color palette
COLOR_PALETTE = [
    "#77C7D9", "#72C0D3", "#6CB8CC", "#60A8BE", "#5499B0", 
    "#4889A2", "#3D7A94", "#316A86", "#255A78", "#194A6A" 
]

# --- Gemini Prompt Engineering ---
def generate_badge_prompt(seed):
    return f"""
    A digital badge with a coding, technology, or software theme. 
    Incorporate elements like code snippets, circuit boards, computers, servers, cloud, database, keyboards, code syntax, abstract shapes.
    Use a color scheme primarily from these hex codes: {COLOR_PALETTE}. Don't include any text in the badge and ensure the background of the image is transparent.
    Ensure a high quality and visually appealing design. Seed: {seed} Image size: 256x256
    """

# --- Badge Generation Logic ---
def generate_and_save_badge():
    # Generate a random seed for variation
    seed = random.randint(1, 10000)
    
    prompt = generate_badge_prompt(seed)
    
    # Make API request to HF Inference API
    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.content

    # Call the API to generate the badge
    res = query({
        "inputs": prompt,
    })

    # Await the response
    if res:
        print(res)
        # Save the image - create new file and write the image to a file
        badge_filename = f"badge_{seed}.png"
        with open(f"badges/{badge_filename}", "wb") as f:
            f.write(res)

        print(f"Badge saved as {badge_filename}")
        return badge_filename
    else:
        print(f"Error generating badge: {res.text}")
        return None

# --- Update README.md ---
def update_readme(badge_filename):
    with open("README.md", "r") as f:
        readme_content = f.read()

    # Find the badges section
    badges_section_start = readme_content.find('<div id="badges" class="flex-container" align=center>')

    if badges_section_start == -1:
        print("Badges section not found in README.md")
        return

    # Create the new badge markdown
    badge_url = f"https://raw.githubusercontent.com/wesleyscholl/wesleyscholl/main/badges/{badge_filename}"  
    new_badge_markdown = f'<img src="{badge_url}" height="150" />\n'

    # Find the position to insert the new badge markdown
    insert_position = readme_content.find("</div>", badges_section_start)
    if insert_position == -1:
        print("Insert position not found in README.md")
        return

    # Insert the new badge markdown after the insert position
    readme_content = (
        readme_content[:insert_position]
        + new_badge_markdown
        + readme_content[insert_position:]
    )

    print("Updating README.md with new badge")
    print(readme_content)

    with open("README.md", "w") as f:
        f.write(readme_content)

# --- Main --- 
if __name__ == "__main__":
    badge_filename = generate_and_save_badge()
    if badge_filename:
        update_readme(badge_filename)
