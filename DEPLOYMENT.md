# 🚀 Deployment Guide: Math Agent

This guide covers deploying the Math Agent to **Render** (backend) and **Vercel** (frontend) with your custom domain `themathagent.com`.

---

## Architecture

```
themathagent.com (Vercel)
    ↓ (CORS allowed)
math-agent-api-xxxxx.onrender.com (FastAPI on Render)
    ├── Persistent data: data/progress.json (mastery state)
    └── Telemetry: data/telemetry.jsonl (event logs)
```

---

## Phase 1: Backend Deployment (Render)

### 1.1 Prerequisites

- [ ] GitHub account (repo is already public)
- [ ] Render account (free tier is fine: render.com)
- [ ] All backend code committed and pushed to GitHub

### 1.2 Files Already in Place

✅ `Procfile` — Gunicorn + Uvicorn configuration  
✅ `render.yaml` — Render deployment manifest with your domain  
✅ `requirements.txt` — All dependencies including gunicorn, uvicorn, fastapi  

### 1.3 Deploy to Render

1. Go to [render.com](https://render.com)
2. Sign in or create account
3. Click **"New+"** → **"Web Service"**
4. Select your GitHub repository (`Agent_Math`)
5. Render will auto-detect `render.yaml` — approve the defaults
6. Click **"Deploy"**

### 1.4 Wait for Deployment

- First deployment: ~3-5 minutes
- Watch the build log in Render dashboard
- Once complete, note your backend URL:
  - Format: `https://math-agent-api-xxxxx.onrender.com`
  - Save this URL! You'll need it for Step 2.

### 1.5 Verify Backend Works

```bash
curl https://math-agent-api-xxxxx.onrender.com/skills/manifest
# Should return a JSON dict of skills and difficulties
```

---

## Phase 2: DNS & Domain Setup

### 2.1 Point Your Domain to Vercel

1. Go to your domain registrar (Namecheap, GoDaddy, etc.)
2. Find DNS settings for `themathagent.com`
3. Add CNAME record:
   - Name: `@` (or root)
   - Value: `cname.vercel.com`
4. Add www subdomain (optional but recommended):
   - Name: `www`
   - Value: `cname.vercel.com`

DNS propagation: 5-30 minutes (sometimes instant)

---

## Phase 3: Frontend Deployment (Vercel)

### 3.1 Deploy to Vercel

1. Go to [vercel.com](https://vercel.com)
2. Sign in or create account
3. Click **"New Project"**
4. Import your GitHub repository (`Agent_Math`)
5. Configure project:
   - **Framework Preset:** Other
   - **Root Directory:** `web`
   - **Environment Variables:**
     ```
     VITE_API_BASE_URL=https://math-agent-api-xxxxx.onrender.com
     ```
     (Use the Render URL from Phase 1.4)

6. Click **"Deploy"**

### 3.2 Add Custom Domain in Vercel

1. Go to your Vercel project settings
2. Click **"Domains"**
3. Add `themathagent.com` and `www.themathagent.com`
4. Vercel will verify DNS (should be automatic if you completed Phase 2.1)

### 3.3 Verify Frontend Works

- Visit `https://themathagent.com`
- Should load without CORS errors
- Should fetch questions from backend
- Should persist mastery across page reloads

---

## Configuration Reference

### Render Backend (`render.yaml`)

```yaml
CORS_ORIGINS: "https://themathagent.com https://www.themathagent.com"
PROGRESS_PATH: data/progress.json
PROGRESS_AUTOSAVE_SECS: "60"
TELEMETRY_ENABLED: "true"
TELEMETRY_PATH: data/telemetry.jsonl
```

### Vercel Frontend

Environment variable in Vercel dashboard:
```
VITE_API_BASE_URL=https://math-agent-api-xxxxx.onrender.com
```

Update this if your Render URL changes.

---

## Monitoring

### Render Dashboard

- View build logs
- Check recent deployments
- Monitor disk usage (1GB for data/)
- View logs: https://dashboard.render.com/

### Vercel Dashboard

- View build logs
- Monitor traffic
- Check analytics
- View logs: https://vercel.com/dashboard/

---

## Data Persistence

### Mastery Progress

Stored at: `data/progress.json` (on Render's persistent disk)

- Auto-saved every 60 seconds (configurable)
- Survives server restarts
- Retrieved via: `GET /progress`

### Telemetry

Stored at: `data/telemetry.jsonl` (on Render's persistent disk)

- JSONL format (one JSON object per line)
- Auto-rotates at 5MB
- Analyzed via: `tools/analyze_telemetry.py`

---

## Troubleshooting

### "CORS Error" when loading frontend

**Cause:** Frontend URL not in `CORS_ORIGINS`

**Fix:**
1. Update `render.yaml`:
   ```yaml
   CORS_ORIGINS: "https://themathagent.com https://www.themathagent.com"
   ```
2. Commit and push
3. Render auto-redeploys in ~30 seconds

### "Cannot reach server" in browser

**Cause:** Backend URL wrong or not deployed yet

**Fix:**
1. Check Render dashboard: is backend running?
2. Check Vercel env vars: is `VITE_API_BASE_URL` correct?
3. In browser console, verify `window.API_BASE`

### DNS not propagating

**Cause:** DNS cache or wrong DNS record

**Fix:**
1. Wait 15-30 minutes
2. Use `nslookup themathagent.com` to verify DNS
3. Clear browser cache (Ctrl+Shift+Delete)

### Questions repeating on page reload

**Expected:** Questions repeat in in-memory mode. Progress persists when cycle mode is enabled.

**To enable cycle mode:** Set session_id on frontend (see `web/app.js`)

---

## Cost Estimate

| Service | Tier | Cost |
|---------|------|------|
| Render  | Free | $0   |
| Vercel  | Free | $0   |
| Domain  | Yearly | $10-15 (depends on registrar) |
| **Total** | | **~$12/year** |

---

## Next Steps

1. ✅ Backend deployed to Render
2. ✅ Domain pointed to Vercel
3. ✅ Frontend deployed to Vercel
4. Test the full application:
   - [ ] Load https://themathagent.com
   - [ ] Answer some questions
   - [ ] Verify mastery persists
   - [ ] Check telemetry: `curl https://math-agent-api-xxxxx.onrender.com/progress`

---

## Support

- **Render support:** render.com/docs
- **Vercel support:** vercel.com/docs
- **Git pushes:** If deploy doesn't trigger, re-push to GitHub
