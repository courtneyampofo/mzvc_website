from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import sqlite3
import hashlib
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Database configuration
DATABASE = 'database/database.db'

def init_db():
    """Initialize the database with tables"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email TEXT,
            role TEXT DEFAULT 'user'
        )
    ''')
    
    # Create sermons table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sermons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            speaker TEXT NOT NULL,
            date TEXT NOT NULL,
            scripture TEXT,
            description TEXT
        )
    ''')
    
    # Create events table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL,
            time TEXT,
            location TEXT,
            registration_required INTEGER DEFAULT 0
        )
    ''')
    
    # Create branches table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS branches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT NOT NULL,
            phone TEXT,
            email TEXT,
            service_times TEXT
        )
    ''')
    
    # Create daily inspiration table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_inspiration (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scripture TEXT NOT NULL,
            quote TEXT,
            author TEXT,
            date TEXT UNIQUE NOT NULL
        )
    ''')
    
    # Insert default admin user if not exists
    cursor.execute('SELECT * FROM users WHERE username = ?', ('admin',))
    if not cursor.fetchone():
        password_hash = hashlib.sha256('admin123'.encode()).hexdigest()
        cursor.execute('''
            INSERT INTO users (username, password_hash, email, role)
            VALUES (?, ?, ?, ?)
        ''', ('admin', password_hash, 'admin@church.com', 'admin'))
    
    # Insert sample data
    insert_sample_data(cursor)
    
    conn.commit()
    conn.close()

def insert_sample_data(cursor):
    """Insert sample data for demonstration"""
    # Sample sermons
    sample_sermons = [
        ('The Power of Faith', 'Pastor John', '2024-01-15', 'Hebrews 11:1', 'Understanding the essence of faith'),
        ('Love Your Neighbor', 'Pastor Sarah', '2024-01-22', 'Matthew 22:39', 'Practicing love in daily life'),
        ('Hope in Christ', 'Pastor John', '2024-01-29', 'Romans 15:13', 'Finding hope through Jesus')
    ]
    
    for sermon in sample_sermons:
        cursor.execute('''
            INSERT OR IGNORE INTO sermons (title, speaker, date, scripture, description)
            VALUES (?, ?, ?, ?, ?)
        ''', sermon)
    
    # Sample events
    sample_events = [
        ('Sunday Service', 'Weekly Sunday worship service', '2024-02-04', '09:00', 'Main Sanctuary', 0),
        ('Bible Study', 'Weekly Bible study group', '2024-02-06', '19:00', 'Fellowship Hall', 0),
        ('Youth Ministry', 'Youth group meeting', '2024-02-08', '18:00', 'Youth Center', 0)
    ]
    
    for event in sample_events:
        cursor.execute('''
            INSERT OR IGNORE INTO events (title, description, date, time, location, registration_required)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', event)
    
    # Sample branches
    sample_branches = [
        ('Main Campus', '123 Church Street, City', '+1-555-0123', 'main@church.com', 'Sunday 9:00 AM, 11:00 AM'),
        ('North Branch', '456 North Avenue, City', '+1-555-0456', 'north@church.com', 'Sunday 10:00 AM'),
        ('South Branch', '789 South Road, City', '+1-555-0789', 'south@church.com', 'Sunday 10:30 AM')
    ]
    
    for branch in sample_branches:
        cursor.execute('''
            INSERT OR IGNORE INTO branches (name, address, phone, email, service_times)
            VALUES (?, ?, ?, ?, ?)
        ''', branch)
    
    # Sample daily inspiration
    sample_inspiration = [
        ('For I know the plans I have for you, declares the Lord, plans to prosper you and not to harm you, plans to give you hope and a future.', 'Jeremiah 29:11', 'Jeremiah', '2024-02-01'),
        ('I can do all things through Christ who strengthens me.', 'Philippians 4:13', 'Paul', '2024-02-02'),
        ('Be strong and courageous. Do not be afraid; do not be discouraged, for the Lord your God will be with you wherever you go.', 'Joshua 1:9', 'Joshua', '2024-02-03')
    ]
    
    for inspiration in sample_inspiration:
        cursor.execute('''
            INSERT OR IGNORE INTO daily_inspiration (scripture, quote, author, date)
            VALUES (?, ?, ?, ?)
        ''', inspiration)

def get_db_connection():
    """Get a database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def require_admin(f):
    """Decorator to require admin access"""
    def decorated_function(*args, **kwargs):
        if not session.get('user_id') or session.get('role') != 'admin':
            flash('Admin access required', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# Routes
@app.route('/')
def index():
    """Homepage"""
    conn = get_db_connection()
    
    # Get upcoming events
    cursor = conn.execute('''
        SELECT * FROM events 
        WHERE date >= date('now') 
        ORDER BY date ASC 
        LIMIT 3
    ''')
    upcoming_events = cursor.fetchall()
    
    # Get today's inspiration
    cursor = conn.execute('''
        SELECT * FROM daily_inspiration 
        WHERE date = date('now')
    ''')
    today_inspiration = cursor.fetchone()
    
    # Get recent sermons
    cursor = conn.execute('''
        SELECT * FROM sermons 
        ORDER BY date DESC 
        LIMIT 3
    ''')
    recent_sermons = cursor.fetchall()
    
    conn.close()
    
    return render_template('index.html', 
                         upcoming_events=upcoming_events,
                         today_inspiration=today_inspiration,
                         recent_sermons=recent_sermons)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login - MINIMAL WORKING VERSION"""
    print("=== LOGIN ROUTE CALLED ===")
    
    if request.method == 'POST':
        print("POST request received")
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        print(f"Username: {username}")
        print(f"Password: {password}")
        
        # Check against database
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('SELECT id, username, password_hash, role FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()
        
        if user and user[2] == hashlib.sha256(password.encode()).hexdigest():
            print("Login successful!")
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['role'] = user[3]
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            print("Login failed")
            flash('Invalid username or password', 'error')
    
    print("Rendering login template...")
    return render_template('login.html')

@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

# Admin Routes
@app.route('/admin')
@require_admin
def admin_dashboard():
    """Admin dashboard main page"""
    conn = get_db_connection()
    
    # Get counts for dashboard
    cursor = conn.execute('SELECT COUNT(*) FROM sermons')
    sermon_count = cursor.fetchone()[0]
    
    cursor = conn.execute('SELECT COUNT(*) FROM events')
    event_count = cursor.fetchone()[0]
    
    cursor = conn.execute('SELECT COUNT(*) FROM branches')
    branch_count = cursor.fetchone()[0]
    
    cursor = conn.execute('SELECT COUNT(*) FROM daily_inspiration')
    inspiration_count = cursor.fetchone()[0]
    
    conn.close()
    
    return render_template('admin/dashboard.html',
                         sermon_count=sermon_count,
                         event_count=event_count,
                         branch_count=branch_count,
                         inspiration_count=inspiration_count)

@app.route('/admin/sermons')
@require_admin
def admin_sermons():
    """Admin sermons management"""
    conn = get_db_connection()
    cursor = conn.execute('SELECT * FROM sermons ORDER BY date DESC')
    sermons = cursor.fetchall()
    conn.close()
    
    return render_template('admin/sermons.html', sermons=sermons)

@app.route('/admin/sermons/add', methods=['GET', 'POST'])
@require_admin
def admin_add_sermon():
    """Add new sermon"""
    if request.method == 'POST':
        title = request.form['title']
        speaker = request.form['speaker']
        date = request.form['date']
        scripture = request.form['scripture']
        description = request.form['description']
        
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO sermons (title, speaker, date, scripture, description)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, speaker, date, scripture, description))
        conn.commit()
        conn.close()
        
        flash('Sermon added successfully!', 'success')
        return redirect(url_for('admin_sermons'))
    
    return render_template('admin/add_sermon.html')

@app.route('/admin/sermons/edit/<int:id>', methods=['GET', 'POST'])
@require_admin
def admin_edit_sermon(id):
    """Edit sermon"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    if request.method == 'POST':
        title = request.form['title']
        speaker = request.form['speaker']
        date = request.form['date']
        scripture = request.form['scripture']
        description = request.form['description']
        
        cursor.execute('''
            UPDATE sermons SET title=?, speaker=?, date=?, scripture=?, description=?
            WHERE id=?
        ''', (title, speaker, date, scripture, description, id))
        conn.commit()
        conn.close()
        
        flash('Sermon updated successfully!', 'success')
        return redirect(url_for('admin_sermons'))
    
    cursor.execute('SELECT * FROM sermons WHERE id = ?', (id,))
    sermon = cursor.fetchone()
    conn.close()
    
    if not sermon:
        flash('Sermon not found', 'error')
        return redirect(url_for('admin_sermons'))
    
    return render_template('admin/edit_sermon.html', sermon=sermon)

@app.route('/admin/sermons/delete/<int:id>')
@require_admin
def admin_delete_sermon(id):
    """Delete sermon"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM sermons WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    flash('Sermon deleted successfully!', 'success')
    return redirect(url_for('admin_sermons'))

@app.route('/admin/events')
@require_admin
def admin_events():
    """Admin events management"""
    conn = get_db_connection()
    cursor = conn.execute('SELECT * FROM events ORDER BY date ASC')
    events = cursor.fetchall()
    conn.close()
    
    return render_template('admin/events.html', events=events)

@app.route('/admin/events/add', methods=['GET', 'POST'])
@require_admin
def admin_add_event():
    """Add new event"""
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        date = request.form['date']
        time = request.form['time']
        location = request.form['location']
        registration_required = 1 if request.form.get('registration_required') else 0
        
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO events (title, description, date, time, location, registration_required)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, description, date, time, location, registration_required))
        conn.commit()
        conn.close()
        
        flash('Event added successfully!', 'success')
        return redirect(url_for('admin_events'))
    
    return render_template('admin/add_event.html')

@app.route('/admin/events/edit/<int:id>', methods=['GET', 'POST'])
@require_admin
def admin_edit_event(id):
    """Edit event"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        date = request.form['date']
        time = request.form['time']
        location = request.form['location']
        registration_required = 1 if request.form.get('registration_required') else 0
        
        cursor.execute('''
            UPDATE events SET title=?, description=?, date=?, time=?, location=?, registration_required=?
            WHERE id=?
        ''', (title, description, date, time, location, registration_required, id))
        conn.commit()
        conn.close()
        
        flash('Event updated successfully!', 'success')
        return redirect(url_for('admin_events'))
    
    cursor.execute('SELECT * FROM events WHERE id = ?', (id,))
    event = cursor.fetchone()
    conn.close()
    
    if not event:
        flash('Event not found', 'error')
        return redirect(url_for('admin_events'))
    
    return render_template('admin/edit_event.html', event=event)

@app.route('/admin/events/delete/<int:id>')
@require_admin
def admin_delete_event(id):
    """Delete event"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM events WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    flash('Event deleted successfully!', 'success')
    return redirect(url_for('admin_events'))

@app.route('/admin/branches')
@require_admin
def admin_branches():
    """Admin branches management"""
    conn = get_db_connection()
    cursor = conn.execute('SELECT * FROM branches')
    branches = cursor.fetchall()
    conn.close()
    
    return render_template('admin/branches.html', branches=branches)

@app.route('/admin/branches/add', methods=['GET', 'POST'])
@require_admin
def admin_add_branch():
    """Add new branch"""
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        phone = request.form['phone']
        email = request.form['email']
        service_times = request.form['service_times']
        
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO branches (name, address, phone, email, service_times)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, address, phone, email, service_times))
        conn.commit()
        conn.close()
        
        flash('Branch added successfully!', 'success')
        return redirect(url_for('admin_branches'))
    
    return render_template('admin/add_branch.html')

@app.route('/admin/branches/edit/<int:id>', methods=['GET', 'POST'])
@require_admin
def admin_edit_branch(id):
    """Edit branch"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        phone = request.form['phone']
        email = request.form['email']
        service_times = request.form['service_times']
        
        cursor.execute('''
            UPDATE branches SET name=?, address=?, phone=?, email=?, service_times=?
            WHERE id=?
        ''', (name, address, phone, email, service_times, id))
        conn.commit()
        conn.close()
        
        flash('Branch updated successfully!', 'success')
        return redirect(url_for('admin_branches'))
    
    cursor.execute('SELECT * FROM branches WHERE id = ?', (id,))
    branch = cursor.fetchone()
    conn.close()
    
    if not branch:
        flash('Branch not found', 'error')
        return redirect(url_for('admin_branches'))
    
    return render_template('admin/edit_branch.html', branch=branch)

@app.route('/admin/branches/delete/<int:id>')
@require_admin
def admin_delete_branch(id):
    """Delete branch"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM branches WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    flash('Branch deleted successfully!', 'success')
    return redirect(url_for('admin_branches'))

@app.route('/admin/inspiration')
@require_admin
def admin_inspiration():
    """Admin daily inspiration management"""
    conn = get_db_connection()
    cursor = conn.execute('SELECT * FROM daily_inspiration ORDER BY date DESC')
    inspirations = cursor.fetchall()
    conn.close()
    
    return render_template('admin/inspiration.html', inspirations=inspirations)

@app.route('/admin/inspiration/add', methods=['GET', 'POST'])
@require_admin
def admin_add_inspiration():
    """Add new daily inspiration"""
    if request.method == 'POST':
        scripture = request.form['scripture']
        quote = request.form['quote']
        author = request.form['author']
        date = request.form['date']
        
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO daily_inspiration (scripture, quote, author, date)
            VALUES (?, ?, ?, ?)
        ''', (scripture, quote, author, date))
        conn.commit()
        conn.close()
        
        flash('Daily inspiration added successfully!', 'success')
        return redirect(url_for('admin_inspiration'))
    
    return render_template('admin/add_inspiration.html')

@app.route('/admin/inspiration/edit/<int:id>', methods=['GET', 'POST'])
@require_admin
def admin_edit_inspiration(id):
    """Edit daily inspiration"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    if request.method == 'POST':
        scripture = request.form['scripture']
        quote = request.form['quote']
        author = request.form['author']
        date = request.form['date']
        
        cursor.execute('''
            UPDATE daily_inspiration SET scripture=?, quote=?, author=?, date=?
            WHERE id=?
        ''', (scripture, quote, author, date, id))
        conn.commit()
        conn.close()
        
        flash('Daily inspiration updated successfully!', 'success')
        return redirect(url_for('admin_inspiration'))
    
    cursor.execute('SELECT * FROM daily_inspiration WHERE id = ?', (id,))
    inspiration = cursor.fetchone()
    conn.close()
    
    if not inspiration:
        flash('Daily inspiration not found', 'error')
        return redirect(url_for('admin_inspiration'))
    
    return render_template('admin/edit_inspiration.html', inspiration=inspiration)

@app.route('/admin/inspiration/delete/<int:id>')
@require_admin
def admin_delete_inspiration(id):
    """Delete daily inspiration"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM daily_inspiration WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    flash('Daily inspiration deleted successfully!', 'success')
    return redirect(url_for('admin_inspiration'))

@app.route('/sermons')
def sermons():
    """Sermon archives"""
    conn = get_db_connection()
    cursor = conn.execute('SELECT * FROM sermons ORDER BY date DESC')
    sermons = cursor.fetchall()
    conn.close()
    
    return render_template('sermons.html', sermons=sermons)

@app.route('/events')
def events():
    """Church events"""
    conn = get_db_connection()
    cursor = conn.execute('SELECT * FROM events ORDER BY date ASC')
    events = cursor.fetchall()
    conn.close()
    
    return render_template('events.html', events=events)

@app.route('/branches')
def branches():
    """Branch information"""
    conn = get_db_connection()
    cursor = conn.execute('SELECT * FROM branches')
    branches = cursor.fetchall()
    conn.close()
    
    return render_template('branches.html', branches=branches)

@app.route('/inspiration')
def inspiration():
    """Daily biblical inspiration"""
    conn = get_db_connection()
    cursor = conn.execute('SELECT * FROM daily_inspiration ORDER BY date DESC')
    inspirations = cursor.fetchall()
    conn.close()
    
    return render_template('inspiration.html', inspirations=inspirations)

if __name__ == '__main__':
    # Ensure uploads directory exists
    os.makedirs('uploads', exist_ok=True)
    
    # Initialize database
    init_db()
    
    print("Church Website is running!")
    print("Default admin credentials: username: admin, password: admin123")
    print("Visit http://localhost:5000 to view the website")
    print("Admin dashboard: http://localhost:5000/admin")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
