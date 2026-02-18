from PIL import Image, ImageDraw
import os
import random

def draw_landscape(season, frame_index, width=256, height=128):
    # Palette definitions
    palettes = {
        "spring": {"sky": (135, 206, 235), "ground": (34, 139, 34), "tree_trunk": (139, 69, 19), "tree_leaf": (255, 183, 197), "mountain": (169, 169, 169)},
        "summer": {"sky": (0, 191, 255), "ground": (50, 205, 50), "tree_trunk": (139, 69, 19), "tree_leaf": (0, 128, 0), "mountain": (105, 105, 105)},
        "autumn": {"sky": (119, 136, 153), "ground": (205, 133, 63), "tree_trunk": (101, 67, 33), "tree_leaf": (210, 105, 30), "mountain": (47, 79, 79)},
        "winter": {"sky": (176, 196, 222), "ground": (240, 248, 255), "tree_trunk": (47, 53, 59), "tree_leaf": (255, 250, 250), "mountain": (112, 128, 144)}
    }
    
    colors = palettes[season]
    img = Image.new("RGBA", (width, height), colors["sky"] + (255,))
    draw = ImageDraw.Draw(img)
    
    # 1. Mountains (Background)
    # Simple triangular mountains
    draw.polygon([(0, height), (50, 40), (120, height)], fill=colors["mountain"] + (255,))
    draw.polygon([(80, height), (160, 30), (240, height)], fill=colors["mountain"] + (255,))
    draw.polygon([(180, height), (256, 50), (320, height)], fill=colors["mountain"] + (255,))

    # 2. Ground
    draw.rectangle([0, height - 30, width, height], fill=colors["ground"] + (255,))
    
    # 3. Trees
    # Draw a few trees specific to season
    def draw_tree(x, y, scale=1.0):
        # Trunk
        tw, th = 8 * scale, 24 * scale
        draw.rectangle([x, y - th, x + tw, y], fill=colors["tree_trunk"] + (255,))
        # Foliage (Circle clusters)
        fw = 24 * scale
        fh = 24 * scale
        leaf_color = colors["tree_leaf"] + (255,)
        draw.ellipse([x - fw/2 + tw/2, y - th - fh + 5, x + fw/2 + tw/2 + fw, y - th + 5], fill=leaf_color)
        draw.ellipse([x - fw/2 + tw/2 - 5, y - th - fh + 15, x + fw/2 + tw/2 + fw - 5, y - th + 15], fill=leaf_color)
        
    random.seed(42) # Consistent trees
    for i in range(5):
        x = 20 + i * 50
        y = height - 25 + random.randint(-5, 5)
        draw_tree(x, y, scale=0.8 + random.random()*0.4)
        
    # 4. Weather Effects
    if season == "spring": # Petals
        for _ in range(30):
            wx = random.randint(0, width)
            wy = random.randint(0, height)
            draw.point((wx, wy), fill=(255, 105, 180, 200))
    elif season == "summer": # Sun rays / Glare
        draw.ellipse([width-40, 10, width-10, 40], fill=(255, 255, 0, 150))
    elif season == "autumn": # Rain
        for _ in range(50):
            wx = random.randint(0, width)
            wy = random.randint(0, height)
            draw.line([wx, wy, wx-2, wy+4], fill=(135, 206, 250, 150), width=1)
    elif season == "winter": # Snow
        for _ in range(50):
            wx = random.randint(0, width)
            wy = random.randint(0, height)
            draw.rectangle([wx, wy, wx+1, wy+1], fill=(255, 255, 255, 200))

    # 5. Character (Walking Animation)
    # Center character
    cx, cy = width // 2, height - 35
    
    # Attire colors
    attire = {
        "spring": ((144, 238, 144), (233, 196, 106)), # Green gear
        "summer": ((255, 215, 0), (233, 196, 106)),   # Yellow tee
        "autumn": ((139, 69, 19), (233, 196, 106)),   # Brown coat
        "winter": ((0, 0, 139), (255, 0, 0))          # Blue coat, Red hat
    }
    body_color, head_color = attire[season]
    
    # Legs animation (Simple scissor)
    # Frame index 0: left leg forward, 1: right leg forward
    leg_color = (0, 0, 0)
    if season == "summer": leg_color = (139, 69, 19) # Shorts -> bare legs (simplified)
    
    if frame_index % 2 == 0:
        # Left fwd, Right back
        draw.line([cx+4, cy+15, cx-2, cy+25], fill=leg_color, width=3)
        draw.line([cx+10, cy+15, cx+16, cy+25], fill=leg_color, width=3)
    else:
        # Right fwd, Left back
        draw.line([cx+4, cy+15, cx+10, cy+25], fill=leg_color, width=3)
        draw.line([cx+10, cy+15, cx-2, cy+25], fill=leg_color, width=3)
        
    # Torso
    draw.rectangle([cx, cy, cx+14, cy+15], fill=body_color + (255,))
    # Head
    draw.rectangle([cx+2, cy-12, cx+12, cy], fill=head_color + (255,))
    
    return img

if __name__ == "__main__":
    base_dir = "/home/abisin/.gemini/antigravity/brain/d18f038d-1088-4e59-b7ad-76281150e007"
    
    frames = []
    # 2 frames per season for walking effect
    for season in ["spring", "summer", "autumn", "winter"]:
        for i in range(2):
            img = draw_landscape(season, i)
            frames.append(img)
            
    # Save as GIF
    output_path = "/home/abisin/Desktop/abisinraj/assets/seasons_walking.gif"
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        optimize=False,
        duration=400, # 400ms per frame
        loop=0
    )
    print(f"Generated detailed GIF at {output_path}")
