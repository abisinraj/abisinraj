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
    # Avatar walks Right, World moves Left
    base_speed = 8 
    # Trees (Far) -> Slow
    # Road/Slope (Mid/Close) -> Fast (base_speed)
    # River (Fluid) -> base_speed + flow
    
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
    
    # Mountains (Fixed or VERY slow scroll? Fixed for simplicity as effective infinity)
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

    # 2. TREES (Sakura - Parallax Scroll)
    # Scroll slower than foreground
    tree_scroll = int(frame_index * 4) 
    random.seed(99) # Fixed seed for placement consistency
    for i in range(20): # More trees
        # Original X position
        orig_x = random.randint(-50, width + 300) # buffer for scrolling
        
        # Apply scroll
        tx = (orig_x - tree_scroll) 
        
        # Only draw if visible
        if -20 < tx < width + 20:
            ty = road_top + random.randint(-5, 10) 
            tw, th = 12, 35
            
            # Trunk
            draw.rectangle([tx, ty-th, tx+tw, ty], fill=cols["tree_trunk"] + (255,))
            # Foliage (Cloud shape for Sakura)
            leaf_c = cols["tree_leaf"] + (255,)
            
            # 3 Circles for foliage
            draw.ellipse([tx-8, ty-th-15, tx+tw//2, ty-th], fill=leaf_c)
            draw.ellipse([tx+tw//2-5, ty-th-15, tx+tw+8, ty-th], fill=leaf_c)
            draw.ellipse([tx-2, ty-th-25, tx+tw+2, ty-th-5], fill=leaf_c)        
            
            # Falling petals (Spring/Sakura)
            if season == "spring" and random.random() > 0.7:
                 px = tx + random.randint(-10, 20)
                 py = ty - random.randint(0, 30)
                 draw.point((px, py), fill="pink")

    # 3. ROAD (Foreground - Scrolled)
    draw.rectangle([0, road_top, width, road_bottom], fill=cols["road"] + (255,))
    
    # Scrolling Road Texture
    random.seed(123) # Seed for texture
    for _ in range(400):
        orig_rx = random.randint(-width, width * 2)
        ry = random.randint(road_top, road_bottom)
        
        rx = (orig_rx - world_shift) % (width * 2) - width # seamless wrap?
        # simpler loop wrap
        rx_wrapped = (orig_rx - world_shift) % width
        
        shade = random.choice([(60, 60, 60), (120, 120, 120)]) 
        draw.point((rx_wrapped, ry), fill=shade + (255,))

    # 4. SLOPE (Midground - Scrolled)
    # Gradient Slope
    steps = 15
    step_h = (slope_bottom - road_bottom) / steps
    
    # Base Gradient (Static relative to screen Y)
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
        
    # Highlight Edge
    draw.line([0, road_bottom, width, road_bottom], fill=(200, 200, 200, 100), width=1)

    # Scrolled Details (Flowers/Grass Tuft)
    if season != "winter":
        random.seed(42) # Consistent seed
        for _ in range(60):
            orig_fx = random.randint(0, width)
            fy = random.randint(road_bottom + 2, slope_bottom - 2)
            
            fx = (orig_fx - world_shift) % width
            
            # Draw Flower
            draw.rectangle([fx, fy, fx+2, fy+2], fill=cols["flower"] + (255,))
            # Draw Grass Tuft nearby
            draw.line([fx+5, fy, fx+5, fy-3], fill=cols["grass_shade"]+(255,), width=1)

    # 5. RIVER (Bottom - Scrolled)
    draw.rectangle([0, slope_bottom, width, height], fill=cols["river"] + (255,))
    
    # River Flow (Faster than walking? or fluid motion)
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
    
    # Colors
    skin_c = hex_to_rgb("#8D5524")
    hair_c = hex_to_rgb("#090806")
    pants_c = (0, 0, 139) if season != "summer" else (255, 215, 0)
    
    shirt_colors = {
        "spring": (144, 238, 144), "summer": (255, 215, 0),
        "autumn": (139, 69, 19), "winter": (178, 34, 34)
    }
    shirt_c = hex_to_rgb(str(shirt_colors[season])) if isinstance(shirt_colors[season], str) else shirt_colors[season]

    # Helper for Thick Line Limb
    def draw_thick_limb(start_x, start_y, length, angle_deg, thickness, color):
        angle_rad = math.radians(angle_deg)
        end_x = start_x + length * math.sin(angle_rad)
        end_y = start_y + length * math.cos(angle_rad)
        
        draw.line([start_x, start_y, end_x, end_y], fill=color, width=thickness)
        # Add round cap?
        draw.ellipse([end_x - thickness//2, end_y - thickness//2, end_x + thickness//2, end_y + thickness//2], fill=color)
        return end_x, end_y
        
    cycle_pct = (frame_index % 8) / 8.0
    hip_x, hip_y = cx, foot_y - 22 # Raised slightly
    
    # Angles
    r_leg_angle = 35 * math.sin(cycle_pct * 2 * math.pi)
    l_leg_angle = 35 * math.sin(cycle_pct * 2 * math.pi + math.pi)
    
    # Thicker Legs (Thickness 5)
    
    # LEFT Leg (Back)
    lx, ly = draw_thick_limb(hip_x, hip_y, 11, l_leg_angle, 5, pants_c + (255,))
    # Knee Bend logic: if lifting back, bend?
    # Simple straight lower leg for now, or slight offset
    draw_thick_limb(lx, ly, 11, l_leg_angle - (20 if l_leg_angle > 0 else 0), 5, pants_c + (255,))
    
    # BODY
    draw.rectangle([cx-7, hip_y-16, cx+7, hip_y], fill=shirt_c + (255,))
    if season == "winter":
        # Sweater pattern
        draw.line([cx-7, hip_y-12, cx+7, hip_y-12], fill=(100,0,0,255), width=2)

    # RIGHT Leg (Front)
    rx, ry = draw_thick_limb(hip_x, hip_y, 11, r_leg_angle, 5, pants_c + (255,))
    draw_thick_limb(rx, ry, 11, r_leg_angle + (20 if r_leg_angle < 0 else 0), 5, pants_c + (255,))

    # HEAD
    head_y = hip_y - 26
    draw.rectangle([cx-6, head_y, cx+6, head_y+11], fill=skin_c + (255,))
    # Hair
    draw.rectangle([cx-7, head_y-3, cx+7, head_y+4], fill=hair_c + (255,))
    draw.rectangle([cx-7, head_y, cx-5, head_y+9], fill=hair_c + (255,))
    
    if season == "winter":
        draw.rectangle([cx-7, head_y-4, cx+7, head_y], fill=(220, 20, 60, 255)) # Beanie

    # ARMS
    # Right Arm
    r_arm_angle = 35 * math.sin(cycle_pct * 2 * math.pi + math.pi)
    shoulder_y = hip_y - 13
    ax, ay = draw_thick_limb(cx, shoulder_y, 9, r_arm_angle, 4, shirt_c + (255,))
    draw_thick_limb(ax, ay, 8, r_arm_angle - 10, 4, skin_c + (255,))


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
    print(f"Generated Scrolled Sakura GIF at {output_path}")
