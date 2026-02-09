# Taking the project to the next level on **https://github.com/SkyCascade/SkyLearn** 🚀

# Repository Moved to [SkyCascade/SkyLearn](https://github.com/SkyCascade/SkyLearn) and no longer maintained here

### Please update your bookmarks and direct all issues and pull requests to the new repository.

---

*Note: This repository is archived and read-only.*

---

### Learning management system using django web framework

Feature-rich learning management system. You may want to build a learning management system(AKA school management system) for a school organization or just for the sake of learning the tech stack and building your portfolio, either way, this project would be a good kickstart for you.

![Screenshot from 2023-12-31 17-36-31](https://github.com/adilmohak/django-lms/assets/60693922/e7fb628a-6275-4160-ae0f-ab27099ab3ca)

---

## GHCR + Docker Compose

This repo includes a GitHub Actions workflow that builds and pushes the Docker image to GHCR on every push to `main`. Tags: `latest` and short `sha`.

### After pushing to GitHub
1. Open the **Actions** tab and ensure the workflow "Build and Push to GHCR" succeeds.
2. Open **Packages** and set `ghcr.io/gunanto/djangolms` visibility to **Public** if you want unauthenticated pulls.

### Pull the image
```bash
docker login ghcr.io
docker pull ghcr.io/gunanto/djangolms:latest
```

### Run with Docker Compose
1. Create `.env` based on `.env.example` and set `SECRET_KEY`.
2. Start the app:
```bash
docker compose up -d --build
```
3. Open `http://localhost:8000`.
