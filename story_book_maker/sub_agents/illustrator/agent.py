from google.adk.models.lite_llm import LiteLlm
from google.adk.agents import Agent
from .prompt import ILLUSTRATOR_DESCRIPTION, ILLUSTRATOR_PROMPT
from .tools import generate_and_save_images

MODEL = LiteLlm(model="openai/gpt-4o-mini")

illustrator_agent = Agent(
    name="IllustratorAgent",
    model=MODEL,
    description=ILLUSTRATOR_DESCRIPTION,
    instruction=ILLUSTRATOR_PROMPT,
    tools=[generate_and_save_images],  # Attach the batch tool
)


# # 1. Define the Tool (The Paintbrush)
# # Ensure an assets directory exists
# MASTER_DIR = Path(__file__).resolve().parent.parent.parent

# # Define the exact path: my_project/assets/illustrations/
# ASSETS_DIR = MASTER_DIR / "assets" / "illustrations"
# ASSETS_DIR.mkdir(parents=True, exist_ok=True)


# def generate_and_save_image_tool(visual_description: str) -> str:
#     """
#     Generates an image via DALL-E 3, downloads it, and saves it locally.
#     Returns the local file path.
#     """
#     # print(f"[DEBUG] Generating image for: {visual_description}")
#     try:
#         # 1. Generate the image (Cloud)
#         response = litellm.image_generation(prompt=visual_description, model="dall-e-3")
#         temporary_url = response.data[0].url

#         # 2. Download the image stream
#         img_data = requests.get(temporary_url).content

#         # 3. Create a unique filename and save it (Local)
#         filename = f"page_img_{uuid.uuid4().hex[:8]}.png"
#         local_path = os.path.join(ASSETS_DIR, filename)

#         with open(local_path, "wb") as handler:
#             handler.write(img_data)

#         print(f"[DEBUG] Image successfully saved to {local_path}")

#         # Return the local path so the Master Agent state is permanent
#         return local_path

#     except Exception as e:
#         return f"Error generating or saving image: {str(e)}"
