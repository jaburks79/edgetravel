# EdgeTravel — Setup & Deployment Guide

## PART 1: LOCAL DEVELOPMENT SETUP

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- Git

### Step-by-Step Local Setup

```bash
# 1. Navigate to the project folder
cd edgetravel

# 2. Create a virtual environment
python -m venv venv

# 3. Activate it
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Copy the environment file
cp .env.example .env

# 6. Generate a secret key (run this in Python)
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
# Copy the output and paste it as DJANGO_SECRET_KEY in your .env file

# 7. Run database migrations
python manage.py migrate

# 8. Load seed data (destinations, categories)
python manage.py shell < seed_data.py

# 9. Create your admin account
python manage.py createsuperuser
# Follow the prompts to set username, email, password

# 10. Collect static files
python manage.py collectstatic --noinput

# 11. Run the development server
python manage.py runserver
```

### Your site is now live at: http://127.0.0.1:8000

### Admin dashboard: http://127.0.0.1:8000/admin/
Log in with the superuser account you created in step 9.

---

## PART 2: PRODUCTION DEPLOYMENT (Railway)

Railway is the easiest option. Free tier available, paid plans start at $5/month.

### Step 1: Prepare your code

```bash
# Initialize git repo
cd edgetravel
git init
git add .
git commit -m "Initial EdgeTravel build"
```

### Step 2: Push to GitHub

1. Create a new repository on github.com (name it "edgetravel")
2. Don't add README or .gitignore (we already have one)
3. Push your code:

```bash
git remote add origin https://github.com/YOUR_USERNAME/edgetravel.git
git branch -M main
git push -u origin main
```

### Step 3: Deploy on Railway

1. Go to https://railway.app and sign up (GitHub login works)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your edgetravel repository
4. Railway will auto-detect it's a Python/Django project

### Step 4: Add a PostgreSQL database

1. In your Railway project, click "New" → "Database" → "PostgreSQL"
2. Railway automatically sets the DATABASE_URL environment variable

### Step 5: Set environment variables

In Railway dashboard → your service → "Variables" tab, add:

```
DJANGO_SECRET_KEY=<generate a new one with the Python command from Part 1>
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=your-app-name.up.railway.app
```

### Step 6: Deploy

Railway auto-deploys when you push to GitHub. It will:
1. Install requirements.txt
2. Run the `release` command from Procfile (migrations)
3. Start gunicorn from the `web` command

### Step 7: Create admin user on production

In Railway dashboard → your service → "Settings" → open the shell:

```bash
python manage.py createsuperuser
python manage.py shell < seed_data.py
```

### Step 8: Set up a custom domain (optional)

1. Buy a domain (Namecheap, Google Domains, etc.)
2. In Railway → your service → "Settings" → "Domains"
3. Add your custom domain
4. Point your domain's DNS to Railway's provided CNAME

---

## PART 3: ALTERNATIVE DEPLOYMENT (Render)

Render.com is another excellent option with a free tier.

1. Sign up at https://render.com
2. New → Web Service → Connect your GitHub repo
3. Settings:
   - Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - Start Command: `gunicorn edgetravel.wsgi`
4. Add environment variables (same as Railway step 5)
5. Add a PostgreSQL database from Render dashboard
6. Copy the Internal Database URL to your DATABASE_URL env var

---

## PART 4: ONGOING MAINTENANCE

### Making content changes (no code needed)
- Log into /admin/ to add destinations, approve trip reports,
  publish guides, manage forum posts, and moderate users

### Making code changes with Claude
1. Come back to Claude and describe what you want changed
2. Claude will provide updated files
3. Replace the files in your local project
4. Test locally: `python manage.py runserver`
5. Push to GitHub: `git add . && git commit -m "description" && git push`
6. Railway/Render auto-deploys from your push

### Database backups
- Railway: Automatic daily backups on paid plans
- Render: Automatic daily backups on paid plans
- Manual: `python manage.py dumpdata > backup.json`

### Security checklist
- [x] CSRF protection (built into Django)
- [x] SQL injection protection (Django ORM)
- [x] XSS protection (Django template auto-escaping)
- [x] Clickjacking protection (X-Frame-Options)
- [x] Rate limiting on login (custom middleware)
- [x] Password hashing (bcrypt via Django)
- [x] HTTPS enforcement in production
- [x] HSTS headers
- [x] Secure cookies
- [x] Content-Type sniffing prevention
- [ ] Set up email for password resets (configure SMTP in .env)
- [ ] Set up monitoring (Railway/Render have built-in logs)
- [ ] Consider Cloudflare for DDoS protection (free tier available)

---

## PROJECT STRUCTURE REFERENCE

```
edgetravel/
├── manage.py               # Django CLI
├── requirements.txt        # Python dependencies
├── Procfile               # Production server config
├── seed_data.py           # Initial data loader
├── .env.example           # Environment vars template
├── .gitignore
├── edgetravel/            # Core project settings
│   ├── settings.py        # Configuration
│   ├── urls.py            # URL routing
│   ├── views.py           # Home page view
│   ├── middleware.py       # Rate limiting
│   └── wsgi.py            # Production server entry
├── accounts/              # User auth & profiles
│   ├── models.py          # Custom User model
│   ├── views.py           # Login, register, profile
│   ├── forms.py           # Auth forms
│   ├── admin.py           # User admin
│   └── urls.py
├── destinations/          # Destination pages
│   ├── models.py          # Destination + risk ratings
│   ├── views.py           # List & detail views
│   ├── admin.py           # Destination management
│   └── urls.py
├── reports/               # Trip reports + voting
│   ├── models.py          # Reports, votes, comments
│   ├── views.py           # Submit, vote, comment
│   ├── forms.py           # Report forms
│   ├── admin.py           # Moderation tools
│   └── urls.py
├── guides/                # Articles & guides
│   ├── models.py          # Guides + categories
│   ├── views.py           # List & detail + read tracking
│   ├── admin.py           # Guide management
│   └── urls.py
├── forum/                 # Community discussions
│   ├── models.py          # Posts, replies, categories
│   ├── views.py           # Forum CRUD
│   ├── forms.py           # Post & reply forms
│   ├── admin.py           # Forum moderation
│   └── urls.py
├── templates/             # All HTML templates
│   ├── base/              # Layout shell, home, pagination
│   ├── accounts/          # Login, register, profile
│   ├── destinations/      # Destination list & detail
│   ├── reports/           # Report list, detail, submit
│   ├── guides/            # Guide list & detail
│   └── forum/             # Forum home, category, thread
├── static/
│   └── css/
│       └── style.css      # Full dark-theme stylesheet
└── media/                 # User uploads (gitignored)
```
