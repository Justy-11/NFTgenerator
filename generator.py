import os
import random
import json
from PIL import Image
from collections import defaultdict

# Configuration
TOTAL_IMAGES = 1000  # Generate 1000 NFTs
OUTPUT_DIR = "output_nfts"
IMAGE_SIZE = (1280, 1280)  # Ensure all images are the same size
LAYERS = ["Background", "Body", "Clothes", "Face", "Hat"]

# Updated Rarity Distribution
RARITY = {
    "Background": {"Olive Green": 5, "Neon Aqua": 5, "Dark Blue": 5, "Gray": 5, "Light Blue": 5, "Purple": 5, "Yellow": 5, "Orange": 5},
    "Body": {"Yellow Ape": 3, "Pink Ape": 4, "Light Gray Ape": 4, "Light Brown Ape": 4, "Leopard Ape": 2, "Gray Ape": 4, "Brown Ape": 4, "Gold Ape": 1, "Black Ape": 4},
    "Clothes": {"Suit": 1, "No Cloth": 4, "Formal Red": 2, "Sailor": 3, "Space": 3, "Summer": 1, "Tank Top White": 4, "Prisoner": 3, "Plain Gray": 4, "Plain Blue": 4, "Graphic Tee Two Mountain": 2, "Army": 2},
    "Face": {"Bubblegum 2": 3, "Bubblegum 1": 3, "Mustache": 3, "Robot Eye": 3, "Beard": 3, "Eye Patch": 3, "Glasses": 3, "Laser Eyes": 1, "Pizza": 1, "Pipe": 2, "Eyes Out": 3, "Cigarette": 2, "Cigar": 2},
    "Hat": {"Party Hat": 2, "Halo": 3, "Crown": 1, "No Hat": 4, "Sailor Hat": 3, "Cowboy Hat": 3, "Captain": 3, "America Helmet": 2}
}

RESTRICTIONS = [
    ("Face", "Bubblegum 1", "Body", "Brown Ape"),  # If Face is Bubblegum 1, Body cannot be these sad Apes
    ("Face", "Bubblegum 1", "Body", "Gold Ape"),   
    ("Face", "Bubblegum 1", "Body", "Light Brown Ape"),
    ("Face", "Bubblegum 1", "Body", "Light Gray Ape"),
    ("Face", "Bubblegum 1", "Body", "Pink Ape"),
    ("Face", "Bubblegum 2", "Body", "Black Ape"),
    ("Face", "Bubblegum 2", "Body", "Gray Ape"),
    ("Face", "Bubblegum 2", "Body", "Leopard Ape"),
    ("Face", "Bubblegum 2", "Body", "Yellow Ape"),
    ("Face", "Eyes Out", "Hat", "Sailor Hat"),
    ("Face", "Eyes Out", "Hat", "Cowboy Hat"),
    ("Face", "Eyes Out", "Hat", "America Helmet"),
    ("Face", "Eyes Out", "Hat", "Captain"),
]

# Define special combinations
SPECIAL_COMBINATIONS = [
    {"Background": "Dark Blue", "Body": "Gold Ape", "Clothes": "Suit", "Face": "Pizza", "Hat": "Crown"},
    {"Background": "Light Blue", "Body": "Leopard Ape", "Clothes": "Summer", "Face": "Pizza", "Hat": "Crown"},
    {"Background": "Purple", "Body": "Yellow Ape", "Clothes": "Suit", "Face": "Pipe", "Hat": "Crown"},
    {"Background": "Yellow", "Body": "Pink Ape", "Clothes": "Summer", "Face": "Laser Eyes", "Hat": "Crown"}
]

# Load available traits
traits = {}
for layer in LAYERS:
    traits[layer] = {trait: count for trait, count in RARITY[layer].items()}

def is_valid_combination(selected_traits):
    for rule in RESTRICTIONS:
        layer1, trait1, layer2, trait2 = rule
        if selected_traits.get(layer1) == trait1 and selected_traits.get(layer2) == trait2:
            return False
    return True

def generate_unique_combinations():
    generated = SPECIAL_COMBINATIONS.copy()  # Start with special combinations
    while len(generated) < TOTAL_IMAGES:
        selected_traits = {}
        for layer in LAYERS:
            available_traits = list(traits[layer].keys())
            selected_trait = random.choices(available_traits, weights=[traits[layer][t] for t in available_traits])[0]
            selected_traits[layer] = selected_trait
        
        if is_valid_combination(selected_traits) and selected_traits not in generated:
            generated.append(selected_traits)
    return generated

def create_images(combinations):
    # Create directories for images and metadata
    image_dir = os.path.join(OUTPUT_DIR, "images")
    metadata_dir = os.path.join(OUTPUT_DIR, "metadata")
    os.makedirs(image_dir, exist_ok=True)
    os.makedirs(metadata_dir, exist_ok=True)
    
    for i, traits in enumerate(combinations):
        base_image = None
        for layer in LAYERS:
            trait_file = f"layers/{layer}/{traits[layer]}.png"
            if os.path.exists(trait_file):
                layer_img = Image.open(trait_file).convert("RGBA").resize(IMAGE_SIZE)
                if base_image is None:
                    base_image = layer_img
                else:
                    base_image = Image.alpha_composite(base_image, layer_img)
        
        if base_image:
            # Save the image
            image_path = os.path.join(image_dir, f"{i}.png")
            base_image.save(image_path)
            
            # Create metadata
            metadata = {
                "name": f"NFT #{i}",
                "description": "A unique NFT from the collection.",
                "image": f"images/{i}.png",  # Relative path to the image
                "attributes": [{"trait_type": key, "value": value} for key, value in traits.items()]
            }
            # Save metadata
            metadata_path = os.path.join(metadata_dir, f"{i}.json")
            with open(metadata_path, "w") as f:
                json.dump(metadata, f, indent=4)

def analyze_trait_distribution(combinations):
    trait_counts = defaultdict(lambda: defaultdict(int))
    
    # Count occurrences of each trait
    for traits in combinations:
        for layer, trait in traits.items():
            trait_counts[layer][trait] += 1
    
    # Display the results
    print("\nTrait Distribution:")
    for layer, counts in trait_counts.items():
        print(f"\n{layer}:")
        for trait, count in sorted(counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {trait}: {count}")

# Generate and create NFT images
combinations = generate_unique_combinations()
create_images(combinations)
analyze_trait_distribution(combinations)
print(f"\nGenerated {TOTAL_IMAGES} NFT images and metadata files!")

# import os
# import random
# import json
# from PIL import Image

# # Configuration
# TOTAL_IMAGES = 1000  # Generate 1000 NFTs
# OUTPUT_DIR = "output_nfts"
# IMAGE_SIZE = (1280, 1280)  # Ensure all images are the same size
# LAYERS = ["Background", "Body", "Clothes", "Face", "Hat"]

# # Updated Rarity Distribution
# RARITY = {
#     "Background": {"Olive Green": 5, "Neon Aqua": 5, "Dark Blue": 5, "Gray": 5, "Light Blue": 5, "Purple": 5, "Yellow": 5, "Orange": 5},
#     "Body": {"Yellow Ape": 3, "Pink Ape": 4, "Light Grey Ape": 4, "Light Brown Ape": 4, "Leopard Ape": 2, "Gray Ape": 4, "Brown Ape": 4, "Gold Ape": 1, "Black Ape": 4},
#     "Clothes": {"Suit": 1, "No Cloth": 4, "Formal Red": 2, "Sailor": 3, "Space": 3, "Summer": 1, "Tank Top White": 4, "Prisoner": 3, "Plain Gray": 4, "Plain Blue": 4, "Graphic Tee Two Mountain": 2, "Army": 2},
#     "Face": {"Bubblegum 2": 3, "Bubblegum 1": 3, "Mustache": 3, "Robot Eye": 3, "Beard": 3, "Eye Patch": 3, "Glasses": 3, "Laser Eyes": 1, "Pizza": 1, "Pipe": 1, "Eyes Out": 3, "Cigarette": 2, "Cigar": 2},
#     "Hat": {"Party Hat": 1, "Halo": 2, "Crown": 1, "No Hat": 4, "Sailor Hat": 3, "Cowboy Hat": 3, "Captain": 3, "America Helmet": 2}
# }

# RESTRICTIONS = [
#     ("Face", "Bubblegum 1", "Body", "Brown Ape"),  # If Face is Bubblegum 1, Body cannot be these sad Apes
#     ("Face", "Bubblegum 1", "Body", "Gold Ape"),   
#     ("Face", "Bubblegum 1", "Body", "Light Brown Ape"),
#     ("Face", "Bubblegum 1", "Body", "Light Grey Ape"),
#     ("Face", "Bubblegum 1", "Body", "Pink Ape"),
#     ("Face", "Bubblegum 2", "Body", "Black Ape"),
#     ("Face", "Bubblegum 2", "Body", "Gray Ape"),
#     ("Face", "Bubblegum 2", "Body", "Leopard Ape"),
#     ("Face", "Bubblegum 2", "Body", "Yellow Ape"),
    # ("Face", "Eyes Out", "Hat", "Sailor Hat"),
    # ("Face", "Eyes Out", "Hat", "Cowboy Hat"),
    # ("Face", "Eyes Out", "Hat", "America Helmet"),
    # ("Face", "Eyes Out", "Hat", "Captain"),
# ]

# # Define special combinations
# SPECIAL_COMBINATIONS = [
#     {"Background": "Dark Blue", "Body": "Gold Ape", "Clothes": "Suit", "Face": "Pizza", "Hat": "Crown"},
#     {"Background": "Light Blue", "Body": "Leopard Ape", "Clothes": "Summer", "Face": "Pizza", "Hat": "Crown"},
#     {"Background": "Purple", "Body": "Yellow Ape", "Clothes": "Suit", "Face": "Pipe", "Hat": "Crown"},
#     {"Background": "Yellow", "Body": "Pink Ape", "Clothes": "Summer", "Face": "Laser Eyes", "Hat": "Crown"}
# ]

# # Load available traits
# traits = {}
# for layer in LAYERS:
#     traits[layer] = {trait: count for trait, count in RARITY[layer].items()}

# def is_valid_combination(selected_traits):
#     for rule in RESTRICTIONS:
#         layer1, trait1, layer2, trait2 = rule
#         if selected_traits.get(layer1) == trait1 and selected_traits.get(layer2) == trait2:
#             return False
#     return True

# def generate_unique_combinations():
#     generated = SPECIAL_COMBINATIONS.copy()  # Start with special combinations
#     while len(generated) < TOTAL_IMAGES:
#         selected_traits = {}
#         for layer in LAYERS:
#             available_traits = list(traits[layer].keys())
#             selected_trait = random.choices(available_traits, weights=[traits[layer][t] for t in available_traits])[0]
#             selected_traits[layer] = selected_trait
        
#         if is_valid_combination(selected_traits) and selected_traits not in generated:
#             generated.append(selected_traits)
#     return generated

# def create_images(combinations):
#     # Create directories for images and metadata
#     image_dir = os.path.join(OUTPUT_DIR, "images")
#     metadata_dir = os.path.join(OUTPUT_DIR, "metadata")
#     os.makedirs(image_dir, exist_ok=True)
#     os.makedirs(metadata_dir, exist_ok=True)
    
#     for i, traits in enumerate(combinations):
#         base_image = None
#         for layer in LAYERS:
#             trait_file = f"layers/{layer}/{traits[layer]}.png"
#             if os.path.exists(trait_file):
#                 layer_img = Image.open(trait_file).convert("RGBA").resize(IMAGE_SIZE)
#                 if base_image is None:
#                     base_image = layer_img
#                 else:
#                     base_image = Image.alpha_composite(base_image, layer_img)
        
#         if base_image:
#             # Save the image
#             image_path = os.path.join(image_dir, f"{i}.png")
#             base_image.save(image_path)
            
#             # Create metadata
#             metadata = {
#                 "name": f"NFT #{i}",
#                 "description": "A unique NFT from the collection.",
#                 "image": f"images/{i}.png",  # Relative path to the image
#                 "attributes": [{"trait_type": key, "value": value} for key, value in traits.items()]
#             }
#             # Save metadata
#             metadata_path = os.path.join(metadata_dir, f"{i}.json")
#             with open(metadata_path, "w") as f:
#                 json.dump(metadata, f, indent=4)

# # Generate and create NFT images
# combinations = generate_unique_combinations()
# create_images(combinations)
# print(f"Generated {TOTAL_IMAGES} NFT images and metadata files!")

# import os
# import random
# import json
# from PIL import Image

# # Configuration
# TOTAL_IMAGES = 100  # Adjusted for sample generation
# OUTPUT_DIR = "output_nfts"
# IMAGE_SIZE = (1280, 1280)  # Ensure all images are the same size
# LAYERS = ["Background", "Body", "Clothes", "Face", "Hat"]
# RARITY = {
#     "Background": {"Olive Green": 4, "Neon Aqua": 4, "Dark Blue": 4, "Gray": 3, "Light Blue": 3, "Purple": 2, "Yellow": 2, "Orange": 3},
#     "Body": {"Yellow Ape": 3, "Pink Ape": 3, "Light Grey Ape": 3, "Light Brown Ape": 3, "Leopard Ape": 3, "Gray Ape": 3, "Brown Ape": 2, "Gold Ape": 2, "Black Ape": 3},
#     "Clothes": {"Suit": 2, "No Cloth": 2, "Formal Red": 2, "Sailor": 2, "Space": 2, "Summer": 2, "Tank Top White": 2, "Prisoner": 2, "Plain Gray": 2, "Plain Blue": 2, "Graphic Tee Two Mountain": 2, "Army": 3},
#     "Face": {"Bubblegum 2": 2, "Bubblegum 1": 2, "Mustache": 2, "Robot Eye": 2, "Beard": 2, "Eye Patch": 2, "Glasses": 2, "Laser Eyes": 2, "Pizza": 2, "Pipe": 2, "Eyes Out": 2, "Cigarette": 2, "Cigar": 2},
#     "Hat": {"Party Hat": 3, "Halo": 3, "Crown": 3, "No Hat": 3, "Sailor Hat": 3, "Cowboy Hat": 3, "Captain": 3, "America Helmet": 4}
# }

# RESTRICTIONS = [
#     ("Face", "Bubblegum 1", "Body", "Brown Ape"),  # If Face is Bubblegum 1, Body cannot be these sad Apes
#     ("Face", "Bubblegum 1", "Body", "Gold Ape"),   
#     ("Face", "Bubblegum 1", "Body", "Light Brown Ape"),
#     ("Face", "Bubblegum 1", "Body", "Light Grey Ape"),
#     ("Face", "Bubblegum 1", "Body", "Pink Ape"),
#     ("Face", "Bubblegum 2", "Body", "Black Ape"),
#     ("Face", "Bubblegum 2", "Body", "Gray Ape"),
#     ("Face", "Bubblegum 2", "Body", "Leopard Ape"),
#     ("Face", "Bubblegum 2", "Body", "Yellow Ape"),
# ]

# # Load available traits
# traits = {}
# for layer in LAYERS:
#     traits[layer] = {trait: count for trait, count in RARITY[layer].items()}

# def is_valid_combination(selected_traits):
#     for rule in RESTRICTIONS:
#         layer1, trait1, layer2, trait2 = rule
#         if selected_traits.get(layer1) == trait1 and selected_traits.get(layer2) == trait2:
#             return False
#     return True

# def generate_unique_combinations():
#     generated = []
#     while len(generated) < TOTAL_IMAGES:
#         selected_traits = {}
#         for layer in LAYERS:
#             available_traits = list(traits[layer].keys())
#             selected_trait = random.choices(available_traits, weights=[traits[layer][t] for t in available_traits])[0]
#             selected_traits[layer] = selected_trait
        
#         if is_valid_combination(selected_traits) and selected_traits not in generated:
#             generated.append(selected_traits)
#     return generated

# def create_images(combinations):
#     if not os.path.exists(OUTPUT_DIR):
#         os.makedirs(OUTPUT_DIR)
    
#     for i, traits in enumerate(combinations):
#         base_image = None
#         for layer in LAYERS:
#             trait_file = f"layers/{layer}/{traits[layer]}.png"
#             if os.path.exists(trait_file):
#                 layer_img = Image.open(trait_file).convert("RGBA").resize(IMAGE_SIZE)
#                 if base_image is None:
#                     base_image = layer_img
#                 else:
#                     base_image = Image.alpha_composite(base_image, layer_img)
        
#         if base_image:
#             image_path = f"{OUTPUT_DIR}/{i}.png"
#             base_image.save(image_path)
#             metadata = {
#                 "name": f"NFT #{i}",
#                 "description": "A unique NFT from the collection.",
#                 "image": image_path,  # Replace with IPFS or hosting URL after upload
#                 "attributes": [{"trait_type": key, "value": value} for key, value in traits.items()]
#             }
#             with open(f"{OUTPUT_DIR}/{i}.json", "w") as f:
#                 json.dump(metadata, f, indent=4)

# # Generate and create NFT images
# combinations = generate_unique_combinations()
# create_images(combinations)
# print(f"Generated {TOTAL_IMAGES} NFT images with metadata compatible with OpenSea!")
