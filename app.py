from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import Base, User, LeaveRequest
from config import Config
from datetime import datetime, date
from functools import wraps
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Base.metadata.create_all(engine)
SessionLocal = scoped_session(sessionmaker(bind=engine))

# Create default admin user
def create_default_admin():
    db_session = SessionLocal()
    try:
        admin = db_session.query(User).filter_by(email='admin@company.com').first()
        if not admin:
            admin = User(
                name='System Admin',
                email='admin@company.com',
                role='admin',
                leave_balance=0
            )
            admin.set_password('admin123')
            db_session.add(admin)
            db_session.commit()
            print("✅ Default admin created: admin@company.com / admin123")
    finally:
        db_session.close()

create_default_admin()


# ==================== DECORATORS ====================

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'warning')
            return redirect(url_for('login'))
        
        db_session = SessionLocal()
        try:
            user = db_session.query(User).get(session['user_id'])
            if not user or user.role != 'admin':
                flash('Unauthorized access. Admin privileges required.', 'danger')
                return redirect(url_for('dashboard'))
        finally:
            db_session.close()
        
        return f(*args, **kwargs)
    return decorated_function


# ==================== HOME & AUTH ROUTES ====================

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        if not all([name, email, password, confirm_password]):
            flash('All fields are required', 'danger')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long', 'danger')
            return render_template('register.html')
        
        db_session = SessionLocal()
        try:
            existing_user = db_session.query(User).filter_by(email=email).first()
            if existing_user:
                flash('Email already registered. Please login.', 'warning')
                return redirect(url_for('login'))
            
            new_user = User(
                name=name,
                email=email,
                role='employee',
                leave_balance=Config.DEFAULT_LEAVE_BALANCE
            )
            new_user.set_password(password)
            
            db_session.add(new_user)
            db_session.commit()
            flash(f'Registration successful! You have {Config.DEFAULT_LEAVE_BALANCE} days of leave.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db_session.rollback()
            flash('Registration failed. Please try again.', 'danger')
            print(f"Registration error: {e}")
        finally:
            db_session.close()
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        
        if not email or not password:
            flash('Please provide both email and password', 'danger')
            return render_template('login.html')
        
        db_session = SessionLocal()
        try:
            user = db_session.query(User).filter_by(email=email).first()
            
            if user and user.check_password(password):
                session['user_id'] = user.id
                session['user_name'] = user.name
                session['user_role'] = user.role
                session.permanent = True
                
                flash(f'Welcome back, {user.name}!', 'success')
                
                if user.role == 'admin':
                    return redirect(url_for('admin_dashboard'))
                else:
                    return redirect(url_for('dashboard'))
            else:
                flash('Invalid email or password', 'danger')
        finally:
            db_session.close()
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully', 'info')
    return redirect(url_for('login'))


# ==================== EMPLOYEE ROUTES ====================

@app.route('/dashboard')
@login_required
def dashboard():
    db_session = SessionLocal()
    try:
        user = db_session.query(User).get(session['user_id'])
        leave_requests = db_session.query(LeaveRequest).filter_by(user_id=user.id)\
            .order_by(LeaveRequest.applied_at.desc()).all()
        
        stats = {
            'total_requests': len(leave_requests),
            'pending': sum(1 for req in leave_requests if req.status == 'Pending'),
            'approved': sum(1 for req in leave_requests if req.status == 'Approved'),
            'rejected': sum(1 for req in leave_requests if req.status == 'Rejected'),
            'leave_balance': user.leave_balance
        }
        
        return render_template('dashboard.html', user=user, requests=leave_requests, stats=stats)
    finally:
        db_session.close()


@app.route('/apply-leave', methods=['GET', 'POST'])
@login_required
def apply_leave():
    db_session = SessionLocal()
    try:
        user = db_session.query(User).get(session['user_id'])
        
        if request.method == 'POST':
            start_date_str = request.form.get('start_date')
            end_date_str = request.form.get('end_date')
            reason = request.form.get('reason', '').strip()
            
            if not all([start_date_str, end_date_str, reason]):
                flash('All fields are required', 'danger')
                return render_template('apply_leave.html', user=user)
            
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid date format', 'danger')
                return render_template('apply_leave.html', user=user)
            
            today = date.today()
            
            if start_date < today:
                flash('Start date cannot be in the past', 'danger')
                return render_template('apply_leave.html', user=user)
            
            if end_date < start_date:
                flash('End date must be after start date', 'danger')
                return render_template('apply_leave.html', user=user)
            
            leave_days = (end_date - start_date).days + 1
            
            if leave_days > user.leave_balance:
                flash(f'Insufficient leave balance. You have {user.leave_balance} days available.', 'danger')
                return render_template('apply_leave.html', user=user)
            
            leave_request = LeaveRequest(
                user_id=user.id,
                start_date=start_date,
                end_date=end_date,
                reason=reason,
                days=leave_days,
                status='Pending'
            )
            
            try:
                db_session.add(leave_request)
                db_session.commit()
                flash(f'Leave request submitted successfully for {leave_days} day(s)!', 'success')
                return redirect(url_for('dashboard'))
            except Exception as e:
                db_session.rollback()
                flash('Failed to submit leave request. Please try again.', 'danger')
                print(f"Leave request error: {e}")
        
        return render_template('apply_leave.html', user=user)
    finally:
        db_session.close()


# ==================== ADMIN ROUTES ====================

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    db_session = SessionLocal()
    try:
        all_requests = db_session.query(LeaveRequest).order_by(LeaveRequest.applied_at.desc()).all()
        
        stats = {
            'total_employees': db_session.query(User).filter_by(role='employee').count(),
            'total_requests': len(all_requests),
            'pending': sum(1 for req in all_requests if req.status == 'Pending'),
            'approved': sum(1 for req in all_requests if req.status == 'Approved'),
            'rejected': sum(1 for req in all_requests if req.status == 'Rejected'),
        }
        
        pending_requests = [req for req in all_requests if req.status == 'Pending']
        
        return render_template('admin_dashboard.html', 
                             requests=all_requests, 
                             pending_requests=pending_requests,
                             stats=stats)
    finally:
        db_session.close()


@app.route('/admin/approve/<int:request_id>')
@admin_required
def approve_leave(request_id):
    db_session = SessionLocal()
    try:
        leave_request = db_session.query(LeaveRequest).get(request_id)
        
        if not leave_request:
            flash('Leave request not found', 'danger')
            return redirect(url_for('admin_dashboard'))
        
        if leave_request.status != 'Pending':
            flash('This request has already been processed', 'warning')
            return redirect(url_for('admin_dashboard'))
        
        user = db_session.query(User).get(leave_request.user_id)
        
        if user.leave_balance < leave_request.days:
            flash(f'Cannot approve: {user.name} has insufficient leave balance', 'danger')
            return redirect(url_for('admin_dashboard'))
        
        leave_request.status = 'Approved'
        leave_request.reviewed_at = datetime.utcnow()
        user.leave_balance -= leave_request.days
        
        try:
            db_session.commit()
            flash(f'Leave approved for {user.name}. {leave_request.days} day(s) deducted.', 'success')
        except Exception as e:
            db_session.rollback()
            flash('Failed to approve leave request', 'danger')
            print(f"Approval error: {e}")
        
        return redirect(url_for('admin_dashboard'))
    finally:
        db_session.close()


@app.route('/admin/reject/<int:request_id>')
@admin_required
def reject_leave(request_id):
    db_session = SessionLocal()
    try:
        leave_request = db_session.query(LeaveRequest).get(request_id)
        
        if not leave_request:
            flash('Leave request not found', 'danger')
            return redirect(url_for('admin_dashboard'))
        
        if leave_request.status != 'Pending':
            flash('This request has already been processed', 'warning')
            return redirect(url_for('admin_dashboard'))
        
        leave_request.status = 'Rejected'
        leave_request.reviewed_at = datetime.utcnow()
        
        try:
            db_session.commit()
            user = db_session.query(User).get(leave_request.user_id)
            flash(f'Leave rejected for {user.name}', 'info')
        except Exception as e:
            db_session.rollback()
            flash('Failed to reject leave request', 'danger')
            print(f"Rejection error: {e}")
        
        return redirect(url_for('admin_dashboard'))
    finally:
        db_session.close()


# ==================== TEARDOWN ====================

@app.teardown_appcontext
def shutdown_session(exception=None):
    SessionLocal.remove()


# ==================== RUN APP ====================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Leave Management System Starting...")
    print("="*60)
    print("📍 Server: http://localhost:5000")
    print("👤 Admin Login: admin@company.com / admin123")
    print("="*60 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)