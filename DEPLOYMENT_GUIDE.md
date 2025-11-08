# 🚀 Deployment Guide: Quadratic Mastery Platform

Deploy the **Math Learning Platform** to **themathagent.com** using Render (backend + frontend).

## Architecture Overview

```
themathagent.com (Frontend - Next.js on Render)
    ↓ API calls
math-agent-api.onrender.com (Backend - FastAPI on Render)
    ├── Persistent data/progress.json (student mastery)
    └── Telemetry data/telemetry.jsonl (analytics)
```

---

## Step 1: Deploy Backend (FastAPI) on Render

### 1.1 Create Backend Service

1. Go to [dashboard.render.com](https://dashboard.render.com)
2. Click **"New+"** → **"Web Service"**
3. Connect your GitHub repo: `Agent_Math`
4. Select branch: `phase1-data-flywheel`
5. Configure service:
   - **Name:** `math-agent-api`
   - **Environment:** Python
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn -k uvicorn.workers.UvicornWorker api.server:app --bind 0.0.0.0:$PORT --timeout 90`
   - **Plan:** Free

### 1.2 Add Environment Variables

In Render dashboard, go to **Environment** tab and add:

| Key | Value |
|-----|-------|
| `PYTHON_VERSION` | `3.11.9` |
| `TELEMETRY_ENABLED` | `true` |
| `PROGRESS_AUTOSAVE_SECS` | `60` |
| `CORS_ORIGINS` | `https://themathagent.com,https://www.themathagent.com` |

### 1.3 Add Persistent Disk

1. Go to **Disks** tab
2. Click **"Add Disk"**
3. Configure:
   - **Name:** `persistent-data`
   - **Mount Path:** `/opt/render/project/src/data`
   - **Size:** 1 GB

### 1.4 Deploy & Test

1. Click **"Create Web Service"**
2. Wait 3-5 minutes for build
3. Note your backend URL: `https://math-agent-api-xxxxx.onrender.com`
4. Test it:
   ```bash
   curl https://math-agent-api-xxxxx.onrender.com/health
   # Should return: {"status":"ok"}
   ```

---

## Step 2: Deploy Frontend (Next.js) on Render

### 2.1 Create Frontend Service

1. In Render dashboard, click **"New+"** → **"Web Service"**
2. Connect same GitHub repo: `Agent_Math`
3. Select branch: `phase1-data-flywheel`
4. Configure service:
   - **Name:** `math-learning-platform`
   - **Environment:** Node
   - **Root Directory:** `math-learning-platform`
   - **Build Command:** `npm install && npm run build`
   - **Start Command:** `npm start`
   - **Plan:** Free

### 2.2 Add Environment Variables

In Render dashboard, go to **Environment** tab and add:

| Key | Value |
|-----|-------|
| `NODE_VERSION` | `18.0.0` |
| `NEXT_PUBLIC_API_URL` | `https://math-agent-api-xxxxx.onrender.com` |

**Important:** Replace `xxxxx` with your actual backend URL from Step 1.4!

### 2.3 Deploy Frontend

1. Click **"Create Web Service"**
2. Wait 3-5 minutes for build
3. Note your frontend URL: `https://math-learning-platform-xxxxx.onrender.com`

---

## Step 3: Connect Custom Domain

### 3.1 Configure Domain in Render

1. Go to your frontend service (`math-learning-platform`)
2. Click **"Settings"** → **"Custom Domains"**
3. Click **"Add Custom Domain"**
4. Add both:
   - `themathagent.com`
   - `www.themathagent.com`

### 3.2 Update DNS Records

Render will show you DNS instructions. Go to your domain registrar and add:

**For root domain (themathagent.com):**
- Type: `A`
- Name: `@`
- Value: `[IP address shown by Render]`

**For www subdomain:**
- Type: `CNAME`
- Name: `www`
- Value: `[CNAME target shown by Render]`

### 3.3 Wait for DNS Propagation

- Usually takes 5-30 minutes
- Check status in Render dashboard
- SSL certificate will be auto-generated

### 3.4 Update Backend CORS

Once your domain is working, update backend CORS:

1. Go to backend service (`math-agent-api`)
2. Go to **Environment** tab
3. Update `CORS_ORIGINS`:
   ```
   https://themathagent.com,https://www.themathagent.com,https://math-learning-platform-xxxxx.onrender.com
   ```
4. Service will auto-redeploy

---

## Step 4: Verify Deployment

### 4.1 Test Backend

```bash
# Health check
curl https://math-agent-api-xxxxx.onrender.com/health

# Get a question
curl -X POST https://math-agent-api-xxxxx.onrender.com/items/generate \
  -H "Content-Type: application/json" \
  -d '{"skill_id": "quad.graph.vertex", "difficulty": "easy"}'
```

### 4.2 Test Frontend

1. Visit `https://themathagent.com`
2. You should see the login page
3. Log in as a new student
4. Try starting the adaptive quiz
5. Answer a few questions
6. Check that progress is tracked

### 4.3 Check CORS

Open browser console (F12) and look for any CORS errors. If you see:
```
Access to XMLHttpRequest at 'https://math-agent-api...' from origin 'https://themathagent.com' has been blocked by CORS policy
```

Then go back and verify Step 3.4.

---

## Alternative: Deploy Frontend on Vercel (Recommended for Next.js)

Vercel is optimized for Next.js and offers better performance:

### Option B.1: Deploy to Vercel

1. Go to [vercel.com](https://vercel.com)
2. Click **"New Project"**
3. Import your GitHub repo: `Agent_Math`
4. Configure:
   - **Framework Preset:** Next.js (auto-detected)
   - **Root Directory:** `math-learning-platform`
   - **Build Command:** `npm run build` (auto-detected)
   - **Output Directory:** `.next` (auto-detected)

### Option B.2: Environment Variables

Add in Vercel dashboard:

| Key | Value |
|-----|-------|
| `NEXT_PUBLIC_API_URL` | `https://math-agent-api-xxxxx.onrender.com` |

### Option B.3: Custom Domain on Vercel

1. Go to project **Settings** → **Domains**
2. Add `themathagent.com` and `www.themathagent.com`
3. Follow Vercel's DNS instructions
4. DNS for Vercel:
   - Type: `CNAME`
   - Name: `@` (or root)
   - Value: `cname.vercel-dns.com`

---

## Deployment Checklist

- [ ] Backend deployed on Render
- [ ] Backend health check passes
- [ ] Frontend deployed (Render or Vercel)
- [ ] Environment variable `NEXT_PUBLIC_API_URL` set correctly
- [ ] Custom domain DNS configured
- [ ] SSL certificate active (auto by Render/Vercel)
- [ ] CORS origins include your domain
- [ ] Can login and answer questions
- [ ] Progress persists across page reloads

---

## Monitoring & Logs

### Render Logs

- Backend logs: `https://dashboard.render.com/web/[service-id]/logs`
- Frontend logs: `https://dashboard.render.com/web/[service-id]/logs`

### Check Backend Data

```bash
# View student progress
curl https://math-agent-api-xxxxx.onrender.com/progress

# Check telemetry
curl https://math-agent-api-xxxxx.onrender.com/health
```

---

## Troubleshooting

### Frontend can't connect to backend

**Error:** Network error or CORS error in browser console

**Fix:**
1. Check `NEXT_PUBLIC_API_URL` environment variable
2. Verify backend is deployed and running
3. Update `CORS_ORIGINS` in backend to include your frontend URL

### Domain not working

**Error:** DNS_PROBE_FINISHED_NXDOMAIN

**Fix:**
1. Verify DNS records at your registrar
2. Wait 30 minutes for DNS propagation
3. Use `nslookup themathagent.com` to check DNS

### Build fails

**Backend build error:**
- Check Python version is 3.11.9
- Verify `requirements.txt` is present

**Frontend build error:**
- Check Node version is >= 18.0.0
- Verify root directory is set to `math-learning-platform`
- Check for TypeScript errors: `npm run type-check`

---

## Cost

| Service | Free Tier Limits | Cost |
|---------|------------------|------|
| Render Backend | 750 hours/month, 512MB RAM | $0 |
| Render Frontend | 750 hours/month, 512MB RAM | $0 |
| Persistent Disk | 1 GB | $0 |
| Vercel (alternative) | 100 GB bandwidth | $0 |
| **Total** | | **$0/month** |

Domain registration: ~$10-15/year

---

## Next Steps After Deployment

1. Share the link: `https://themathagent.com`
2. Monitor usage in Render/Vercel dashboards
3. Check telemetry data periodically
4. Consider upgrading to paid tier if you get high traffic (>750 hrs/month)

---

## Support

- **Render Docs:** https://render.com/docs
- **Vercel Docs:** https://vercel.com/docs
- **Next.js Docs:** https://nextjs.org/docs
- **Repository Issues:** https://github.com/[your-username]/Agent_Math/issues
