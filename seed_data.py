"""
Seed script — Run after migrations to populate initial data.
Usage: python manage.py shell < seed_data.py
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edgetravel.settings')
django.setup()

from destinations.models import Destination
from guides.models import GuideCategory
from forum.models import ForumCategory

# --- Destinations ---
destinations = [
    {
        "name": "Iraqi Kurdistan",
        "region": "middle_east",
        "country_code": "IQ",
        "risk_level": 3,
        "emoji_icon": "🏔️",
        "summary": "Ancient citadels, Kurdish hospitality, and relative stability in northern Iraq.",
        "overview": "Iraqi Kurdistan is the autonomous region in northern Iraq governed by the Kurdistan Regional Government (KRG). It encompasses the provinces of Erbil, Sulaymaniyah, Duhok, and Halabja. Unlike much of Iraq, Kurdistan has been relatively stable since the early 2000s and has developed its own tourism infrastructure.\n\nThe region offers ancient citadels (Erbil Citadel is one of the oldest continuously inhabited settlements on Earth), dramatic mountain scenery, bustling bazaars, and some of the most hospitable people you'll meet anywhere. It's a fascinating destination that challenges every preconception most Westerners have about Iraq.",
        "safety_brief": "Kurdistan is significantly safer than the rest of Iraq but is not risk-free. The main concerns are proximity to active conflict zones to the south and west, occasional cross-border Turkish military operations targeting PKK positions in the mountains, and ISIS sleeper cells in disputed territories near Kirkuk.\n\nStick to the three main KRG provinces and you'll find security comparable to many developing nations. Avoid the disputed territories south of the KRG boundary line. Travel to Kirkuk is possible but requires caution.",
        "visa_info": "Many nationalities receive visa-on-arrival at Erbil (EBL) and Sulaymaniyah (ISU) airports. This is a KRG visa and does NOT permit travel to federal Iraq. US, UK, EU citizens typically get 30 days. Check current requirements before travel as policies change frequently.",
        "transport_info": "Direct flights to Erbil from Istanbul, Amman, Dubai, and several European cities. Internal travel by shared taxi is cheap and efficient. Roads between major cities are excellent. Hiring a driver for rural/mountain areas is recommended.",
        "money_info": "Iraqi Dinar (IQD) is the currency but US Dollars are widely accepted in tourist areas. ATMs exist in Erbil and Sulaymaniyah but can be unreliable. Bring US cash as backup. Budget travelers can get by on $30-50/day.",
        "connectivity_info": "Local SIM cards available cheaply at the airport. 4G coverage is good in cities, spotty in mountains. Korek and Asiacell are the main providers. Wi-Fi available in most hotels and cafes.",
        "tips": "Learn a few Kurdish phrases — it goes a long way. Dress modestly, especially in smaller towns. Alcohol is available and socially acceptable in Kurdistan, unlike much of Iraq. The best time to visit is spring (March-May) or autumn (September-November).",
        "is_published": True,
    },
    {
        "name": "Somaliland",
        "region": "east_africa",
        "country_code": "SO",
        "risk_level": 4,
        "emoji_icon": "🌍",
        "summary": "Self-declared republic with improving security and a fascinating nomadic culture.",
        "overview": "Somaliland declared independence from Somalia in 1991 but remains internationally unrecognized. Despite this, it has built a functioning government, held democratic elections, and maintains significantly better security than southern Somalia.\n\nThe country offers ancient cave paintings at Laas Geel, the bustling port city of Berbera with pristine beaches, and a window into traditional Somali nomadic culture that few outsiders have experienced.",
        "safety_brief": "Somaliland is dramatically safer than Somalia proper, but risks remain. The eastern regions near Puntland are contested and should be avoided. Al-Shabaab has limited presence but cannot be ruled out entirely. Petty crime is low. Hiring a local guide/fixer is strongly recommended and may be required by authorities.\n\nThe main practical risks are poor roads, limited medical facilities, and extreme heat.",
        "visa_info": "Visa on arrival available for most nationalities at Hargeisa airport (HGA). Typically $60 for 30 days. You may need a letter of invitation — check current requirements. There is no Somaliland embassy in most countries as it is unrecognized.",
        "transport_info": "Flights via Ethiopian Airlines, Daallo Airlines, or charter from Addis Ababa, Dubai, or Djibouti. Internal travel by 4x4 with a driver. Roads are rough outside Hargeisa-Berbera highway.",
        "money_info": "Somaliland Shilling is the official currency but USD is widely used. Mobile money (Zaad) is ubiquitous — more common than cash. No international ATMs. Bring USD cash.",
        "connectivity_info": "Mobile coverage is surprisingly good along main routes. Telesom is the main provider. Data is cheap. Wi-Fi available in Hargeisa hotels.",
        "tips": "Respect local customs — Somaliland is conservative and Islamic. Women should dress very modestly. Chewing khat is a major social activity. Photography can be sensitive — always ask permission. The best time to visit is the cooler dry season (October-March).",
        "is_published": True,
    },
    {
        "name": "Chernobyl Exclusion Zone",
        "region": "eastern_europe",
        "country_code": "UA",
        "risk_level": 2,
        "emoji_icon": "☢️",
        "summary": "Guided tours through the frozen Soviet ghost town around the 1986 nuclear disaster site.",
        "overview": "The Chernobyl Exclusion Zone is a 30-kilometer restricted area around the Chernobyl Nuclear Power Plant in northern Ukraine. The 1986 disaster was the worst nuclear accident in history, and the zone remains one of the most radioactively contaminated areas on Earth.\n\nThe abandoned city of Pripyat, once home to 49,000 people, is frozen in time — a Soviet ghost town where nature is slowly reclaiming apartment blocks, schools, and an amusement park that never opened. Licensed tour operators run day trips and multi-day expeditions from Kyiv.",
        "safety_brief": "Radiation levels on standard tour routes are low and comparable to a long-haul flight. However, hotspots exist and certain areas remain dangerously contaminated. NEVER touch anything, eat outdoors, or wander off designated paths.\n\nNote: Access may be restricted due to the ongoing conflict in Ukraine. Check current conditions before planning.",
        "visa_info": "Tourists visit as part of Ukraine and follow Ukrainian visa rules. Many nationalities get visa-free access for 90 days. You MUST book through a licensed tour operator to enter the zone — independent access is illegal.",
        "transport_info": "Tours depart from Kyiv, approximately 2 hours drive north. All transport within the zone is provided by your tour operator.",
        "money_info": "Ukrainian Hryvnia (UAH). Tours are typically paid in advance in USD or EUR. ATMs widely available in Kyiv.",
        "connectivity_info": "Limited mobile coverage in the zone itself. Some areas have signal, others don't. Your tour guide will have communication equipment.",
        "tips": "Wear long sleeves and closed shoes (required). Bring your own food and water. Winter visits offer an especially eerie atmosphere with fewer tourists. Book multi-day tours for deeper exploration beyond the standard stops.",
        "is_published": True,
    },
    {
        "name": "Afghanistan",
        "region": "central_asia",
        "country_code": "AF",
        "risk_level": 5,
        "emoji_icon": "⛰️",
        "summary": "The Wakhan Corridor and Bamyan offer stunning landscapes under Taliban governance.",
        "overview": "Afghanistan under Taliban rule (since August 2021) remains one of the most challenging destinations on Earth. However, a small number of travelers continue to visit, particularly the Wakhan Corridor in the northeast and the Bamyan Valley in central Afghanistan.\n\nThe country offers extraordinary landscapes — the Hindu Kush mountains, the ancient Buddhas of Bamyan (destroyed by the Taliban in 2001 but the niches remain), and the remote Wakhan Corridor bordering Tajikistan, Pakistan, and China. The cultural experience is unlike anything else.",
        "safety_brief": "EXTREME RISK. All Western governments advise against all travel. Risks include armed conflict, terrorism, kidnapping (particularly of Westerners), landmines, and arbitrary detention by Taliban authorities. Women face severe restrictions on movement and dress.\n\nIF you choose to go despite these warnings: travel only with an experienced local operator, keep an extremely low profile, register with your embassy, and carry a satellite communication device. The Wakhan Corridor is considered the 'safest' region but this is relative.",
        "visa_info": "Taliban-issued visas are available but the process is opaque and constantly changing. Some travelers obtain them through operators in Kabul. Your home country likely has no diplomatic presence in Afghanistan to assist you if things go wrong.",
        "transport_info": "Limited commercial flights to Kabul (Kam Air, Ariana Afghan). Internal travel by road is dangerous in many areas. Flights to Bamyan when available. 4x4 with driver required.",
        "money_info": "Afghan Afghani (AFN) and USD. Banking system is largely collapsed. Bring all cash you'll need. Mobile money (M-Paisa) exists but limited.",
        "connectivity_info": "Mobile coverage exists in cities but is unreliable. Almost nonexistent in rural areas. Satellite phone strongly recommended.",
        "tips": "This destination is only for experienced high-risk travelers. Women should expect severe restrictions. Photography is extremely sensitive — never photograph military checkpoints or Taliban personnel. Travel insurance will not cover you here. Tell people where you are going and check in regularly.",
        "is_published": True,
    },
    {
        "name": "Colombia (Conflict Zones)",
        "region": "south_america",
        "country_code": "CO",
        "risk_level": 4,
        "emoji_icon": "🌿",
        "summary": "Beyond the tourist trail into FARC-affected regions with emerging community tourism.",
        "overview": "While cities like Bogota, Medellin, and Cartagena are well-established tourist destinations, large swaths of rural Colombia remain affected by decades of armed conflict between the government, FARC dissidents, ELN guerrillas, and narco-trafficking groups.\n\nRegions like Cauca, Catatumbo, Choco, and parts of Putumayo are seeing the emergence of community-based tourism initiatives, often run by former conflict-affected communities. These offer a raw and authentic experience of Colombia far from the tourist trail.",
        "safety_brief": "High risk in rural conflict-affected areas. Active armed groups, coca cultivation regions, landmines in remote areas, and kidnapping risks remain real. However, security varies enormously by specific location.\n\nAlways consult local contacts before traveling to rural areas. Avoid overland travel at night. Stick to community tourism programs that have established security protocols with local communities.",
        "visa_info": "US, UK, EU citizens get 90 days visa-free on arrival. Standard Colombian entry applies — the risk is internal, not at the border.",
        "transport_info": "Internal flights to regional capitals (Popayan, Quibdo, Pasto). From there, local buses or hired transport. Roads in conflict zones are often unpaved and can be blocked.",
        "money_info": "Colombian Peso (COP). ATMs available in regional capitals. Cash only in rural areas. Budget $20-40/day in rural regions.",
        "connectivity_info": "Mobile coverage good in towns, nonexistent in deep rural areas. Claro and Movistar are main providers.",
        "tips": "Learn Spanish — English is not spoken in these regions. Community tourism projects should be booked through local NGOs or verified operators. Coca-growing regions are not safe for casual tourists. Colombia has the second-highest number of landmine victims after Afghanistan — stay on established paths.",
        "is_published": True,
    },
    {
        "name": "Pakistan (KPK & Tribal Areas)",
        "region": "south_asia",
        "country_code": "PK",
        "risk_level": 3,
        "emoji_icon": "🏔️",
        "summary": "Swat Valley and Chitral offer world-class trekking with a complex security backdrop.",
        "overview": "Pakistan's Khyber Pakhtunkhwa province and the former tribal areas offer some of the most spectacular mountain scenery on Earth. The Swat Valley, once devastated by Taliban occupation (2007-2009), has been rebuilt and is actively courting tourists. Chitral and the Kalash Valleys provide access to one of the world's most unique indigenous cultures.\n\nFurther north, the Karakoram Highway and the approach to K2 base camp draw serious mountaineers and adventure travelers. Pakistan's tourism potential is enormous and largely untapped.",
        "safety_brief": "Security has improved dramatically since the 2010s military operations, but risks persist. The former FATA (Federally Administered Tribal Areas) require special permits and have restricted access. Occasional militant attacks occur. Sectarian violence affects some areas.\n\nSwat, Chitral, and the northern areas (Gilgit-Baltistan, Hunza) are significantly safer and see regular tourist traffic. A No Objection Certificate (NOC) may be required for certain areas.",
        "visa_info": "Pakistan e-visa available for most nationalities. Tourist visa typically 90 days. The process has been simplified considerably in recent years. Some nationalities can get visa on arrival.",
        "transport_info": "Flights to Islamabad (ISB) from major hubs. Internal flights to Gilgit, Chitral, Swat (weather dependent — mountain flights cancel frequently). The Karakoram Highway is an epic overland route. Local buses and hired vehicles available.",
        "money_info": "Pakistani Rupee (PKR). ATMs available in cities and larger towns. Cash needed in rural areas. Very affordable — budget travelers can manage on $15-25/day.",
        "connectivity_info": "Good mobile coverage on main routes. Jazz and Zong are popular providers. Tourist SIM registration can be bureaucratic — bring your passport.",
        "tips": "Pakistan's hospitality is legendary — expect to be invited for tea constantly. Dress conservatively everywhere. Women should cover their heads in KPK and tribal areas. The best trekking season is June-September. Winter closes many mountain passes. Security situation can change quickly — monitor local news.",
        "is_published": True,
    },
]

for d in destinations:
    obj, created = Destination.objects.get_or_create(
        name=d['name'],
        defaults=d
    )
    status = "Created" if created else "Already exists"
    print(f"  {status}: {obj.name}")

# --- Guide Categories ---
guide_cats = [
    ("Destination Guides", "destination-guides", "In-depth practical guides for specific destinations", 1),
    ("Safety & Security", "safety", "Staying safe in high-risk environments", 2),
    ("Gear & Equipment", "gear", "Essential gear for dangerous travel", 3),
    ("Border Crossings", "borders", "Practical info on specific border crossings", 4),
    ("Practical Tips", "practical", "General practical advice for high-risk travel", 5),
]

print("\nGuide Categories:")
for name, slug, desc, order in guide_cats:
    obj, created = GuideCategory.objects.get_or_create(
        slug=slug,
        defaults={"name": name, "description": desc, "order": order}
    )
    print(f"  {'Created' if created else 'Exists'}: {name}")

# --- Forum Categories ---
forum_cats = [
    ("Trip Planning", "trip-planning", "Plan your next trip — ask questions, get advice", "🗺️", 1),
    ("Destination Q&A", "destination-qa", "Questions about specific destinations", "❓", 2),
    ("Gear & Safety", "gear-safety", "Equipment, safety protocols, and preparation", "🎒", 3),
    ("Visa & Logistics", "visa-logistics", "Visas, border crossings, transport, and paperwork", "📋", 4),
    ("Contacts & Fixers", "contacts-fixers", "Finding and vetting local guides and fixers", "🤝", 5),
    ("General Discussion", "general", "Everything else — ethics, news, stories", "💬", 6),
]

print("\nForum Categories:")
for name, slug, desc, icon, order in forum_cats:
    obj, created = ForumCategory.objects.get_or_create(
        slug=slug,
        defaults={"name": name, "description": desc, "icon": icon, "order": order}
    )
    print(f"  {'Created' if created else 'Exists'}: {name}")

print("\n✅ Seed data complete!")
