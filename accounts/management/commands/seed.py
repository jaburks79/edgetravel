from django.core.management.base import BaseCommand
from destinations.models import Destination
from guides.models import GuideCategory
from forum.models import ForumCategory


class Command(BaseCommand):
    help = 'Load initial seed data'

    def handle(self, *args, **options):
        destinations = [
            {"name": "Iraqi Kurdistan", "region": "middle_east", "country_code": "IQ", "risk_level": 3, "emoji_icon": "", "summary": "Ancient citadels, Kurdish hospitality, and relative stability in northern Iraq.", "overview": "Iraqi Kurdistan is the autonomous region in northern Iraq governed by the Kurdistan Regional Government (KRG). It encompasses the provinces of Erbil, Sulaymaniyah, Duhok, and Halabja. Unlike much of Iraq, Kurdistan has been relatively stable since the early 2000s and has developed its own tourism infrastructure.", "safety_brief": "Kurdistan is significantly safer than the rest of Iraq but is not risk-free. Stick to the three main KRG provinces and you will find security comparable to many developing nations.", "visa_info": "Many nationalities receive visa-on-arrival at Erbil and Sulaymaniyah airports. US, UK, EU citizens typically get 30 days.", "transport_info": "Direct flights to Erbil from Istanbul, Amman, Dubai. Internal travel by shared taxi is cheap and efficient.", "money_info": "Iraqi Dinar (IQD) is the currency but US Dollars are widely accepted. Bring USD cash as backup. Budget travelers can get by on $30-50/day.", "connectivity_info": "Local SIM cards available cheaply at the airport. 4G coverage is good in cities. Korek and Asiacell are the main providers.", "tips": "Learn a few Kurdish phrases. Dress modestly. Alcohol is available in Kurdistan. Best time to visit is spring or autumn.", "is_published": True},
            {"name": "Somaliland", "region": "east_africa", "country_code": "SO", "risk_level": 4, "emoji_icon": "", "summary": "Self-declared republic with improving security and a fascinating nomadic culture.", "overview": "Somaliland declared independence from Somalia in 1991 but remains internationally unrecognized. Despite this, it has built a functioning government and maintains significantly better security than southern Somalia.", "safety_brief": "Somaliland is dramatically safer than Somalia proper, but risks remain. The eastern regions near Puntland should be avoided. Hiring a local guide is strongly recommended.", "visa_info": "Visa on arrival available for most nationalities at Hargeisa airport. Typically $60 for 30 days.", "transport_info": "Flights via Ethiopian Airlines or Daallo Airlines from Addis Ababa, Dubai, or Djibouti. Internal travel by 4x4 with a driver.", "money_info": "Somaliland Shilling is official but USD is widely used. Mobile money (Zaad) is ubiquitous. No international ATMs. Bring USD cash.", "connectivity_info": "Mobile coverage is surprisingly good along main routes. Telesom is the main provider.", "tips": "Respect local customs. Women should dress very modestly. Photography can be sensitive. Best time to visit is October-March.", "is_published": True},
            {"name": "Chernobyl Exclusion Zone", "region": "eastern_europe", "country_code": "UA", "risk_level": 2, "emoji_icon": "", "summary": "Guided tours through the frozen Soviet ghost town around the 1986 nuclear disaster site.", "overview": "The Chernobyl Exclusion Zone is a 30-kilometer restricted area around the Chernobyl Nuclear Power Plant in northern Ukraine. The abandoned city of Pripyat is frozen in time.", "safety_brief": "Radiation levels on standard tour routes are low. However, hotspots exist. NEVER touch anything, eat outdoors, or wander off designated paths. Access may be restricted due to the conflict in Ukraine.", "visa_info": "Follow Ukrainian visa rules. Many nationalities get visa-free access for 90 days. You MUST book through a licensed tour operator.", "transport_info": "Tours depart from Kyiv, approximately 2 hours drive north.", "money_info": "Ukrainian Hryvnia (UAH). Tours are typically paid in advance in USD or EUR.", "connectivity_info": "Limited mobile coverage in the zone itself. Your tour guide will have communication equipment.", "tips": "Wear long sleeves and closed shoes. Bring your own food and water. Winter visits offer an especially eerie atmosphere.", "is_published": True},
            {"name": "Afghanistan", "region": "central_asia", "country_code": "AF", "risk_level": 5, "emoji_icon": "", "summary": "The Wakhan Corridor and Bamyan offer stunning landscapes under Taliban governance.", "overview": "Afghanistan under Taliban rule remains one of the most challenging destinations on Earth. A small number of travelers visit the Wakhan Corridor and the Bamyan Valley.", "safety_brief": "EXTREME RISK. All Western governments advise against all travel. Risks include armed conflict, terrorism, kidnapping, landmines, and arbitrary detention.", "visa_info": "Taliban-issued visas are available but the process is opaque and constantly changing.", "transport_info": "Limited commercial flights to Kabul. Internal travel by road is dangerous. 4x4 with driver required.", "money_info": "Afghan Afghani (AFN) and USD. Banking system is largely collapsed. Bring all cash you will need.", "connectivity_info": "Mobile coverage exists in cities but is unreliable. Satellite phone strongly recommended.", "tips": "Only for experienced high-risk travelers. Photography is extremely sensitive. Travel insurance will not cover you here.", "is_published": True},
            {"name": "Colombia (Conflict Zones)", "region": "south_america", "country_code": "CO", "risk_level": 4, "emoji_icon": "", "summary": "Beyond the tourist trail into FARC-affected regions with emerging community tourism.", "overview": "Large swaths of rural Colombia remain affected by decades of armed conflict. Regions like Cauca and Catatumbo are seeing the emergence of community-based tourism initiatives.", "safety_brief": "High risk in rural conflict-affected areas. Active armed groups, coca cultivation regions, landmines, and kidnapping risks remain real.", "visa_info": "US, UK, EU citizens get 90 days visa-free on arrival.", "transport_info": "Internal flights to regional capitals. Local buses or hired transport from there. Roads are often unpaved.", "money_info": "Colombian Peso (COP). ATMs available in regional capitals. Cash only in rural areas. Budget $20-40/day.", "connectivity_info": "Mobile coverage good in towns, nonexistent in deep rural areas. Claro and Movistar are main providers.", "tips": "Learn Spanish. Community tourism projects should be booked through local NGOs. Stay on established paths due to landmines.", "is_published": True},
            {"name": "Pakistan (KPK & Tribal Areas)", "region": "south_asia", "country_code": "PK", "risk_level": 3, "emoji_icon": "", "summary": "Swat Valley and Chitral offer world-class trekking with a complex security backdrop.", "overview": "Pakistan's Khyber Pakhtunkhwa province offers some of the most spectacular mountain scenery on Earth. The Swat Valley has been rebuilt and is actively courting tourists.", "safety_brief": "Security has improved dramatically but risks persist. Swat, Chitral, and the northern areas are significantly safer and see regular tourist traffic.", "visa_info": "Pakistan e-visa available for most nationalities. Tourist visa typically 90 days.", "transport_info": "Flights to Islamabad from major hubs. Internal flights to Gilgit, Chitral, Swat. The Karakoram Highway is an epic overland route.", "money_info": "Pakistani Rupee (PKR). ATMs available in cities. Cash needed in rural areas. Very affordable at $15-25/day.", "connectivity_info": "Good mobile coverage on main routes. Jazz and Zong are popular providers.", "tips": "Hospitality is legendary. Dress conservatively. Women should cover their heads in KPK. Best trekking season is June-September.", "is_published": True},
        ]

        self.stdout.write("Creating destinations...")
        for d in destinations:
            obj, created = Destination.objects.get_or_create(name=d['name'], defaults=d)
            self.stdout.write(f"  {'Created' if created else 'Exists'}: {obj.name}")

        guide_cats = [
            ("Destination Guides", "destination-guides", "In-depth practical guides for specific destinations", 1),
            ("Safety & Security", "safety", "Staying safe in high-risk environments", 2),
            ("Gear & Equipment", "gear", "Essential gear for dangerous travel", 3),
            ("Border Crossings", "borders", "Practical info on specific border crossings", 4),
            ("Practical Tips", "practical", "General practical advice for high-risk travel", 5),
        ]

        self.stdout.write("\nCreating guide categories...")
        for name, slug, desc, order in guide_cats:
            obj, created = GuideCategory.objects.get_or_create(slug=slug, defaults={"name": name, "description": desc, "order": order})
            self.stdout.write(f"  {'Created' if created else 'Exists'}: {name}")

        forum_cats = [
            ("Trip Planning", "trip-planning", "Plan your next trip", 1),
            ("Destination Q&A", "destination-qa", "Questions about specific destinations", 2),
            ("Gear & Safety", "gear-safety", "Equipment and safety protocols", 3),
            ("Visa & Logistics", "visa-logistics", "Visas, borders, transport, paperwork", 4),
            ("Contacts & Fixers", "contacts-fixers", "Finding local guides and fixers", 5),
            ("General Discussion", "general", "Everything else", 6),
        ]

        self.stdout.write("\nCreating forum categories...")
        for name, slug, desc, order in forum_cats:
            obj, created = ForumCategory.objects.get_or_create(slug=slug, defaults={"name": name, "description": desc, "order": order})
            self.stdout.write(f"  {'Created' if created else 'Exists'}: {name}")


ffrom accounts.models import User
        admin_user = User.objects.filter(username='admin').first()
        if admin_user:
            admin_user.set_password('EdgeTravel2026!')
            admin_user.is_superuser = True
            admin_user.is_staff = True
            admin_user.save()
            self.stdout.write("  Reset admin password")
        else:
            User.objects.create_superuser('admin', 'admin@edgetravel.com', 'EdgeTravel2026!')
            self.stdout.write("  Created admin user")

            
        self.stdout.write(self.style.SUCCESS("\nSeed data complete!"))


