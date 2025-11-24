from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import get_user, DiceRoller


# Blueprint groups related routes together
main = Blueprint('main', __name__)

# Store a DiceRoller instance per user
dice_rollers = {}


def get_roller():
    """Get or create DiceRoller for current user."""
    if current_user.is_authenticated:
        user_id = current_user.id
        if user_id not in dice_rollers:
            dice_rollers[user_id] = DiceRoller()
        return dice_rollers[user_id]
    return None


# ============== PUBLIC ROUTES ==============

@main.route('/')
def home():
    """Home page - anyone can access."""
    return render_template('home.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    """Login page - handles both displaying form and processing login."""
    
    # Already logged in? Go to dashboard
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = get_user(username)
        
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')


# ============== PROTECTED ROUTES ==============

@main.route('/dashboard')
@login_required
def dashboard():
    """Main dice roller interface - must be logged in."""
    roller = get_roller()
    recent_rolls = roller.get_history()[-10:]
    return render_template('dashboard.html',
                          username=current_user.username,
                          recent_rolls=recent_rolls)


@main.route('/roll', methods=['POST'])
@login_required
def roll():
    """Handle dice roll form submission."""
    roller = get_roller()
    
    try:
        num_dice = int(request.form.get('num_dice', 1))
        sides = int(request.form.get('sides', 6))
        
        results = roller.roll(num_dice, sides)
        flash(f'Rolled {num_dice}d{sides}: {results} (Total: {sum(results)})', 'success')
    except ValueError as e:
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('main.dashboard'))


@main.route('/stats')
@login_required
def stats():
    """Display roll statistics."""
    roller = get_roller()
    return render_template('stats.html',
                          username=current_user.username,
                          stats=roller.get_stats(),
                          history=roller.get_history())


@main.route('/clear', methods=['POST'])
@login_required
def clear():
    """Clear roll history."""
    roller = get_roller()
    roller.clear_history()
    flash('History cleared!', 'success')
    return redirect(url_for('main.dashboard'))


@main.route('/logout')
@login_required
def logout():
    """Log out the user."""
    if current_user.id in dice_rollers:
        del dice_rollers[current_user.id]
    
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))