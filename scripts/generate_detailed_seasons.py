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
            "grass_base": "#66CD00", "grass_shade": "#458B00", "tree_trunk": "#8B4513", "tree_leaf": "#FFB7C5", # Sakura Pink
            "river": "#1E90FF", "flower": "#FF69B4"
        },
        "summer": {
            "sky": "#00BFFF", "mountain": "#483D8B", "road": "#A0522D", 
            "grass_base": "#32CD32", "grass_shade": "#006400", "tree_trunk": "#8B4513", "tree_leaf": "#008000",
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
            "river": "#B0E0E6", "flower": "#FFFFFF"
        }
    }
    cols = {k: hex_to_rgb(v) for k, v in palettes[season].items()}

    # --- SCROLL SPEEDS (Parallax) ---
    base_speed = 8 
    world_shift = frame_index * base_speed
    
    sky_h = int(height * 0.3)
    road_top = sky_h
    road_bottom = int(height * 0.5) 
    slope_bottom = int(height * 0.75)
    
    # 1. SKY & HORIZON
    draw.rectangle([0, 0, width, sky_h], fill=cols["sky"] + (255,))
    
    # Sun/Moon
    sun_col = (255, 255, 200, 200) if season != "autumn" else (255, 140, 0, 200)
    draw.ellipse([width - 50, 5, width - 10, 45], fill=sun_col)
    
    # Mountains (Fixed)
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

    # 2. TREES & WIND (Sakura - Parallax Scroll)
    tree_scroll = int(frame_index * 4) 
    random.seed(99) 
    for i in range(20): 
        orig_x = random.randint(-50, width + 300) 
        tx = (orig_x - tree_scroll) 
        
        if -20 < tx < width + 20:
            ty = road_top + random.randint(-5, 10) 
            tw, th = 12, 35
            
            # Trunk
            draw.rectangle([tx, ty-th, tx+tw, ty], fill=cols["tree_trunk"] + (255,))
            # Foliage
            leaf_c = cols["tree_leaf"] + (255,)
            draw.ellipse([tx-8, ty-th-15, tx+tw//2, ty-th], fill=leaf_c)
            draw.ellipse([tx+tw//2-5, ty-th-15, tx+tw+8, ty-th], fill=leaf_c)
            draw.ellipse([tx-2, ty-th-25, tx+tw+2, ty-th-5], fill=leaf_c)        
            
            # Falling petals (Sakura/Spring)
            # Add LOTS of petals
            if season == "spring":
                 random.seed(tx * 10) # Consistent per tree but random
                 for _ in range(5): # 5 petals per tree area
                     px = tx + random.randint(-30, 50) - (frame_index * 5) % 100 # Falling diagonally
                     py = ty - random.randint(-20, 40) + (frame_index * 2) % 40
                     draw.point((px, py), fill="#FF69B4") # Hot Pink

    # WIND & PARTICLES (Global)
    if season == "spring":
        # Wind Lines "Whooshing"
        wind_shift = int(frame_index * 15)
        random.seed(777)
        for i in range(10):
            wx_start = random.randint(-100, width)
            wy = random.randint(10, slope_bottom)
            
            wx = (wx_start + wind_shift) % (width + 100) - 50
            draw.line([wx, wy, wx+30, wy+2], fill=(255, 255, 255, 100), width=1)
            
    # Particles (Dust/Pollen)
    if season in ["spring", "summer"]:
        random.seed(frame_index + 100)
        for _ in range(30):
            dx = random.randint(0, width)
            dy = random.randint(0, height)
            d_col = (255, 255, 200, 150) if season=="summer" else (255, 192, 203, 150)
            draw.point((dx, dy), fill=d_col)

    # 3. ROAD (Foreground - Scrolled)
    draw.rectangle([0, road_top, width, road_bottom], fill=cols["road"] + (255,))
    
    random.seed(123) 
    for _ in range(400):
        orig_rx = random.randint(-width, width * 2)
        ry = random.randint(road_top, road_bottom)
        rx_wrapped = (orig_rx - world_shift) % width
        shade = random.choice([(60, 60, 60), (120, 120, 120)]) 
        draw.point((rx_wrapped, ry), fill=shade + (255,))

    # 4. SLOPE (Midground - Scrolled)
    steps = 15
    step_h = (slope_bottom - road_bottom) / steps
    for i in range(steps):
        sy = road_bottom + i * step_h
        ey = sy + step_h + 1
        factor = i / steps
        r, g, b = cols["grass_base"]
        shadow_intensity = 0.5 * (1 - factor)
        r = int(r * (1 - shadow_intensity))
        g = int(g * (1 - shadow_intensity))
        b = int(b * (1 - shadow_intensity))
        draw.rectangle([0, sy, width, ey], fill=(r, g, b, 255))
        
    draw.line([0, road_bottom, width, road_bottom], fill=(200, 200, 200, 100), width=1)

    if season != "winter":
        random.seed(42) 
        for _ in range(60):
            orig_fx = random.randint(0, width)
            fy = random.randint(road_bottom + 2, slope_bottom - 2)
            fx = (orig_fx - world_shift) % width
            draw.rectangle([fx, fy, fx+2, fy+2], fill=cols["flower"] + (255,))
            draw.line([fx+5, fy, fx+5, fy-3], fill=cols["grass_shade"]+(255,), width=1)

    # 5. RIVER (Bottom - Scrolled)
    draw.rectangle([0, slope_bottom, width, height], fill=cols["river"] + (255,))
    river_flow = frame_index * 10
    if season == "winter": river_flow = 0
    random.seed(55)
    for i in range(50):
        orig_lx = random.randint(0, width)
        y = random.randint(slope_bottom + 2, height - 2)
        lw = random.randint(10, 30)
        lx = (orig_lx - river_flow) % width
        l_col = (255, 255, 255, 120)
        draw.line([lx, y, lx+lw, y], fill=l_col, width=1)

    # 6. AVATAR (Refined Legs & Animation)
    cx = width // 2
    foot_y = road_bottom - 4
    
    skin_c = hex_to_rgb("#8D5524")
    hair_c = hex_to_rgb("#090806")
    # Change Summer Pants/Shirt to match request "change yellow cloth"
    pants_c = (0, 0, 139) # Blue jeans default
    
    shirt_colors = {
        "spring": (144, 238, 144), 
        "summer": (0, 191, 255), # Deep Sky Blue (No more Yellow)
        "autumn": (139, 69, 19), 
        "winter": (178, 34, 34)
    }
    shirt_c = hex_to_rgb(str(shirt_colors[season])) if isinstance(shirt_colors[season], str) else shirt_colors[season]

    # Helper for Two-Segment Limb (Thigh thicker than Calf)
    def draw_leg(hip_x, hip_y, angle, length, color, pants_c):
        # Angle in degrees
        rad = math.radians(angle)
        
        # Thigh (Thicker)
        thigh_len = length // 2 + 2
        knee_x = hip_x + thigh_len * math.sin(rad)
        knee_y = hip_y + thigh_len * math.cos(rad)
        
        draw.line([hip_x, hip_y, knee_x, knee_y], fill=pants_c, width=6) # Thigh Thickness 6
        
        # Calf (Thinner)
        # Simple straight leg for now (or slight bend if back leg)
        # Let's add slight bend offset for fluidity
        bend = 0
        if angle > 0: bend = -10 # Back leg bends
        
        rad2 = math.radians(angle + bend)
        calf_len = length // 2 + 2
        foot_x = knee_x + calf_len * math.sin(rad2)
        foot_y = knee_y + calf_len * math.cos(rad2)
        
        draw.line([knee_x, knee_y, foot_x, foot_y], fill=pants_c, width=4) # Calf Thickness 4
        return foot_x, foot_y
        
    cycle_pct = (frame_index % 8) / 8.0
    hip_x, hip_y = cx, foot_y - 22 
    
    # Angles
    r_leg_angle = 35 * math.sin(cycle_pct * 2 * math.pi)
    l_leg_angle = 35 * math.sin(cycle_pct * 2 * math.pi + math.pi)
    
    # Draw Legs
    # Left (Back)
    draw_leg(hip_x, hip_y, l_leg_angle, 12, pants_c + (255,), pants_c + (255,))
    
    # Body
    draw.rectangle([cx-7, hip_y-16, cx+7, hip_y], fill=shirt_c + (255,))
    if season == "winter":
        draw.line([cx-7, hip_y-12, cx+7, hip_y-12], fill=(100,0,0,255), width=2)

    # Right (Front)
    draw_leg(hip_x, hip_y, r_leg_angle, 12, pants_c + (255,), pants_c + (255,))

    # HEAD
    head_y = hip_y - 26
    draw.rectangle([cx-6, head_y, cx+6, head_y+11], fill=skin_c + (255,))
    draw.rectangle([cx-7, head_y-3, cx+7, head_y+4], fill=hair_c + (255,))
    draw.rectangle([cx-7, head_y, cx-5, head_y+9], fill=hair_c + (255,))
    
    if season == "winter":
        draw.rectangle([cx-7, head_y-4, cx+7, head_y], fill=(220, 20, 60, 255)) 

    # ARMS
    # Standard stick arm is fine, maybe slightly thicker
    r_arm_angle = 35 * math.sin(cycle_pct * 2 * math.pi + math.pi)
    shoulder_y = hip_y - 13
    rad_arm = math.radians(r_arm_angle)
    elbow_x = cx + 5 * math.sin(rad_arm)
    elbow_y = shoulder_y + 5 * math.cos(rad_arm)
    draw.line([cx, shoulder_y, elbow_x, elbow_y], fill=shirt_c + (255,), width=4)
    
    hand_x = elbow_x + 5 * math.sin(rad_arm - 0.2)
    hand_y = elbow_y + 5 * math.cos(rad_arm - 0.2)
    draw.line([elbow_x, elbow_y, hand_x, hand_y], fill=skin_c + (255,), width=3)


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
    print(f"Generated Final Spring/Legs GIF at {output_path}")
