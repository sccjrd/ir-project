import json
import random
from datetime import datetime, timedelta

# Generate IKEA Hackers data (Blog-style, detailed)
def generate_ikea_hackers_data(num_items=150):
    categories = [
        'kitchen', 'bedroom', 'living-room', 'bathroom', 'children',
        'storage', 'lighting', 'outdoor', 'workspace', 'dining'
    ]
    
    ikea_products = [
        'KALLAX', 'BILLY', 'LACK', 'HEMNES', 'MALM', 'PAX', 'EKET',
        'IVAR', 'BESTA', 'STUVA', 'ALEX', 'NORDLI', 'BRIMNES',
        'TROFAST', 'TARVA', 'FLISAT', 'MICKE', 'RAST'
    ]
    
    hack_types = [
        'Storage Solution', 'Room Divider', 'Custom Furniture',
        'Kids Play Area', 'Hidden Storage', 'Media Center',
        'Wardrobe System', 'Desk Setup', 'Nightstand', 'Coffee Table',
        'Bookshelf', 'Entryway Organizer', 'Closet System'
    ]
    
    authors = ['Sarah Johnson', 'Mike Chen', 'Emma Williams', 'David Brown',
               'Lisa Anderson', 'Tom Wilson', 'Rachel Green', 'Alex Martinez']
    
    data = []
    
    for i in range(num_items):
        product = random.choice(ikea_products)
        hack_type = random.choice(hack_types)
        category = random.choice(categories)
        author = random.choice(authors)
        
        # Generate date within last 2 years
        days_ago = random.randint(0, 730)
        date = (datetime.now() - timedelta(days=days_ago)).isoformat()
        
        title = f"{hack_type} using IKEA {product}"
        
        content = f"This DIY project transforms the IKEA {product} into a functional {hack_type.lower()}. "
        content += f"The hack involves simple modifications that anyone can do at home. "
        content += f"Materials needed include the {product} unit, some basic tools, and creative thinking. "
        content += f"The finished product fits perfectly in any {category.replace('-', ' ')} and adds both style and functionality. "
        content += f"This budget-friendly solution costs a fraction of store-bought alternatives while providing exactly what you need. "
        content += f"The step-by-step process takes about 2-4 hours to complete and requires minimal DIY experience."
        
        item = {
            'title': title,
            'content': content,
            'author': author,
            'date': date,
            'url': f'https://ikeahackers.net/2024/{i+1000}/{title.lower().replace(" ", "-")}.html',
            'categories': [category, 'ikea-hacks'],
            'tags': [product.lower(), 'diy', 'hack', category],
            'image_url': f'https://ikeahackers.net/images/{product.lower()}-hack-{i}.jpg',
            'excerpt': content[:200] + '...'
        }
        data.append(item)
    
    return data


# Generate Tosize data (Project-based, community-driven)
def generate_tosize_data(num_items=100):
    project_types = [
        'Furniture Makeover', 'Space Optimization', 'Custom Build',
        'Upcycling Project', 'Organization Hack', 'Decorative Upgrade'
    ]
    
    ikea_items = [
        'KALLAX shelf', 'BILLY bookcase', 'LACK table', 'PAX wardrobe',
        'MALM dresser', 'EKET cabinet', 'BESTA unit', 'HEMNES furniture',
        'STUVA storage', 'IVAR shelving', 'ALEX drawers', 'TARVA dresser'
    ]
    
    rooms = [
        'living room', 'bedroom', 'kitchen', 'home office',
        'kids room', 'bathroom', 'entryway', 'dining room',
        'craft room', 'laundry room'
    ]
    
    data = []
    
    for i in range(num_items):
        project = random.choice(project_types)
        item = random.choice(ikea_items)
        room = random.choice(rooms)
        
        days_ago = random.randint(0, 730)
        date = (datetime.now() - timedelta(days=days_ago)).isoformat()
        
        title = f"{project}: Transforming {item} for {room}"
        
        content = f"A creative {project.lower()} that reimagines the IKEA {item}. "
        content += f"Perfect for maximizing space in your {room}, this project combines functionality with aesthetic appeal. "
        content += f"The transformation includes custom painting, additional hardware, and clever positioning. "
        content += f"Total cost remains under budget while achieving a high-end look. "
        content += f"This community-shared project has been replicated by hundreds of DIY enthusiasts worldwide. "
        content += f"Difficulty level is moderate, suitable for weekend warriors with basic tools."
        
        item = {
            'title': title,
            'content': content,
            'author': 'Tosize Community',
            'date': date,
            'url': f'https://www.tosize.it/en-it/diy/projects/ikea-hack-{i+2000}',
            'categories': [room.replace(' ', '-'), 'diy-projects'],
            'tags': ['ikea', 'diy', project.lower().replace(' ', '-')],
            'image_url': f'https://www.tosize.it/images/project-{i}.jpg',
            'excerpt': content[:200] + '...'
        }
        data.append(item)
    
    return data


# Generate Apartment Therapy data (Style-focused, home decor)
def generate_apartment_therapy_data(num_items=80):
    style_themes = [
        'Modern Minimalist', 'Scandinavian Chic', 'Industrial Style',
        'Bohemian Decor', 'Mid-Century Modern', 'Farmhouse Style',
        'Contemporary Design', 'Eclectic Mix', 'Rustic Charm'
    ]
    
    furniture_pieces = [
        'shelving unit', 'dresser', 'nightstand', 'coffee table',
        'bookcase', 'media console', 'storage bench', 'side table',
        'desk', 'cabinet', 'wardrobe', 'console table'
    ]
    
    data = []
    
    for i in range(num_items):
        style = random.choice(style_themes)
        furniture = random.choice(furniture_pieces)
        
        days_ago = random.randint(0, 730)
        date = (datetime.now() - timedelta(days=days_ago)).isoformat()
        
        title = f"How to Create a {style} {furniture.title()} with IKEA"
        
        content = f"Discover how to achieve a stunning {style.lower()} look using affordable IKEA pieces. "
        content += f"This stylish {furniture} hack elevates basic IKEA furniture into something special. "
        content += f"The secret lies in thoughtful styling, strategic paint choices, and clever hardware upgrades. "
        content += f"Interior designers love this approach for achieving high-end aesthetics on a budget. "
        content += f"The transformation process is straightforward and yields impressive results that feel custom-made. "
        content += f"This IKEA hack has been featured in multiple home tours and continues to inspire homeowners. "
        content += f"Materials are readily available at hardware stores, and the project completes in a single afternoon."
        
        item = {
            'title': title,
            'content': content,
            'author': 'Apartment Therapy',
            'date': date,
            'url': f'https://www.apartmenttherapy.com/ikea-hack-{furniture.replace(" ", "-")}-{i+3000}',
            'categories': ['IKEA', 'Home Decor', style.replace(' ', '-')],
            'tags': ['ikea', 'hack', 'diy', 'home-decor', furniture.replace(' ', '-')],
            'image_url': f'https://www.apartmenttherapy.com/images/hack-{i}.jpg',
            'excerpt': content[:200] + '...'
        }
        data.append(item)
    
    return data


# Generate all three datasets
print("Generating IKEA Hackers data...")
ikea_hackers = generate_ikea_hackers_data(150)

print("Generating Tosize data...")
tosize = generate_tosize_data(100)

print("Generating Apartment Therapy data...")
apartment_therapy = generate_apartment_therapy_data(80)

# Save to JSON files
with open('ikea_hacks.json', 'w', encoding='utf-8') as f:
    json.dump(ikea_hackers, f, indent=4, ensure_ascii=False)

with open('tosize_hacks.json', 'w', encoding='utf-8') as f:
    json.dump(tosize, f, indent=4, ensure_ascii=False)

with open('apartmenttherapy_hacks.json', 'w', encoding='utf-8') as f:
    json.dump(apartment_therapy, f, indent=4, ensure_ascii=False)

print(f"\n✅ Generated {len(ikea_hackers)} IKEA Hackers entries")
print(f"✅ Generated {len(tosize)} Tosize entries")
print(f"✅ Generated {len(apartment_therapy)} Apartment Therapy entries")
print(f"\nTotal: {len(ikea_hackers) + len(tosize) + len(apartment_therapy)} items")
print("\nFiles created:")
print("- ikea_hacks.json")
print("- tosize_hacks.json")
print("- apartmenttherapy_hacks.json")