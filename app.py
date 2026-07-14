import streamlit as st
import json

st.set_page_config(page_title="My Packing Locker", page_icon="⛺", layout="wide")
st.title("⛺ My Packing Locker")
st.write("Your master locker is private to this browser session. Export a backup file below to save your changes permanently!")

# --- INTERACTIVE HTML EXPORT GENERATOR ---
def convert_to_interactive_note(filtered_items, selected_categories, note_title):
    html_output = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{note_title}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, sans-serif; max-width: 600px; margin: 30px auto; padding: 20px; background-color: #fcfcfc; color: #333; }}
        h1 {{ font-size: 28px; color: #111; margin-bottom: 5px; }}
        h2 {{ font-size: 18px; margin-top: 30px; border-bottom: 1px solid #eee; padding-bottom: 5px; color: #555; text-transform: uppercase; }}
        .checklist-item {{ display: flex; align-items: center; margin-bottom: 10px; font-size: 16px; }}
        .checklist-item input[type="checkbox"] {{ width: 20px; height: 20px; margin-right: 12px; cursor: pointer; accent-color: #ffb703; }}
        .checklist-item label {{ cursor: pointer; }}
        .checklist-item input[type="checkbox"]:checked + label {{ text-decoration: line-through; color: #888; }}
    </style>
</head>
<body>
    <h1>🎒 {note_title}</h1>
    <p style="color: #888; margin-top: 0; font-size: 14px;">Interactive Packing Checklist</p>
"""
    for cat in selected_categories:
        cat_strip = cat.strip()
        cat_items = [i for i in filtered_items if i["category"].strip() == cat_strip]
        if cat_items:
            html_output += f"\n    <h2>{cat_strip}</h2>\n"
            for item in cat_items:
                safe_id = f"item_{item['name'].lower().replace(' ', '_')}_{cat_strip.lower().replace(' ', '_')}"
                html_output += f'    <div class="checklist-item"><input type="checkbox" id="{safe_id}"><label for="{safe_id}">{item["name"]}</label></div>\n'
    html_output += "</body>\n</html>"
    return html_output

# --- INITIAL SYSTEM DATA TEMPLATE ---
def get_default_locker_data():
    return {
        "categories": [
            "⛺ Camping", "✨ Ambiance", "👕 Clothing", "🪥 Toiletries", "🍳 Cooking", 
            "🎒 Backpacking", "🧭 Hiking", "🌊 Surf & Water Sports", "🎣 Fishing", 
            "🛶 Boating", "🧗 Climbing", "🏃 Trail Running", "🚴 Cycling", "🎿 Skiing", 
            "🚌 VW Bus Trip", "📱 Devices", "📋 Tasks", "🤖 Other"
        ],
        "weather_profiles": ["🌤️ Always", "🔥 Hot", "❄️ Snow"],
        "master_items": [
            # ⛺ Camping
            {"name": "Tent", "category": "⛺ Camping", "weather": ["🌤️ Always"]},
            {"name": "Footprint", "category": "⛺ Camping", "weather": ["🌤️ Always"]},
            {"name": "Tent stakes", "category": "⛺ Camping", "weather": ["🌤️ Always"]},
            {"name": "Sleeping bags", "category": "⛺ Camping", "weather": ["🌤️ Always"]},
            {"name": "Sleeping pads", "category": "⛺ Camping", "weather": ["🌤️ Always"]},
            {"name": "Insulated high R-value sleeping pads", "category": "⛺ Camping", "weather": ["❄️ Snow"]},
            {"name": "Sheet", "category": "⛺ Camping", "weather": ["🌤️ Always"]},
            {"name": "Comforter", "category": "⛺ Camping", "weather": ["🌤️ Always"]},
            {"name": "Heavy Blanket", "category": "⛺ Camping", "weather": ["🌤️ Always"]},
            {"name": "Full sized pillow", "category": "⛺ Camping", "weather": ["🌤️ Always"]},
            {"name": "Shadowcaster shade", "category": "⛺ Camping", "weather": ["🌤️ Always"]},
            {"name": "Camp chairs", "category": "⛺ Camping", "weather": ["🌤️ Always"]},
            {"name": "Alite chairs", "category": "⛺ Camping", "weather": ["🌤️ Always"]},
            {"name": "Camp table", "category": "⛺ Camping", "weather": ["🌤️ Always"]},
            {"name": "First aid kit", "category": "⛺ Camping", "weather": ["🌤️ Always"]},
            {"name": "Multi-tool or pocket knife", "category": "⛺ Camping", "weather": ["🌤️ Always"]},
            {"name": "Repair kit", "category": "⛺ Camping", "weather": ["🌤️ Always"]},
            {"name": "Duct tape", "category": "⛺ Camping", "weather": ["🌤️ Always"]},
            {"name": "Paracord", "category": "⛺ Camping", "weather": ["🌤️ Always"]},
            {"name": "Trash bags", "category": "⛺ Camping", "weather": ["🌤️ Always"]},
            {"name": "Lanterns", "category": "⛺ Camping", "weather": ["🌤️ Always"]},
            {"name": "Wood", "category": "⛺ Camping", "weather": ["🌤️ Always"]},
            {"name": "Newspaper or fire starters", "category": "⛺ Camping", "weather": ["🌤️ Always"]},
            {"name": "Hand & toe warmers", "category": "⛺ Camping", "weather": ["❄️ Snow"]},
            
            # ✨ Ambiance
            {"name": "Rechargeable LED string lights", "category": "✨ Ambiance", "weather": ["🌤️ Always"]},
            {"name": "Bluetooth speaker", "category": "✨ Ambiance", "weather": ["🌤️ Always"]},
            {"name": "Picnic blanket", "category": "✨ Ambiance", "weather": ["🌤️ Always"]},
            {"name": "Puffin blanket", "category": "✨ Ambiance", "weather": ["🌤️ Always"]},
            {"name": "Pendelton blanket", "category": "✨ Ambiance", "weather": ["🌤️ Always"]},
            {"name": "Citronella candle / incense sticks", "category": "✨ Ambiance", "weather": ["🔥 Hot"]},
            {"name": "Table cloth", "category": "✨ Ambiance", "weather": ["🌤️ Always"]},
            {"name": "Silverware", "category": "✨ Ambiance", "weather": ["🌤️ Always"]},
            {"name": "Cute coffee mugs", "category": "✨ Ambiance", "weather": ["🌤️ Always"]},
            
            # 👕 Clothing
            {"name": "T-shirts", "category": "👕 Clothing", "weather": ["🌤️ Always"]},
            {"name": "Tank tops", "category": "👕 Clothing", "weather": ["🌤️ Always"]},
            {"name": "Underwear/Bras", "category": "👕 Clothing", "weather": ["🌤️ Always"]},
            {"name": "Socks", "category": "👕 Clothing", "weather": ["🌤️ Always"]},
            {"name": "Quick-dry shorts", "category": "👕 Clothing", "weather": ["🌤️ Always"]},
            {"name": "Quick-dry pants", "category": "👕 Clothing", "weather": ["🌤️ Always"]},
            {"name": "Yoga pants", "category": "👕 Clothing", "weather": ["🌤️ Always"]},
            {"name": "Puffy jacket", "category": "👕 Clothing", "weather": ["🌤️ Always"]},
            {"name": "Sweatshirt", "category": "👕 Clothing", "weather": ["🌤️ Always"]},
            {"name": "Windbreaker jacket", "category": "👕 Clothing", "weather": ["🌤️ Always"]},
            {"name": "Rain jacket (waterproof shell)", "category": "👕 Clothing", "weather": ["🌤️ Always"]},
            {"name": "Sweatpants", "category": "👕 Clothing", "weather": ["🌤️ Always"]},
            {"name": "Sleeping clothes", "category": "👕 Clothing", "weather": ["🌤️ Always"]},
            {"name": "Swimwear", "category": "👕 Clothing", "weather": ["🔥 Hot"]},
            {"name": "Wide-brim sun hat or baseball cap", "category": "👕 Clothing", "weather": ["🔥 Hot"]},
            {"name": "Thermal long-underwear bottoms", "category": "👕 Clothing", "weather": ["❄️ Snow"]},
            {"name": "Mid layer top", "category": "👕 Clothing", "weather": ["❄️ Snow"]},
            {"name": "Heavyweight wool socks", "category": "👕 Clothing", "weather": ["❄️ Snow"]},
            
            # 🪥 Toiletries
            {"name": "Toothbrush", "category": "🪥 Toiletries", "weather": ["🌤️ Always"]},
            {"name": "Toothpaste", "category": "🪥 Toiletries", "weather": ["🌤️ Always"]},
            {"name": "Deodorant", "category": "🪥 Toiletries", "weather": ["🌤️ Always"]},
            {"name": "Soap", "category": "🪥 Toiletries", "weather": ["🌤️ Always"]},
            {"name": "Shampoo", "category": "🪥 Toiletries", "weather": ["🌤️ Always"]},
            {"name": "Conditioner", "category": "🪥 Toiletries", "weather": ["🌤️ Always"]},
            {"name": "Razor", "category": "🪥 Toiletries", "weather": ["🌤️ Always"]},
            {"name": "Sunscreen", "category": "🪥 Toiletries", "weather": ["🌤️ Always"]},
            {"name": "Mosquito repellant", "category": "🪥 Toiletries", "weather": ["🌤️ Always"]},
            {"name": "Pain Meds", "category": "🪥 Toiletries", "weather": ["🌤️ Always"]},
            {"name": "Allergy Meds", "category": "🪥 Toiletries", "weather": ["🌤️ Always"]},
            {"name": "Other Meds", "category": "🪥 Toiletries", "weather": ["🌤️ Always"]},
            {"name": "Tweezers", "category": "🪥 Toiletries", "weather": ["🌤️ Always"]},
            {"name": "Nail Clippers", "category": "🪥 Toiletries", "weather": ["🌤️ Always"]},
            
            # 🍳 Cooking
            {"name": "Propane camp stove", "category": "🍳 Cooking", "weather": ["🌤️ Always"]},
            {"name": "Butane camp stove", "category": "🍳 Cooking", "weather": ["🌤️ Always"]},
            {"name": "Ultralight camp stove", "category": "🍳 Cooking", "weather": ["🌤️ Always"]},
            {"name": "Fuel canister(s)", "category": "🍳 Cooking", "weather": ["🌤️ Always"]},
            {"name": "Lighter / matches / flint striker", "category": "🍳 Cooking", "weather": ["🌤️ Always"]},
            {"name": "Stove grate", "category": "🍳 Cooking", "weather": ["🌤️ Always"]},
            {"name": "REI Cooler", "category": "🍳 Cooking", "weather": ["🌤️ Always"]},
            {"name": "Coleman Cooler", "category": "🍳 Cooking", "weather": ["🌤️ Always"]},
            {"name": "Icepacks/Ice", "category": "🍳 Cooking", "weather": ["🌤️ Always"]},
            {"name": "Water filtration system or large water jug", "category": "🍳 Cooking", "weather": ["🌤️ Always"]},
            {"name": "Nesting cookset (pots, pans, lids)", "category": "🍳 Cooking", "weather": ["🌤️ Always"]},
            {"name": "Big pan", "category": "🍳 Cooking", "weather": ["🌤️ Always"]},
            {"name": "Cutting board", "category": "🍳 Cooking", "weather": ["🌤️ Always"]},
            {"name": "Kitchen knife", "category": "🍳 Cooking", "weather": ["🌤️ Always"]},
            {"name": "Spatula", "category": "🍳 Cooking", "weather": ["🌤️ Always"]},
            {"name": "Cooking tongs", "category": "🍳 Cooking", "weather": ["🌤️ Always"]},
            {"name": "Large serving spoon", "category": "🍳 Cooking", "weather": ["🌤️ Always"]},
            {"name": "Rotating roasting sticks", "category": "🍳 Cooking", "weather": ["🌤️ Always"]},
            {"name": "Plates & bowls", "category": "🍳 Cooking", "weather": ["🌤️ Always"]},
            {"name": "Eating utensils (spork/knife)", "category": "🍳 Cooking", "weather": ["🌤️ Always"]},
            {"name": "Napkins", "category": "🍳 Cooking", "weather": ["🌤️ Always"]},
            {"name": "Paper towels", "category": "🍳 Cooking", "weather": ["🌤️ Always"]},
            {"name": "Spices – salt, pepper, etc", "category": "🍳 Cooking", "weather": ["🌤️ Always"]},
            {"name": "Biodegradable camp soap", "category": "🍳 Cooking", "weather": ["🌤️ Always"]},
            {"name": "Sponge / scrubber", "category": "🍳 Cooking", "weather": ["🌤️ Always"]},
            {"name": "Quick-dry dish towel", "category": "🍳 Cooking", "weather": ["🌤️ Always"]},
            
            # 🎒 Backpacking
            {"name": "Backpacks", "category": "🎒 Backpacking", "weather": ["🌤️ Always"]},
            {"name": "Ultralight sleeping pads", "category": "🎒 Backpacking", "weather": ["🌤️ Always"]},
            {"name": "Foam 40”", "category": "🎒 Backpacking", "weather": ["🌤️ Always"]},
            {"name": "Slipcover duo 40”", "category": "🎒 Backpacking", "weather": ["🌤️ Always"]},
            {"name": "Backpacking pillow", "category": "🎒 Backpacking", "weather": ["🌤️ Always"]},
            {"name": "Bear canister or food hang bag with paracord", "category": "🎒 Backpacking", "weather": ["🌤️ Always"]},
            {"name": "Water Filter", "category": "🎒 Backpacking", "weather": ["🌤️ Always"]},
            {"name": "Lightweight backpacking stove", "category": "🎒 Backpacking", "weather": ["🌤️ Always"]},
            {"name": "Lightweight cookset", "category": "🎒 Backpacking", "weather": ["🌤️ Always"]},
            {"name": "Trowel", "category": "🎒 Backpacking", "weather": ["🌤️ Always"]},
            {"name": "Biodegradable soap", "category": "🎒 Backpacking", "weather": ["🌤️ Always"]},
            
            # 🧭 Hiking
            {"name": "Daypack", "category": "🧭 Hiking", "weather": ["🌤️ Always"]},
            {"name": "Hydration bladder", "category": "🧭 Hiking", "weather": ["🌤️ Always"]},
            {"name": "Water bottles (2L capacity)", "category": "🧭 Hiking", "weather": ["🌤️ Always"]},
            {"name": "Topographic map & physical compass", "category": "🧭 Hiking", "weather": ["🌤️ Always"]},
            {"name": "Trekking poles", "category": "🧭 Hiking", "weather": ["🌤️ Always"]},
            {"name": "Moleskin / blister kit", "category": "🧭 Hiking", "weather": ["🌤️ Always"]},
            {"name": "High-energy trail mix & snacks", "category": "🧭 Hiking", "weather": ["🌤️ Always"]},
            
            # 🌊 Surf & Water Sports
            {"name": "Surfboard(s)", "category": "🌊 Surf & Water Sports", "weather": ["🌤️ Always"]},
            {"name": "Fins", "category": "🌊 Surf & Water Sports", "weather": ["🌤️ Always"]},
            {"name": "Towel", "category": "🌊 Surf & Water Sports", "weather": ["🌤️ Always"]},
            {"name": "Changing bin", "category": "🌊 Surf & Water Sports", "weather": ["🌤️ Always"]},
            {"name": "Water jug", "category": "🌊 Surf & Water Sports", "weather": ["🌤️ Always"]},
            {"name": "Board bag", "category": "🌊 Surf & Water Sports", "weather": ["🌤️ Always"]},
            {"name": "Board Sock", "category": "🌊 Surf & Water Sports", "weather": ["🌤️ Always"]},
            {"name": "Surfboard leash", "category": "🌊 Surf & Water Sports", "weather": ["🌤️ Always"]},
            {"name": "Fin key", "category": "🌊 Surf & Water Sports", "weather": ["🌤️ Always"]},
            {"name": "Spare fin screws", "category": "🌊 Surf & Water Sports", "weather": ["🌤️ Always"]},
            {"name": "Vehicle tie-down straps / soft racks", "category": "🌊 Surf & Water Sports", "weather": ["🌤️ Always"]},
            {"name": "Waterproof dry bag", "category": "🌊 Surf & Water Sports", "weather": ["🌤️ Always"]},
            {"name": "Rash guard / UV protection shirt", "category": "🌊 Surf & Water Sports", "weather": ["🔥 Hot"]},
            {"name": "Sunscreen - reef safe", "category": "🌊 Surf & Water Sports", "weather": ["🔥 Hot"]},
            {"name": "Tropical surfboard wax (basecoat + topcoat)", "category": "🌊 Surf & Water Sports", "weather": ["🔥 Hot"]},
            {"name": "Wetsuit (4/3mm or 5/4mm)", "category": "🌊 Surf & Water Sports", "weather": ["🌤️ Always"]},
            {"name": "Neoprene booties/gloves", "category": "🌊 Surf & Water Sports", "weather": ["❄️ Snow"]},
            {"name": "Cold-water surfboard wax", "category": "🌊 Surf & Water Sports", "weather": ["🌤️ Always"]},
            {"name": "Ear drops", "category": "🌊 Surf & Water Sports", "weather": ["🌤️ Always"]},
            
            # 🎣 Fishing
            {"name": "Fishing rods", "category": "🎣 Fishing", "weather": ["🌤️ Always"]},
            {"name": "Tenkara Rods", "category": "🎣 Fishing", "weather": ["🌤️ Always"]},
            {"name": "Flies", "category": "🎣 Fishing", "weather": ["🌤️ Always"]},
            {"name": "Line & tippet", "category": "🎣 Fishing", "weather": ["🌤️ Always"]},
            {"name": "Fishing license", "category": "🎣 Fishing", "weather": ["🌤️ Always"]},
            {"name": "Needle-nose pliers with wire cutters", "category": "🎣 Fishing", "weather": ["🌤️ Always"]},
            {"name": "Line nippers", "category": "🎣 Fishing", "weather": ["🌤️ Always"]},
            {"name": "Patagonia fishing backpack", "category": "🎣 Fishing", "weather": ["🌤️ Always"]},
            {"name": "Chain for caught fish", "category": "🎣 Fishing", "weather": ["🌤️ Always"]},
            {"name": "Fishing waders", "category": "🎣 Fishing", "weather": ["❄️ Snow"]},
            {"name": "Insulated wading boots", "category": "🎣 Fishing", "weather": ["❄️ Snow"]},
            
            # 🛶 Boating
            {"name": "Life jackets / PFDs", "category": "🛶 Boating", "weather": ["🌤️ Always"]},
            {"name": "Paddles or oars", "category": "🛶 Boating", "weather": ["🌤️ Always"]},
            {"name": "Safety throw line", "category": "🛶 Boating", "weather": ["🌤️ Always"]},
            {"name": "Inflatable kayak", "category": "🛶 Boating", "weather": ["🌤️ Always"]},
            {"name": "Explorer 300", "category": "🛶 Boating", "weather": ["🌤️ Always"]},
            {"name": "Large Pump", "category": "🛶 Boating", "weather": ["🌤️ Always"]},
            {"name": "Bilge pump or bailer", "category": "🛶 Boating", "weather": ["🌤️ Always"]},
            {"name": "Dry bag", "category": "🛶 Boating", "weather": ["🌤️ Always"]},
            
            # 🧗 Climbing
            {"name": "Climbing harness", "category": "🧗 Climbing", "weather": ["🌤️ Always"]},
            {"name": "Climbing shoes", "category": "🧗 Climbing", "weather": ["🌤️ Always"]},
            {"name": "Climbing helmet", "category": "🧗 Climbing", "weather": ["🌤️ Always"]},
            {"name": "Chalk bag with chalk", "category": "🧗 Climbing", "weather": ["🌤️ Always"]},
            {"name": "Dynamic climbing rope", "category": "🧗 Climbing", "weather": ["🌤️ Always"]},
            {"name": "Belay device", "category": "🧗 Climbing", "weather": ["🌤️ Always"]},
            {"name": "Locking carabiners", "category": "🧗 Climbing", "weather": ["🌤️ Always"]},
            {"name": "Anchor material", "category": "🧗 Climbing", "weather": ["🌤️ Always"]},
            {"name": "Nylon runners / slings", "category": "🧗 Climbing", "weather": ["🌤️ Always"]},
            
            # 🏃 Trail Running
            {"name": "Trail running shoes", "category": "🏃 Trail Running", "weather": ["🌤️ Always"]},
            {"name": "Trail running socks", "category": "🏃 Trail Running", "weather": ["🌤️ Always"]},
            {"name": "Sports bra", "category": "🏃 Trail Running", "weather": ["🌤️ Always"]},
            {"name": "Running Tank", "category": "🏃 Trail Running", "weather": ["🌤️ Always"]},
            {"name": "Hydration vest or running belt", "category": "🏃 Trail Running", "weather": ["🌤️ Always"]},
            {"name": "High-energy blocks", "category": "🏃 Trail Running", "weather": ["🌤️ Always"]},
            {"name": "Lightweight running shorts", "category": "🏃 Trail Running", "weather": ["🔥 Hot"]},
            {"name": "Thermal running tights", "category": "🏃 Trail Running", "weather": ["❄️ Snow"]},
            {"name": "Lightweight windproof gloves", "category": "🏃 Trail Running", "weather": ["❄️ Snow"]},
            {"name": "Ear-warmer headband", "category": "🏃 Trail Running", "weather": ["❄️ Snow"]},
            
            # 🚴 Cycling
            {"name": "Bike (Road/Gravel/Mountain)", "category": "🚴 Cycling", "weather": ["🌤️ Always"]},
            {"name": "Helmet", "category": "🚴 Cycling", "weather": ["🌤️ Always"]},
            {"name": "Cycling lights", "category": "🚴 Cycling", "weather": ["🌤️ Always"]},
            {"name": "Cycling shoes", "category": "🚴 Cycling", "weather": ["🌤️ Always"]},
            {"name": "Padded bib shorts / chamois", "category": "🚴 Cycling", "weather": ["🌤️ Always"]},
            {"name": "Cycling jersey", "category": "🚴 Cycling", "weather": ["🌤️ Always"]},
            {"name": "Cycling jacket", "category": "🚴 Cycling", "weather": ["🌤️ Always"]},
            {"name": "Lightweight wind vest", "category": "🚴 Cycling", "weather": ["🌤️ Always"]},
            {"name": "Water bottles / cages (2x)", "category": "🚴 Cycling", "weather": ["🌤️ Always"]},
            {"name": "Bike computer", "category": "🚴 Cycling", "weather": ["🌤️ Always"]},
            {"name": "Saddle bag with spare tube & tire levers", "category": "🚴 Cycling", "weather": ["🌤️ Always"]},
            {"name": "Mini bike pump or CO2 inflator", "category": "🚴 Cycling", "weather": ["🌤️ Always"]},
            {"name": "Multi-tool with chain breaker", "category": "🚴 Cycling", "weather": ["🌤️ Always"]},
            {"name": "Arm & leg warmers", "category": "🚴 Cycling", "weather": ["❄️ Snow"]},
            {"name": "Thermal shoe covers (booties)", "category": "🚴 Cycling", "weather": ["❄️ Snow"]},
            
            # 🎿 Skiing
            {"name": "Front country Skis", "category": "🎿 Skiing", "weather": ["❄️ Snow"]},
            {"name": "Backcountry Skis", "category": "🎿 Skiing", "weather": ["❄️ Snow"]},
            {"name": "Cross-country Skis", "category": "🎿 Skiing", "weather": ["❄️ Snow"]},
            {"name": "Ski boots", "category": "🎿 Skiing", "weather": ["❄️ Snow"]},
            {"name": "Ski poles", "category": "🎿 Skiing", "weather": ["❄️ Snow"]},
            {"name": "Ski helmet", "category": "🎿 Skiing", "weather": ["❄️ Snow"]},
            {"name": "Goggles (with lenses)", "category": "🎿 Skiing", "weather": ["❄️ Snow"]},
            {"name": "Waterproof ski jacket", "category": "🎿 Skiing", "weather": ["❄️ Snow"]},
            {"name": "Waterproof ski bibs", "category": "🎿 Skiing", "weather": ["❄️ Snow"]},
            {"name": "Puffy Jacket", "category": "🎿 Skiing", "weather": ["❄️ Snow"]},
            {"name": "Base layers", "category": "🎿 Skiing", "weather": ["❄️ Snow"]},
            {"name": "Mid layers", "category": "🎿 Skiing", "weather": ["❄️ Snow"]},
            {"name": "Ski socks (2-3 pairs)", "category": "🎿 Skiing", "weather": ["❄️ Snow"]},
            {"name": "Heavyweight gloves / mittens", "category": "🎿 Skiing", "weather": ["❄️ Snow"]},
            {"name": "Lightweight gloves / mittens", "category": "🎿 Skiing", "weather": ["❄️ Snow"]},
            {"name": "Glove liners", "category": "🎿 Skiing", "weather": ["❄️ Snow"]},
            {"name": "Balaclava or neck gaiter", "category": "🎿 Skiing", "weather": ["❄️ Snow"]},
            {"name": "Beacon", "category": "🎿 Skiing", "weather": ["❄️ Snow"]},
            {"name": "Avy probe", "category": "🎿 Skiing", "weather": ["❄️ Snow"]},
            {"name": "Shovel", "category": "🎿 Skiing", "weather": ["❄️ Snow"]},
            {"name": "Backcountry pack", "category": "🎿 Skiing", "weather": ["❄️ Snow"]},
            {"name": "Skins", "category": "🎿 Skiing", "weather": ["❄️ Snow"]},
            {"name": "Ice Ax", "category": "🎿 Skiing", "weather": ["❄️ Snow"]},
            {"name": "Harness/anchors", "category": "🎿 Skiing", "weather": ["❄️ Snow"]},
            {"name": "Ski pass", "category": "🎿 Skiing", "weather": ["❄️ Snow"]},
            {"name": "Sno Park permit", "category": "🎿 Skiing", "weather": ["❄️ Snow"]},
            {"name": "Reserve parking ahead", "category": "🎿 Skiing", "weather": ["❄️ Snow"]},
            {"name": "Pocket hand warmers", "category": "🎿 Skiing", "weather": ["❄️ Snow"]},
            {"name": "Ski strap (for carrying skis easily)", "category": "🎿 Skiing", "weather": ["❄️ Snow"]},
            {"name": "Spare part kit", "category": "🎿 Skiing", "weather": ["❄️ Snow"]},
            
            # 🚌 VW Bus Trip
            {"name": "VW mechanical tool roll & metric sockets", "category": "🚌 VW Bus Trip", "weather": ["🌤️ Always"]},
            {"name": "Engine oil (Type 4 or preferred weight, 1-2 quarts)", "category": "🚌 VW Bus Trip", "weather": ["🌤️ Always"]},
            {"name": "Jumper cables", "category": "🚌 VW Bus Trip", "weather": ["🌤️ Always"]},
            {"name": "Leveling blocks / chocks", "category": "🚌 VW Bus Trip", "weather": ["🌤️ Always"]},
            {"name": "Shore power extension cord & adapters", "category": "🚌 VW Bus Trip", "weather": ["🌤️ Always"]},
            {"name": "Water Filter", "category": "🚌 VW Bus Trip", "weather": ["🌤️ Always"]},
            {"name": "Staples - Salt, pepper, chili flakes, chai, OVOO, soap, foil, Ziplock’s, ramen", "category": "🚌 VW Bus Trip", "weather": ["🌤️ Always"]},
            {"name": "Toilet", "category": "🚌 VW Bus Trip", "weather": ["🌤️ Always"]},
            {"name": "Toilet paper", "category": "🚌 VW Bus Trip", "weather": ["🌤️ Always"]},
            {"name": "Paper towels", "category": "🚌 VW Bus Trip", "weather": ["🌤️ Always"]},
            {"name": "Charged lights", "category": "🚌 VW Bus Trip", "weather": ["🌤️ Always"]},
            
            # 📱 Devices
            {"name": "Phones", "category": "📱 Devices", "weather": ["🌤️ Always"]},
            {"name": "Computers", "category": "📱 Devices", "weather": ["🌤️ Always"]},
            {"name": "Ipad", "category": "📱 Devices", "weather": ["🌤️ Always"]},
            {"name": "Watch", "category": "📱 Devices", "weather": ["🌤️ Always"]},
            {"name": "High-capacity power bank", "category": "📱 Devices", "weather": ["🌤️ Always"]},
            {"name": "Ultralight power bank", "category": "📱 Devices", "weather": ["🌤️ Always"]},
            {"name": "Charging cables (USB-C, Lightning, etc.)", "category": "📱 Devices", "weather": ["🌤️ Always"]},
            {"name": "Headlamp & charging cords", "category": "📱 Devices", "weather": ["🌤️ Always"]},
            {"name": "GPS", "category": "📱 Devices", "weather": ["🌤️ Always"]},
            {"name": "Waterproof phone pouch", "category": "📱 Devices", "weather": ["🌤️ Always"]},
            
            # 📋 Tasks
            {"name": "Fully charge lights, lamps, devices", "category": "📋 Tasks", "weather": ["🌤️ Always"]},
            {"name": "Download offline maps", "category": "📋 Tasks", "weather": ["🌤️ Always"]},
            {"name": "Water Bonnie", "category": "📋 Tasks", "weather": ["🌤️ Always"]},
            {"name": "Water indoor plants/fill jars", "category": "📋 Tasks", "weather": ["🌤️ Always"]},
            {"name": "Take out compost", "category": "📋 Tasks", "weather": ["🌤️ Always"]},
            {"name": "Take down trash", "category": "📋 Tasks", "weather": ["🌤️ Always"]},
            {"name": "Run dishwasher", "category": "📋 Tasks", "weather": ["🌤️ Always"]},
            
            # 🤖 Other
            {"name": "IDs", "category": "🤖 Other", "weather": ["🌤️ Always"]},
            {"name": "Cash", "category": "🤖 Other", "weather": ["🌤️ Always"]},
            {"name": "Chapstick", "category": "🤖 Other", "weather": ["🌤️ Always"]},
            {"name": "Polarized sunglasses", "category": "🤖 Other", "weather": ["🌤️ Always"]},
            {"name": "National Park Pass", "category": "🤖 Other", "weather": ["🌤️ Always"]},
            {"name": "California Park Pass", "category": "🤖 Other", "weather": ["🌤️ Always"]},
            {"name": "Camera", "category": "🤖 Other", "weather": ["🌤️ Always"]},
            {"name": "Notebook", "category": "🤖 Other", "weather": ["🌤️ Always"]},
            {"name": "Pen", "category": "🤖 Other", "weather": ["🌤️ Always"]},
            {"name": "Art supplies", "category": "🤖 Other", "weather": ["🌤️ Always"]},
            {"name": "Reading material", "category": "🤖 Other", "weather": ["🌤️ Always"]},
            {"name": "Baseball cap", "category": "🤖 Other", "weather": ["🌤️ Always"]},
            {"name": "Warm beanie", "category": "🤖 Other", "weather": ["❄️ Snow"]},
            {"name": "Hammock", "category": "🤖 Other", "weather": ["🌤️ Always"]},
            {"name": "Cards/games", "category": "🤖 Other", "weather": ["🌤️ Always"]},
            {"name": "Electrolytes", "category": "🤖 Other", "weather": ["🌤️ Always"]}
        ],
        "saved_trips": {}, "deleted_items": []
    }

# --- STATE INITIALIZATION (BROWSER SESSION ONLY) ---
default_template = get_default_locker_data()
for key in ["categories", "weather_profiles", "master_items", "saved_trips", "deleted_items"]:
    if key not in st.session_state: 
        st.session_state[key] = default_template[key]

DEFAULT_CHECKED_CATS = ["camping", "ambiance", "clothing", "toiletries", "cooking", "devices", "tasks", "other"]
EMOJIS = ["⛺", "✨", "👕", "🪥", "🍳", "🎒", "🧭", "🌊", "🎣", "🛶", "🧗", "🏃", "🚴", "🎿", "🚌", "📱", "📋", "🤖", "🌤️", "🔥", "❄️"]

# ==========================================
# --- SIDEBAR SECTION 1: TRIP SETTINGS ---
# ==========================================
st.sidebar.subheader("🌴 Trip Settings")

st.sidebar.write("**Expected Weather Profiles:**")
selected_weather = []
for w_prof in st.session_state.weather_profiles:
    w_prof_clean = w_prof.strip()
    w_default = "Always" in w_prof_clean
    w_key = f"weather_filter_{w_prof_clean}"
    if st.sidebar.checkbox(w_prof, value=w_default, key=w_key):
        selected_weather.append(w_prof_clean)

st.sidebar.write("**Select Activities / Categories:**")
selected_categories = []
for cat in st.session_state.categories:
    cat_strip = cat.strip()
    clean_cat_name = "".join(c for c in cat_strip if c.isalnum() or c.isspace()).strip().lower()
    cat_default = any(tgt in clean_cat_name for tgt in DEFAULT_CHECKED_CATS)
    
    c_key = f"filter_{cat_strip}"
    if st.sidebar.checkbox(cat, value=cat_default, key=c_key):
        selected_categories.append(cat_strip)

st.sidebar.markdown("---")

# ==========================================
# --- SIDEBAR SECTION 2: CONFIGURATION DESK ---
# ==========================================
st.sidebar.header("⚙️ Configuration Desk")

with st.sidebar.expander("💾 Locker Data Backup (Import/Export)", expanded=False):
    st.write("Keep your custom locker data safe across visits or share templates.")
    
    export_payload = {
        "categories": st.session_state.categories,
        "weather_profiles": st.session_state.weather_profiles,
        "master_items": st.session_state.master_items,
        "saved_trips": st.session_state.saved_trips,
        "deleted_items": st.session_state.deleted_items
    }
    json_string = json.dumps(export_payload, indent=4)
    
    st.download_button(
        label="📥 Download Locker Backup (.json)",
        data=json_string,
        file_name="my_packing_locker_backup.json",
        mime="application/json",
        use_container_width=True
    )
    
    st.markdown("---")
    uploaded_file = st.file_uploader("📤 Restore from Backup file:", type=["json"])
    if uploaded_file is not None:
        try:
            imported_data = json.load(uploaded_file)
            if all(k in imported_data for k in ["categories", "weather_profiles", "master_items"]):
                st.session_state.categories = imported_data["categories"]
                st.session_state.weather_profiles = imported_data["weather_profiles"]
                st.session_state.master_items = imported_data["master_items"]
                st.session_state.saved_trips = imported_data.get("saved_trips", {})
                st.session_state.deleted_items = imported_data.get("deleted_items", [])
                st.success("Locker state restored successfully!")
                st.rerun()
            else:
                st.error("Invalid configuration schema file structure.")
        except Exception as e:
            st.error(f"Error reading file context: {e}")

with st.sidebar.expander("📦 Gear Item Manager", expanded=False):
    tab_add, tab_edit, tab_delete = st.tabs(["➕ Add Item", "✏️ Edit Tags", "❌ Delete Item"])
    
    with tab_add:
        with st.form("add_item_form", clear_on_submit=True):
            add_name = st.text_input("Item Name:")
            add_cat = st.selectbox("Assign Category:", options=st.session_state.categories)
            add_weather = st.multiselect("Assign Weather Profiles:", options=st.session_state.weather_profiles, default=[st.session_state.weather_profiles[0]])
            if st.form_submit_button("Save New Item") and add_name and add_weather:
                st.session_state.master_items.append({"name": add_name, "category": add_cat, "weather": add_weather})
                st.success(f"Added {add_name} to this session!")
                st.rerun()

    with tab_edit:
        if st.session_state.master_items:
            search_query = st.text_input("🔎 Search existing items:", key="item_search_input").strip().lower()
            all_items_mapped = [{"index": idx, "item": i, "label": f"{i['name']} ({i['category']})"} for idx, i in enumerate(st.session_state.master_items)]
            
            if search_query:
                filtered_search_results = [m for m in all_items_mapped if search_query in m["label"].lower()]
            else:
                filtered_search_results = all_items_mapped
            
            if filtered_search_results:
                search_labels = [m["label"] for m in filtered_search_results]
                selected_label = st.selectbox("Select match to edit:", options=search_labels, key="edit_sel")
                match_obj = filtered_search_results[search_labels.index(selected_label)]
                target = match_obj["item"]
                
                st.markdown("---")
                up_name = st.text_input("Edit Name:", value=target["name"])
                up_cat = st.selectbox("Modify Category:", options=st.session_state.categories, index=st.session_state.categories.index(target["category"]) if target["category"] in st.session_state.categories else 0)
                up_weather = st.multiselect("Modify Weather:", options=st.session_state.weather_profiles, default=[w for w in target["weather"] if w in st.session_state.weather_profiles])
                
                if st.button("Update Specifications"):
                    target.update({"name": up_name, "category": up_cat, "weather": up_weather})
                    st.success("Updated item tags!")
                    st.rerun()
            else:
                st.info("No matching gear found.")

    with tab_delete:
        if st.session_state.master_items:
            del_labels = [f"{i['name']} ({i['category']})" for i in st.session_state.master_items]
            selected_del = st.selectbox("Choose item to delete:", options=del_labels, key="del_sel")
            if st.button("🗑️ Send Item to Trash Bin", use_container_width=True):
                d_idx = del_labels.index(selected_del)
                removed_item = st.session_state.master_items.pop(d_idx)
                if removed_item not in st.session_state.deleted_items: st.session_state.deleted_items.append(removed_item)
                st.success("Moved item to Trash Bin.")
                st.rerun()

with st.sidebar.expander("🛠️ Edit, Reorder & Manage Setup", expanded=False):
    st.subheader("Manage Categories")
    c1, c2 = st.columns([1, 3])
    with c1: cat_em = st.selectbox("Emoji", EMOJIS, key="c_em")
    with c2: cat_nm = st.text_input("Category Name:", key="c_nm")
    if st.button("Add Category") and cat_nm:
        st.session_state.categories.append(f"{cat_em} {cat_nm}")
        st.rerun()

    edit_cat = st.selectbox("Modify Category Structure:", options=["-- Select --"] + st.session_state.categories)
    if edit_cat != "-- Select --":
        if st.button("❌ Delete Category entirely"):
            st.session_state.categories.remove(edit_cat)
            st.session_state.master_items = [i for i in st.session_state.master_items if i["category"] != edit_cat]
            st.rerun()

    st.markdown("---")
    st.subheader("Reorder Activities")
    move_cat = st.selectbox("Choose Category to Shift:", options=st.session_state.categories)
    curr_idx = st.session_state.categories.index(move_cat)
    col_u, col_d = st.columns(2)
    with col_u:
        if st.button("🔼 Move Up") and curr_idx > 0:
            st.session_state.categories.insert(curr_idx - 1, st.session_state.categories.pop(curr_idx))
            st.rerun()
    with col_d:
        if st.button("🔽 Move Down") and curr_idx < len(st.session_state.categories) - 1:
            st.session_state.categories.insert(curr_idx + 1, st.session_state.categories.pop(curr_idx))
            st.rerun()

    st.markdown("---")
    st.subheader("Manage Weather Profiles")
    w_c1, w_c2 = st.columns([1, 3])
    with w_c1: w_em = st.selectbox("Emoji", EMOJIS, key="w_em")
    with w_c2: w_nm = st.text_input("Profile Name:", key="w_nm")
    if st.button("Add Weather Profile") and w_nm:
        st.session_state.weather_profiles.append(f"{w_em} {w_nm}")
        st.rerun()

    edit_w = st.selectbox("Delete Weather Profile:", options=["-- Select --"] + st.session_state.weather_profiles)
    if edit_w != "-- Select --":
        if st.button("❌ Delete Profile entirely"):
            st.session_state.weather_profiles.remove(edit_w)
            for item in st.session_state.master_items:
                if edit_w in item["weather"]:
                    item["weather"].remove(edit_w)
                    if not item["weather"]:
                        item["weather"] = [st.session_state.weather_profiles[0]]
            st.rerun()

with st.sidebar.expander("💾 Save / Load Trip Setups", expanded=False):
    trip_name_input = st.text_input("Name this trip view:")
    load_trip = st.selectbox("Load saved trip:", options=["-- Select --"] + list(st.session_state.saved_trips.keys())) if st.session_state.saved_trips else "-- Select --"

with st.sidebar.expander("🗑️ Item Trash Bin / Recovery", expanded=False):
    if st.session_state.deleted_items:
        trash_opts = [f"{i['name']} ({i['category']})" for i in st.session_state.deleted_items]
        sel_trash = st.multiselect("Items in Trash Bin:", options=trash_opts)
        if st.button("♻️ Restore Selected Gear") and sel_trash:
            for label in sel_trash:
                for item in list(st.session_state.deleted_items):
                    if f"{item['name']} ({item['category']})" == label:
                        st.session_state.master_items.append(item)
                        st.session_state.deleted_items.remove(item)
            st.rerun()
        if st.button("💥 Empty Trash Permanently"):
            st.session_state.deleted_items = []
            st.rerun()
    else: st.info("Trash bin empty.")

# ==================================================
# --- DYNAMIC MATRIX FILTER CALCULATION ENGINE ---
# ==================================================
filtered_items = []
cleaned_selected_categories = [c.strip() for c in selected_categories]
cleaned_selected_weather = [w.strip() for w in selected_weather]

for item in st.session_state.master_items:
    item_cat = item["category"].strip()
    if item_cat in cleaned_selected_categories:
        item_weather = [w.strip() for w in item["weather"]]
        if any(w in cleaned_selected_weather for w in item_weather):
            filtered_items.append(item)

if trip_name_input and st.sidebar.button("Save Current View as Trip"):
    st.session_state.saved_trips[trip_name_input] = {"categories": selected_categories, "weather": selected_weather, "items": [i["name"] for i in filtered_items]}
    st.sidebar.success(f"Trip '{trip_name_input}' cached!"); st.rerun()

# ==========================================
# --- MAIN CANVAS OUTPUT VIEWPORT ---
# ==========================================
main_col, action_col = st.columns([3, 1])

with main_col:
    if not selected_categories:
        st.info("Adjust your trip settings in the sidebar to populate your dynamic packing checklist!")
    else:
        # Custom CSS to force columns to stay horizontal on narrow mobile screens
        st.markdown(
            """
            <style>
            [data-testid="stHorizontalBlock"] > div {
                flex-direction: row !important;
                flex-wrap: nowrap !important;
            }
            [data-testid="stHorizontalBlock"] > div > div {
                min-width: fit-content !important;
                margin-right: 10px;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        
        btn_col1, btn_col2, _ = st.columns([1, 1, 3])
        with btn_col1:
            if st.button("✅ Select All"):
                for item in filtered_items: st.session_state[f"chk_{item['name']}_{item['category'].strip()}"] = True
                st.rerun()
        with btn_col2:
            if st.button("🧹 Clear All"):
                for key in list(st.session_state.keys()):
                    if key.startswith("chk_"): st.session_state[key] = False
                st.rerun()
                
        st.write("💡 *Check items off below to explicitly include them in your final exported file.*")
        current_checked_items = []
        
        for cat in selected_categories:
            cat_strip = cat.strip()
            cat_items = [i for i in filtered_items if i["category"].strip() == cat_strip]
            
            with st.expander(cat_strip, expanded=False):
                if cat_items:
                    for item in cat_items:
                        chk_key = f"chk_{item['name']}_{cat_strip}"
                        if chk_key not in st.session_state: 
                            st.session_state[chk_key] = True
                        
                        if st.checkbox(item['name'], key=chk_key):
                            current_checked_items.append(item)
                else:
                    st.caption("ℹ️ No gear items in this category match your current weather settings.")

with action_col:
    st.subheader("Action Center")
    custom_note_name = st.text_input("Label your exported note file:", value="Trip Packing List")
    safe_filename = "".join([c for c in custom_note_name if c.isalnum() or c in (' ', '_', '-')]).strip().replace(' ', '_') or "my_packing_list"
    
    note_html_data = convert_to_interactive_note(current_checked_items, selected_categories, custom_note_name)
    st.download_button(label="📥 Export Dynamic Checklist Note", data=note_html_data, file_name=f"{safe_filename}.html", mime="text/html", disabled=len(current_checked_items) == 0)
    
    if len(current_checked_items) == 0: st.caption("🎒 Check off items to enable file download.")
    st.markdown("---")
    if st.button("🔄 Restore Missing Default Items"):
        fresh_defaults = get_default_locker_data()
        current_names = {item["name"].lower().strip() for item in st.session_state.master_items}
        restored_count = 0
        for default_item in fresh_defaults["master_items"]:
            if default_item["name"].lower().strip() not in current_names:
                st.session_state.master_items.append(default_item)
                restored_count += 1
        if restored_count > 0:
            st.success(f"Restored {restored_count} default items!"); st.rerun()
        else: st.info("Locker already has all defaults.")