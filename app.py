from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import Config
from models import db, User, Photo, Like
import os
import uuid
from werkzeug.utils import secure_filename

# ==================== INISIALISASI APP ====================
app = Flask(__name__)
app.config.from_object(Config)

# Inisialisasi Database
db.init_app(app)

# Inisialisasi Flask-Migrate
migrate = Migrate(app, db)

# Inisialisasi Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Silakan login untuk mengakses halaman ini.'
login_manager.login_message_category = 'info'

# Inisialisasi CSRF Protection
csrf = CSRFProtect(app)

# Inisialisasi Rate Limiter
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ==================== HELPER FUNCTIONS ====================
def allowed_file(filename):
    """Cek apakah ekstensi file diperbolehkan"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def save_uploaded_file(file):
    """Simpan file upload dan return nama file unik dengan error handling"""
    try:
        if file and allowed_file(file.filename):
            filename = str(uuid.uuid4()) + '_' + secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            # Pastikan folder upload ada
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            
            # Cek apakah file sudah ada (hindari overwrite)
            if os.path.exists(file_path):
                filename = str(uuid.uuid4()) + '_' + secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            file.save(file_path)
            
            # Verifikasi file berhasil disimpan
            if not os.path.exists(file_path):
                return None
                
            return filename
    except Exception as e:
        app.logger.error(f"Error saving file: {str(e)}")
        return None
    
    return None

# ==================== ROUTES ====================

# Home - Galeri Foto dengan Pagination
@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 12  # Foto per halaman
    
    photos_pagination = Photo.query.order_by(
        Photo.created_at.desc()
    ).paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('index.html', 
                         photos=photos_pagination.items, 
                         pagination=photos_pagination)

# Search Foto
@app.route('/search')
def search():
    query = request.args.get('q', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = 12
    
    if not query:
        return redirect(url_for('index'))
    
    # Search berdasarkan judul, deskripsi, atau nama uploader
    photos_pagination = Photo.query.join(
        Photo.uploader
    ).filter(
        db.or_(
            Photo.title.ilike(f'%{query}%'),
            Photo.description.ilike(f'%{query}%'),
            User.name.ilike(f'%{query}%')
        )
    ).order_by(
        Photo.created_at.desc()
    ).paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('index.html', 
                         photos=photos_pagination.items, 
                         pagination=photos_pagination,
                         search_query=query)

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Login berhasil! Selamat datang, ' + user.name, 'success')
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('index'))
        else:
            flash('Email atau password salah', 'error')
    
    return render_template('login.html')

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        if not name or not email or not password:
            flash('Semua field harus diisi', 'error')
            return redirect(url_for('register'))

        if User.query.filter_by(email=email).first():
            flash('Email sudah terdaftar', 'error')
            return redirect(url_for('register'))

        # Validasi kekuatan password server-side
        if len(password) < 8:
            flash('Password minimal 8 karakter', 'error')
            return redirect(url_for('register'))
        
        # Cek apakah password mengandung huruf kapital, angka, atau karakter spesial
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password)
        
        if not (has_upper and has_digit):
            flash('Password harus mengandung minimal 1 huruf kapital dan 1 angka', 'error')
            return redirect(url_for('register'))

        user = User(name=name, email=email)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash('Registrasi berhasil! Silakan login', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Anda telah logout', 'info')
    return redirect(url_for('index'))

# Upload Foto
@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        # Cek apakah ada file di request
        if 'photo' not in request.files:
            flash('Tidak ada file yang dipilih', 'error')
            return redirect(url_for('upload'))

        file = request.files['photo']

        # Cek apakah file kosong
        if file.filename == '':
            flash('Tidak ada file yang dipilih', 'error')
            return redirect(url_for('upload'))

        # Validasi ukuran file (16MB max)
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > app.config['MAX_CONTENT_LENGTH']:
            flash('Ukuran file terlalu besar (max 16MB)', 'error')
            return redirect(url_for('upload'))

        # Simpan file
        filename = save_uploaded_file(file)

        if filename:
            try:
                photo = Photo(
                    title=request.form.get('title'),
                    description=request.form.get('description'),
                    image_file=filename,
                    user_id=current_user.id
                )

                db.session.add(photo)
                db.session.commit()

                flash('Foto berhasil diupload!', 'success')
                return redirect(url_for('my_photos'))
            except Exception as e:
                db.session.rollback()
                app.logger.error(f"Error saving photo to database: {str(e)}")
                flash('Terjadi kesalahan saat menyimpan foto', 'error')
                return redirect(url_for('upload'))
        else:
            flash('Format file tidak didukung atau terjadi kesalahan', 'error')

    return render_template('upload.html')

# Foto Saya - Dashboard User dengan Pagination
@app.route('/my-photos')
@login_required
def my_photos():
    page = request.args.get('page', 1, type=int)
    per_page = 9  # Foto per halaman
    
    photos_pagination = Photo.query.filter_by(
        user_id=current_user.id
    ).order_by(Photo.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    # FIXED: pakai likes_count bukan likes
    total_likes = sum(photo.likes_count for photo in photos_pagination.items)

    return render_template('my_photos.html', 
                         photos=photos_pagination.items, 
                         total_likes=total_likes,
                         pagination=photos_pagination)

# Edit Profil - NEW ROUTE
@app.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        name = request.form.get('name')
        
        if not name:
            flash('Nama harus diisi', 'error')
            return redirect(url_for('edit_profile'))
        
        current_user.name = name
        db.session.commit()
        
        flash('Profil berhasil diupdate!', 'success')
        return redirect(url_for('edit_profile'))
    
    return render_template('edit_profile.html')

# Edit Foto
@app.route('/edit/<int:photo_id>', methods=['GET', 'POST'])
@login_required
def edit_photo(photo_id):
    photo = Photo.query.get_or_404(photo_id)

    if photo.user_id != current_user.id:
        flash('Anda tidak berhak mengedit foto ini', 'error')
        return redirect(url_for('my_photos'))

    if request.method == 'POST':
        photo.title = request.form.get('title')
        photo.description = request.form.get('description')

        if 'photo' in request.files:
            file = request.files['photo']
            if file and file.filename != '' and allowed_file(file.filename):
                try:
                    # Hapus file lama
                    old_file_path = os.path.join(app.config['UPLOAD_FOLDER'], photo.image_file)
                    if os.path.exists(old_file_path):
                        try:
                            os.remove(old_file_path)
                        except OSError as e:
                            app.logger.error(f"Error deleting old file: {str(e)}")
                    
                    # Simpan file baru
                    new_filename = save_uploaded_file(file)
                    if new_filename:
                        photo.image_file = new_filename
                    else:
                        flash('Gagal menyimpan file baru', 'error')
                        return redirect(url_for('edit_photo', photo_id=photo_id))
                except Exception as e:
                    app.logger.error(f"Error replacing file: {str(e)}")
                    flash('Terjadi kesalahan saat mengganti file', 'error')
                    return redirect(url_for('edit_photo', photo_id=photo_id))

        try:
            db.session.commit()
            flash('Foto berhasil diupdate', 'success')
            return redirect(url_for('my_photos'))
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error updating photo: {str(e)}")
            flash('Terjadi kesalahan saat mengupdate foto', 'error')
            return redirect(url_for('edit_photo', photo_id=photo_id))

    return render_template('upload.html', photo=photo)

# Hapus Foto
@app.route('/delete/<int:photo_id>', methods=['POST'])
@login_required
def delete_photo(photo_id):
    photo = Photo.query.get_or_404(photo_id)

    if photo.user_id != current_user.id:
        flash('Anda tidak berhak menghapus foto ini', 'error')
        return redirect(url_for('my_photos'))

    try:
        # Hapus file dari filesystem
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], photo.image_file)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except OSError as e:
                app.logger.error(f"Error deleting file: {str(e)}")
                flash('File foto gagal dihapus, tetapi data akan dihapus', 'warning')

        # Hapus dari database
        db.session.delete(photo)
        db.session.commit()

        flash('Foto berhasil dihapus', 'success')
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error deleting photo: {str(e)}")
        flash('Terjadi kesalahan saat menghapus foto', 'error')
    
    return redirect(url_for('my_photos'))

# Like Foto (AJAX) - 1 User 1 Like & Harus Login
# Rate limiting: 10 like per menit per user untuk mencegah abuse
@app.route('/like/<int:photo_id>', methods=['POST'])
@login_required
@limiter.limit("10 per minute")
def like_photo(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    user = current_user

    existing_like = Like.query.filter_by(user_id=user.id, photo_id=photo_id).first()

    if existing_like:
        db.session.delete(existing_like)
        photo.likes_count -= 1
        db.session.commit()
        return jsonify({'likes': photo.likes_count, 'liked': False})
    else:
        new_like = Like(user_id=user.id, photo_id=photo_id)
        db.session.add(new_like)
        photo.likes_count += 1
        db.session.commit()
        return jsonify({'likes': photo.likes_count, 'liked': True})

# Download Foto
@app.route('/download/<int:photo_id>')
def download_photo(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    
    # Direktori file upload
    upload_dir = app.config['UPLOAD_FOLDER']
    
    # Cek apakah file ada
    file_path = os.path.join(upload_dir, photo.image_file)
    if not os.path.exists(file_path):
        flash('File foto tidak ditemukan', 'error')
        return redirect(url_for('index'))
    
    # Kirim file sebagai download
    return send_from_directory(
        upload_dir,
        photo.image_file,
        as_attachment=True,
        download_name=photo.title + os.path.splitext(photo.image_file)[1]
    )

# Error Handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    flash('Terjadi kesalahan pada server', 'error')
    return redirect(url_for('index'))

# Rate limit exceeded handler
@app.errorhandler(429)
def ratelimit_handler(error):
    return jsonify({
        'error': 'Terlalu banyak request',
        'message': 'Silakan tunggu beberapa saat sebelum mencoba lagi'
    }), 429

# ==================== JALANKAN APP ====================
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)