# Catatan Langkah

## Inisialisasi Git
1. `git init`
2. `git branch -m main`
3. `git add .`
4. `git commit -m "Initial commit"`

## Bersihkan Secret Stripe dan History
1. Hapus hardcoded `sk_test_...` di `payments/views_stripe.py` dan ganti ke `os.getenv("STRIPE_SECRET_KEY")`.
2. Commit perubahan:
   - `git commit -m "Remove hardcoded Stripe secret key"`
3. Rewrite history agar commit bersih:
   - `git checkout --orphan main_clean`
   - `git add .`
   - `git commit -m "Initial commit"`
   - `git branch -f main`
   - `git checkout main`
   - `git branch -D main_clean`

## Tambah Docker dan Compose
1. Buat `Dockerfile`.
2. Buat `docker-compose.yml`.
3. Buat `.dockerignore`.

## Tambah Workflow GHCR
1. Buat `.github/workflows/ghcr.yml` untuk build dan push ke GHCR (tag: `latest` + short `sha`).
2. Commit:
   - `git add .dockerignore Dockerfile docker-compose.yml .github/workflows/ghcr.yml`
   - `git commit -m "Add Docker Compose and GHCR build workflow"`

## Remote dan Push ke GitHub
1. `git remote add origin https://github.com/Gunanto/djangolms.git`
2. `git push -u origin main` (login pakai PAT).

## Buat .env Lokal
1. Buat `.env` dari `.env.example`.
2. Set `SECRET_KEY` baru dan `DEBUG=True`.

## Setelah Push di GitHub
1. Cek tab **Actions** dan pastikan workflow sukses.
2. Tab **Packages** → set image `ghcr.io/gunanto/djangolms` ke **Public** (jika ingin pull tanpa auth).

---

# Menjalankan via Docker Compose (Lokal)

## Siapkan .env
- Pastikan `.env` ada di root repo.
- Update email setting jika perlu.
  - Tambahkan `ALLOWED_HOSTS=127.0.0.1,localhost,0.0.0.0` jika diperlukan.

## Jalankan Compose
```bash
docker compose up -d --build
```

## Cek Container
```bash
docker compose ps
```

## Lihat Log
```bash
docker compose logs -f
```

## Akses Aplikasi
- Buka `http://localhost:8000`

## Jalankan Migrasi & Buat Akun Admin
```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

## Catatan Login
- Login di `http://localhost:8000/en/accounts/login/?next=/en/`

---

# Menjalankan via Docker Run (GHCR)

## Login & Pull Image (opsional)
```bash
docker login ghcr.io -u gunanto
docker pull ghcr.io/gunanto/djangolms:latest
```

## Jalankan Container
```bash
docker run -d --name djangolms --env-file .env -p 8000:8000 ghcr.io/gunanto/djangolms:latest
```
## Otomatis migrate saat `docker run`
```bash
docker run --name djangolms --env-file .env -p 8000:8000 ghcr.io/gunanto/djangolms:latest \
  bash -lc "python manage.py migrate && gunicorn config.wsgi:application --bind 0.0.0.0:8000"
```

## Rebuild & Push Image (jika code lokal lebih baru)
```bash
docker build -t ghcr.io/gunanto/djangolms:latest .
docker push ghcr.io/gunanto/djangolms:latest
```

## Jalankan Migrasi & Buat Akun Admin
```bash
docker exec -it djangolms python manage.py migrate
docker exec -it djangolms python manage.py createsuperuser
```

## Catatan Login
- Login di `http://localhost:8000/en/accounts/login/?next=/en/`

---

# Catatan Tambahan
- `.env` jangan di-commit.
- Jika butuh database, tambahkan service Postgres di `docker-compose.yml` dan update `DATABASES` di `config/settings.py`.
- Untuk produksi: set `DEBUG=False`, isi `SECRET_KEY`, dan konfigurasi email sesuai kebutuhan.

## Persist Database (SQLite)
- Untuk Compose, gunakan volume (sudah di `docker-compose.yml`):
  - `./data/db.sqlite3:/app/db.sqlite3`
- Untuk Docker Run:
```bash
docker run --name djangolms \
  --env-file .env \
  -p 8000:8000 \
  -v $(pwd)/data/db.sqlite3:/app/db.sqlite3 \
  ghcr.io/gunanto/djangolms:latest
```

## Cek Container Lama
```bash
docker ps -a
docker start djangolms
```
