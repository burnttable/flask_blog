# Flask Blog Service System

A full-featured blog service system built with Flask, SQLite, and Jinja2 templates.

## Features

- User authentication (registration, login, logout)
- Blog post CRUD (create, edit, publish, modify, delete)
- Multiple page themes (light mode and dark mode)
- Blog interactions (likes, dislikes, comments)
- Blog search functionality

## Quick Start

### Windows

1. Create a virtual environment:
```cmd
python -m venv venv
venv\Scripts\activate
```

2. Install dependencies:
```cmd
pip install -r requirements.txt
```

3. Run the application:
```cmd
python app.py
# OR use the batch script
run.bat
```

4. Open your browser and navigate to `http://localhost:5000`

### Quick Setup Verification

After following the steps above, you should see:
- Flask starting up on `http://127.0.0.1:5000`
- "Running on all addresses (0.0.0.0)" message
- No database errors (tables are auto-created on first run)

If you see any errors, check the **Troubleshooting** section below.

### Linux/macOS

1. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
# OR use the shell script
chmod +x run.sh
./run.sh
```

4. Open your browser and navigate to `http://localhost:5000`

## Configuration

1. **Copy the example environment file:**
   ```bash
   # Windows
   copy .env.example .env

   # Linux/Mac
   cp .env.example .env
   ```

2. **Environment variables in `.env`:**
   - `SECRET_KEY`: Secret key for session management (change in production!)
   - `DATABASE_URL`: Optional - SQLite database path. If not set, the app will use the system temp directory (portable default).

3. **Database Location Options:**
   - **Default (Recommended)**: Leave `DATABASE_URL` commented out. The app will use the temp directory automatically.
   - **Custom Location**: Uncomment `DATABASE_URL` and set an absolute path:
     - Windows: `sqlite:///C:/path/to/project/blog.db`
     - Linux/Mac: `sqlite:////home/username/project/blog.db` (4 slashes for absolute paths)

## Database Setup

The database is automatically created on first run. All tables (users, posts, comments, likes, preferences) are initialized automatically.

## Project Structure

```
flask_blog/
├── app.py                  # Main Flask application
├── config.py               # App configuration
├── requirements.txt        # Dependencies
├── .env                    # Environment variables (not in git)
├── .env.example           # Example environment file
├── .gitignore             # Git ignore file
├── run.bat                # Windows startup script
├── run.sh                 # Unix/Linux/Mac startup script
├── README.md              # This file
│
├── models/                # Database models
│   ├── __init__.py
│   ├── user.py            # User model
│   ├── post.py            # Post model
│   ├── comment.py         # Comment model
│   ├── like.py            # Like/Dislike model
│   └── preference.py      # Theme preferences
│
├── routes/                # Route blueprints
│   ├── __init__.py
│   ├── auth.py            # Auth routes (login, register, logout)
│   ├── posts.py           # Post CRUD routes
│   ├── main.py            # Home/main routes
│   └── api.py             # AJAX API (likes, comments)
│
├── templates/             # Jinja2 templates
│   ├── base.html          # Master template with theme support
│   ├── index.html         # Home page
│   ├── auth/              # Auth templates
│   │   ├── login.html
│   │   └── register.html
│   ├── posts/             # Post templates
│   │   ├── create.html
│   │   ├── edit.html
│   │   ├── view.html
│   │   └── search.html
│   ├── components/        # Reusable components
│   │   ├── header.html
│   │   ├── footer.html
│   │   ├── theme_toggle.html
│   │   └── post_card.html
│   └── errors/            # Error pages
│       ├── 404.html
│       └── 500.html
│
├── static/                # Static files
│   ├── css/
│   │   ├── styles.css         # Main styles
│   │   ├── theme-light.css    # Light theme
│   │   └── theme-dark.css     # Dark theme
│   ├── js/
│   │   ├── theme.js           # Theme toggle
│   │   ├── post-interactions.js  # Like/dislike handlers
│   │   └── search.js          # Search functionality
│   └── images/
│
└── utils/                 # Utilities
    ├── __init__.py
    ├── decorators.py      # login_required decorator
    └── helpers.py         # Helper functions
```

## API Endpoints

### Authentication
- `GET/POST /auth/register` - Register new user
- `GET/POST /auth/login` - Login user
- `GET /auth/logout` - Logout user

### Posts
- `GET /` - Home page (post list)
- `GET /posts/create` - Show create form
- `POST /posts/create` - Create post
- `GET /posts/<id>` - View single post
- `GET /posts/<id>/edit` - Show edit form
- `POST /posts/<id>/edit` - Update post
- `POST /posts/<id>/publish` - Publish draft
- `POST /posts/<id>/delete` - Delete post
- `GET /posts/my` - User's posts

### AJAX API
- `POST /api/posts/<id>/like` - Like post
- `POST /api/posts/<id>/dislike` - Dislike post
- `POST /api/posts/<id>/comments` - Add comment
- `GET /api/posts/<id>/comments` - Get comments
- `DELETE /api/comments/<id>` - Delete comment
- `POST /api/search` - Search posts

## Deployment

### Deploy to Render.com (Recommended)

1. **Prepare for deployment:**
   - Copy `.env.example` to `.env` if needed
   - Ensure `.env` file has a strong `SECRET_KEY`
   - For Render/Heroku, the platform will set `DATABASE_URL` automatically

2. **Push to GitHub:**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-github-repo>
git push -u origin main
```

3. **Deploy on Render:**
   - Create account at [render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Render auto-detects Flask
   - Set environment variables:
     - `SECRET_KEY`: Generate a strong random key
     - `FLASK_ENV`: `production`
   - Click "Deploy"

4. **Get your URL:** Render will provide a URL like `https://flask-blog.onrender.com`

### Configure Cloudflare DNS (Optional)

For a custom domain with Cloudflare CDN:

1. Add your domain to Cloudflare
2. Create CNAME record: `blog → <your-render-app>.onrender.com` (Proxied - orange cloud)
3. Enable "Always Use HTTPS" in Cloudflare SSL/TLS settings
4. Enable Cloudflare caching and security features

### Alternative Deployment Options

The application can also be deployed to:
- **Heroku**: Using the Procfile (create one with `web: python app.py`)
- **Railway**: Auto-detects Flask from requirements.txt
- **PythonAnywhere**: Upload code and configure virtualenv
- **VPS/Dedicated Server**: Use Gunicorn as WSGI server

## Security Notes

1. **Change the SECRET_KEY** in `.env` before deploying to production
2. The application uses:
   - CSRF protection on all forms
   - Password hashing with pbkdf2_sha256
   - SQL injection prevention (SQLAlchemy ORM)
   - XSS prevention (Jinja2 auto-escaping)
   - Secure, HttpOnly session cookies

## Troubleshooting

### Database Issues

If you get "unable to open database file" error:

1. **Easiest fix**: Comment out or remove `DATABASE_URL` from `.env` - the app will use the temp directory
2. **Custom path**: Set `DATABASE_URL` in `.env` with absolute path:
   - Windows: `sqlite:///C:/Users/YourName/flask_blog/blog.db`
   - Linux/Mac: `sqlite:////home/username/flask_blog/blog.db` (4 slashes)
3. Ensure the directory has write permissions

### Port Already in Use

If port 5000 is already in use, modify `app.py`:
```python
app.run(host='0.0.0.0', port=8000, debug=True)  # Use port 8000
```

## Development

### Adding New Features

1. **New Model**: Add to `models/` directory
2. **New Routes**: Add to `routes/` directory
3. **New Templates**: Add to `templates/` directory
4. **New Static Files**: Add to `static/` directory

### Running Tests

Tests can be added using pytest. Create a `tests/` directory and add test files.

## License

MIT License - feel free to use this project for learning or production!

## Support

For issues or questions, please check the code comments or create an issue in your repository.
