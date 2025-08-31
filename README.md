# Mount Zion Victory Church Website

A modern, responsive church website built with Python Flask backend and HTML/CSS/JavaScript frontend, featuring sermon archives, daily inspiration, church events, and branch information.

## 🚀 Features

### Core Functionality
- **User Authentication**: Secure login system with session management
- **Sermon Archives**: Browse and search through sermon collections
- **Daily Inspiration**: Biblical quotes and motivational content
- **Church Events**: Event calendar with grid and calendar views
- **Branch Information**: Details about different church locations
- **Responsive Design**: Mobile-friendly interface

### Technical Features
- **Search & Filter**: Find content quickly across all sections
- **Interactive Elements**: Smooth animations, parallax effects, and hover interactions
- **Flash Messages**: User feedback and notifications
- **Pagination**: Efficient content browsing
- **Form Validation**: Client and server-side validation

## 🛠️ Tech Stack

### Backend
- **Python 3.8+**: Core programming language
- **Flask 2.3.3**: Web framework for routing and server logic
- **SQLite**: Lightweight, file-based database
- **Werkzeug**: WSGI utilities and security features

### Frontend
- **HTML5**: Semantic markup structure
- **CSS3**: Modern styling with CSS Grid, Flexbox, and animations
- **JavaScript (ES6+)**: Interactive functionality and DOM manipulation
- **Jinja2**: Server-side templating engine

### Database
- **SQLite**: No server setup required, perfect for development and small deployments

## 📁 Project Structure

```
church_website/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── database/             # Database files
│   └── database.db      # SQLite database
├── static/               # Static assets
│   ├── css/             # Stylesheets
│   │   ├── style.css    # Main styles
│   │   └── responsive.css # Responsive design
│   ├── js/              # JavaScript files
│   │   ├── main.js      # General functionality
│   │   └── auth.js      # Authentication logic
│   └── images/          # Image assets
├── templates/            # HTML templates
│   ├── base.html        # Base template
│   ├── index.html       # Homepage
│   ├── login.html       # Login page
│   ├── sermons.html     # Sermon archives
│   ├── events.html      # Church events
│   ├── branches.html    # Branch information
│   └── inspiration.html # Daily inspiration
└── uploads/             # File uploads (future use)
```

## 🗄️ Database Schema

### Tables
- **users**: User accounts and authentication
- **sermons**: Sermon metadata and content
- **events**: Church events and schedules
- **branches**: Church location information
- **daily_inspiration**: Biblical quotes and motivational content

### Default Data
- Admin user: `admin` / `admin123`
- Sample sermons, events, branches, and inspiration content

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the project**
   ```bash
   cd church_website
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the website**
   - Open your browser and go to `http://localhost:5000`
   - Login with default credentials: `admin` / `admin123`

## 🔐 Security Features

- **Password Hashing**: SHA256 encryption for user passwords
- **Session Management**: Secure session handling with Flask
- **Input Validation**: Client and server-side form validation
- **SQL Injection Protection**: Parameterized queries with SQLite

## 🎨 Customization

### Styling
- Modify `static/css/style.css` for main styles
- Edit `static/css/responsive.css` for mobile responsiveness
- Update color schemes and typography in CSS variables

### Content
- Edit templates in the `templates/` directory
- Modify database content through the Flask app
- Add new routes and functionality in `app.py`

### JavaScript
- Enhance interactivity in `static/js/main.js`
- Modify authentication logic in `static/js/auth.js`
- Add new features and animations

## 📱 Responsive Design

The website is fully responsive with breakpoints for:
- **Desktop**: 1200px and above
- **Tablet**: 768px to 1199px
- **Mobile**: Below 768px

## 🔧 Development Phases

### Phase 1: Core Structure ✅
- Basic Flask application setup
- Database initialization and schema
- User authentication system
- Basic templates and styling

### Phase 2: Content Management ✅
- Sermon archives with search/filter
- Event management and calendar
- Branch information display
- Daily inspiration system

### Phase 3: Enhanced Features (Future)
- File uploads for sermons and images
- User registration and profiles
- Advanced search and filtering
- Admin dashboard
- Content management system

## 🚀 Deployment

### Local Development
- Perfect for learning and development
- No external dependencies
- Easy to modify and test

### Production Considerations
- Use a production WSGI server (Gunicorn, uWSGI)
- Set up proper environment variables
- Configure HTTPS and security headers
- Consider migrating to PostgreSQL for larger scale

## 📚 Learning Objectives

This project demonstrates:
- **Web Development**: Full-stack web application development
- **Python Flask**: Backend framework usage and routing
- **Database Design**: SQLite schema design and queries
- **Frontend Development**: HTML, CSS, and JavaScript integration
- **User Authentication**: Session management and security
- **Responsive Design**: Mobile-first web development
- **Template Engines**: Jinja2 templating with Flask

## 🐛 Troubleshooting

### Common Issues
1. **Port already in use**: Change port in `app.py` or kill existing process
2. **Database errors**: Delete `database/database.db` and restart app
3. **Import errors**: Ensure all requirements are installed
4. **Template not found**: Check file paths and Jinja2 syntax

### Debug Mode
Enable debug mode in `app.py` for development:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

## 🤝 Contributing

This is a learning project, but suggestions for improvements are welcome:
- Add new features and functionality
- Improve styling and user experience
- Enhance security measures
- Optimize performance

## 📄 License

This project is created for educational purposes. Feel free to use and modify for your own learning and development.

## 🎯 Next Steps

After getting familiar with the current implementation:
1. **Add new features**: User registration, file uploads, admin panel
2. **Enhance UI/UX**: More animations, better mobile experience
3. **Improve security**: Add CSRF protection, rate limiting
4. **Performance**: Implement caching, lazy loading, CDN
5. **Testing**: Add unit tests and integration tests

---

**Happy Coding! 🎉**

For questions or support, refer to the Flask documentation and web development best practices.
