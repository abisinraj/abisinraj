from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
import os
import random
import math

def hex_to_rgb(hex_color):
    try:
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    except ValueError:
        return (0, 0, 0) # Fallback

def draw_stardew_scene(season, frame_index, width=256, height=128):
    img = Image.new("RGBA", (width, height), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)

    # --- PALETTES (Stardew-inspired) ---
    palettes = {
        "spring": {
            "sky": "#87CEFA", "mountain": "#7B68EE", "road": "#8B4513", 
            "grass_base": "#66CD00", "grass_shade": "#458B00", "tree_trunk": "#8B4513", "tree_leaf": "#FF69B4",
            "river": "#1E90FF", "flower": "#FF69B4"
        },
        "summer": {
            "sky": "#00BFFF", "mountain": "#483D8B", "road": "#A0522D", 
            "grass_base": "#32CD32", "grass_shade": "#006400", "tree_trunk": "#8B4513", "tree_leaf": "#006400",
            "river": "#0000CD", "flower": "#FFD700"
        },
        "autumn": {
            "sky": "#FF7F50", "mountain": "#8B4513", "road": "#696969", 
            "grass_base": "#DAA520", "grass_shade": "#8B4513", "tree_trunk": "#654321", "tree_leaf": "#FF4500",
            "river": "#4682B4", "flower": "#800000"
        },
        "winter": {
            "sky": "#B0C4DE", "mountain": "#708090", "road": "#A9A9A9", 
            "grass_base": "#F0FFFF", "grass_shade": "#AFEEEE", "tree_trunk": "#2F4F4F", "tree_leaf": "#F0F8FF",
            "river": "#B0E0E6", "flower": "#FFFFFF" # Icy river color
        }
    }
    cols = {k: hex_to_rgb(v) for k, v in palettes[season].items()}

    # --- LAYERS ---
    # Concept: Top-down-ish perspective or Cross-view
    # Sky (Top 25%) -> Mountains (Horizon) -> Road (Mid-Top) -> Slope (Mid-Bottom) -> River (Bottom)
    
    sky_h = int(height * 0.3)
    road_top = sky_h
    road_bottom = int(height * 0.5) # Road is a band
    slope_bottom = int(height * 0.75)
    
    # 1. SKY & HORIZON
    draw.rectangle([0, 0, width, sky_h], fill=cols["sky"] + (255,))
    
    # Sun/Moon
    sun_col = (255, 255, 200, 200) if season != "autumn" else (255, 140, 0, 200)
    draw.ellipse([width - 50, 5, width - 10, 45], fill=sun_col)
    
    # Mountains (Far Background)
    mx_start = 0
    for i in range(5):
        peak_h = 30 + random.randint(-5, 5)
        base_w = 60 + random.randint(0, 20)
        draw.polygon([
            (mx_start, sky_h), 
            (mx_start + base_w//2, sky_h - peak_h), 
            (mx_start + base_w, sky_h)
        ], fill=cols["mountain"] + (255,))
        mx_start += base_w // 1.5

    # 2. TREES (Horizon Line - Behind Road)
    random.seed(99)
    for i in range(15):
        tx = random.randint(0, width)
        # Planted at horizon/road top edge
        ty = road_top + random.randint(-5, 5) 
        tw, th = 10, 30
        
        # Trunk
        draw.rectangle([tx, ty-th, tx+tw, ty], fill=cols["tree_trunk"] + (255,))
        # Foliage
        leaf_c = cols["tree_leaf"] + (255,)
        draw.polygon([(tx-6, ty-10), (tx+tw//2, ty-th-10), (tx+tw+6, ty-10)], fill=leaf_c)
        draw.polygon([(tx-6, ty-20), (tx+tw//2, ty-th-20), (tx+tw+6, ty-20)], fill=leaf_c)

    # 3. ROAD (Foreground Band)
    draw.rectangle([0, road_top, width, road_bottom], fill=cols["road"] + (255,))
    # Road Texture (Gravel/Paved)
    for _ in range(400):
        rx = random.randint(0, width)
        ry = random.randint(road_top, road_bottom)
        shade = random.choice([(60, 60, 60), (120, 120, 120)]) if season == "autumn" else [(100, 100, 100), (140, 140, 140)]
        draw.point((rx, ry), fill=shade + (255,))
    # Road Kerb?
    draw.line([0, road_bottom, width, road_bottom], fill=(50, 50, 50, 255), width=2)

    # 4. SLOPE (Midground Gradient)
    # Visualizing a slope going DOWN from road to river
    # Lighting: Darker at the top (shadow from road?) or Lighter?
    # Let's make it Darker at top, lighter at bottom to show depth/angle
    steps = 15
    step_h = (slope_bottom - road_bottom) / steps
    
    for i in range(steps):
        sy = road_bottom + i * step_h
        ey = sy + step_h + 1
        factor = i / steps # 0 to 1
        
        # Base green
        r, g, b = cols["grass_base"]
        
        # Shadow/Light Gradient
        # Top is darker (shadow), Bottom is lighter (catching light)
        shadow_intensity = 0.6 * (1 - factor) # Strong shadow at top
        
        r = int(r * (1 - shadow_intensity))
        g = int(g * (1 - shadow_intensity))
        b = int(b * (1 - shadow_intensity))
        
        draw.rectangle([0, sy, width, ey], fill=(r, g, b, 255))
        
    # Highlight Edge at top of slope (Slope Crest)
    draw.line([0, road_bottom, width, road_bottom], fill=(200, 200, 200, 100), width=1)

    # Slope Details
    if season != "winter":
        random.seed(42 + frame_index)
        for _ in range(40):
            fx = random.randint(0, width)
            fy = random.randint(road_bottom + 2, slope_bottom - 2)
            # Make flowers stand out more
            draw.rectangle([fx, fy, fx+1, fy+1], fill=cols["flower"] + (255,))

    # 5. RIVER (Bottom)
    draw.rectangle([0, slope_bottom, width, height], fill=cols["river"] + (255,))
    
    # Water Reflections & Flow
    scroll_offset = (frame_index * 6) % 24
    if season == "winter":
        scroll_offset = 0 # Frozen
        
    for y in range(slope_bottom + 4, height, 4):
        lw = random.randint(10, 40)
        lx = (random.randint(0, width) + scroll_offset) % width
        line_color = (255, 255, 255, 120)
        draw.line([lx, y, lx+lw, y], fill=line_color, width=1)


    # 6. AVATAR (Organic Animation)
    # Walking on the ROAD (road_bottom - offset)
    cx = width // 2
    foot_y = road_bottom - 5 # Just above the kerb
    
    # Body Colors
    skin_c = hex_to_rgb("#8D5524")
    hair_c = hex_to_rgb("#090806")
    pants_c = (0, 0, 139) if season != "summer" else (255, 215, 0)
    
    shirt_colors = {
        "spring": (144, 238, 144), "summer": (255, 215, 0),
        "autumn": (139, 69, 19), "winter": (178, 34, 34)
    }
    shirt_c = hex_to_rgb(str(shirt_colors[season])) if isinstance(shirt_colors[season], str) else shirt_colors[season]

    # Animation Frame Logic (0-7)
    # Cycle: Contact -> Recoil -> Passing -> High Point -> Contact...
    # Simplified to: Stride Right, Neutral, Stride Left, Neutral...
    
    # Helper to draw rotated limb (approximate via polygon)
    def draw_limb(start_x, start_y, length, angle_deg, thickness, color):
        angle_rad = math.radians(angle_deg)
        end_x = start_x + length * math.sin(angle_rad)
        end_y = start_y + length * math.cos(angle_rad)
        draw.line([start_x, start_y, end_x, end_y], fill=color, width=thickness)
        return end_x, end_y
        
    # Walk Cycle Parameters
    cycle_pct = (frame_index % 8) / 8.0
    # Hip Center
    hip_x, hip_y = cx, foot_y - 20 
    
    # Leg Angles (Sinusoid for fluidity)
    # Right Leg (Front)
    r_leg_angle = 30 * math.sin(cycle_pct * 2 * math.pi)
    # Left Leg (Back)
    l_leg_angle = 30 * math.sin(cycle_pct * 2 * math.pi + math.pi)
    
    # Knee Bend (Simple approximation: if angle imply back swing, bend knee)
    
    # Draw Left Leg (Behind)
    lx, ly = draw_limb(hip_x, hip_y, 10, l_leg_angle, 4, pants_c + (255,))
    draw_limb(lx, ly, 10, l_leg_angle, 4, pants_c + (255,)) # Lower leg
    
    # Body
    draw.rectangle([cx-6, hip_y-15, cx+6, hip_y], fill=shirt_c + (255,))
    if season == "winter": # Sweater Texture
        draw.line([cx-4, hip_y-12, cx+4, hip_y-12], fill=(139,0,0,255), width=1)
        draw.line([cx-4, hip_y-8, cx+4, hip_y-8], fill=(139,0,0,255), width=1)

    # Draw Right Leg (Front)
    rx, ry = draw_limb(hip_x, hip_y, 10, r_leg_angle, 4, pants_c + (255,))
    draw_limb(rx, ry, 10, r_leg_angle, 4, pants_c + (255,)) # Lower leg

    # Head
    head_y = hip_y - 25
    draw.rectangle([cx-5, head_y, cx+5, head_y+10], fill=skin_c + (255,))
    # Hair
    draw.rectangle([cx-6, head_y-2, cx+6, head_y+3], fill=hair_c + (255,))
    draw.rectangle([cx-6, head_y, cx-4, head_y+8], fill=hair_c + (255,)) # Back hair
    
    # Hat (Winter)
    if season == "winter":
        draw.rectangle([cx-6, head_y-3, cx+6, head_y], fill=(220, 20, 60, 255))
        draw.ellipse([cx-2, head_y-6, cx+2, head_y-2], fill=(255, 255, 255, 255))

    # Arms (Opposite to legs)
    # Right Arm (Front)
    r_arm_angle = 30 * math.sin(cycle_pct * 2 * math.pi + math.pi)
    shoulder_y = hip_y - 12
    ax, ay = draw_limb(cx, shoulder_y, 8, r_arm_angle, 3, shirt_c + (255,))
    draw_limb(ax, ay, 7, r_arm_angle, 3, skin_c + (255,)) # Forearm

    # Props
    if season == "autumn":
       # Net
       draw.line([cx+5, shoulder_y+5, cx+15, shoulder_y-10], fill=(100, 50, 0, 255), width=2)
       draw.ellipse([cx+12, shoulder_y-15, cx+20, shoulder_y-7], outline=(200, 200, 200, 255))

    return img

if __name__ == "__main__":
    frames = []
    # 8 frames per season
    for season in ["spring", "summer", "autumn", "winter"]:
        for i in range(8):
            img = draw_stardew_scene(season, i)
            frames.append(img)
            
    # Save as GIF
    output_path = "/home/abisin/Desktop/abisinraj/assets/seasons_walking.gif"
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        optimize=False,
        duration=120, 
        loop=0
    )
    print(f"Generated Organic Animation GIF at {output_path}")
