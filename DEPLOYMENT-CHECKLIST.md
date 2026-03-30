# ✅ Deployment Checklist

## Pre-Deployment

### 1. Get API Keys
- [ ] Google Gemini API key from https://makersuite.google.com/app/apikey
- [ ] AWS account created (optional but recommended)
- [ ] AWS S3 bucket created: `meet-scribe-summaries`
- [ ] AWS IAM user with S3 access
- [ ] AWS access key and secret key saved

### 2. Create Accounts
- [ ] Render account: https://render.com
- [ ] Vercel account: https://vercel.com
- [ ] GitHub repository created (if using)

---

## Backend Deployment (Render)

### Step 1: Prepare
- [ ] Navigate to `meet-scribe-backend` folder
- [ ] Verify `main.py` exists
- [ ] Verify `requirements.txt` exists
- [ ] Verify `Procfile` exists
- [ ] Verify `runtime.txt` exists

### Step 2: Deploy
- [ ] Go to https://dashboard.render.com
- [ ] Click "New +" → "Web Service"
- [ ] Connect GitHub repo or upload files
- [ ] Set name: `meet-scribe-api`
- [ ] Set root directory: `meet-scribe-backend`
- [ ] Set build command: `pip install -r requirements.txt`
- [ ] Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Step 3: Environment Variables
- [ ] Add `SECRET_KEY` (generate random string)
- [ ] Add `GEMINI_API_KEY` (from Google)
- [ ] Add `AWS_ACCESS_KEY_ID` (optional)
- [ ] Add `AWS_SECRET_ACCESS_KEY` (optional)
- [ ] Add `AWS_BUCKET_NAME` (optional)

### Step 4: Verify
- [ ] Click "Create Web Service"
- [ ] Wait for deployment (5-10 minutes)
- [ ] Copy your API URL: `https://meet-scribe-api-XXXX.onrender.com`
- [ ] Test health check: Visit `https://your-api-url.onrender.com/`
- [ ] Test API docs: Visit `https://your-api-url.onrender.com/docs`
- [ ] Verify response shows: `{"status": "Google Meet AI Scribe API Running"}`

---

## Frontend Deployment (Vercel)

### Step 1: Update API URL
- [ ] Open `meet-scribe-frontend/index.html`
- [ ] Find line ~300: `const API_URL = ...`
- [ ] Replace with your Render URL:
  ```javascript
  const API_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:8000' 
    : 'https://meet-scribe-api-XXXX.onrender.com';
  ```
- [ ] Save the file

### Step 2: Deploy
- [ ] Go to https://vercel.com/new
- [ ] Import your GitHub repository
- [ ] Set root directory: `meet-scribe-frontend`
- [ ] Framework preset: Other
- [ ] Click "Deploy"

### Step 3: Verify
- [ ] Wait for deployment (~30 seconds)
- [ ] Copy your app URL: `https://your-project.vercel.app`
- [ ] Visit the URL
- [ ] Verify landing page loads
- [ ] Check browser console for errors (F12)

---

## Testing

### Backend Tests
- [ ] Visit `https://your-api-url.onrender.com/`
- [ ] Should see: `{"status": "Google Meet AI Scribe API Running"}`
- [ ] Visit `https://your-api-url.onrender.com/docs`
- [ ] Should see interactive API documentation
- [ ] Try "GET /" endpoint in docs
- [ ] Should return 200 OK

### Frontend Tests
- [ ] Visit your Vercel URL
- [ ] Landing page loads without errors
- [ ] Click "Get Started" button
- [ ] Signup form appears
- [ ] Fill in test credentials:
  - Name: Test User
  - Email: test@example.com
  - Password: test123456
- [ ] Click "Create Account"
- [ ] Should redirect to dashboard
- [ ] Verify you see "Welcome, Test User!"

### Full Flow Test
- [ ] On dashboard, enter:
  - Meeting Title: "Test Meeting"
  - Google Meet Link: https://meet.google.com/test-demo-link
- [ ] Click "Deploy Bot to Meeting"
- [ ] Should see success message
- [ ] Click "My Meetings" in navbar
- [ ] Should see your test meeting
- [ ] Status should be "Pending" or "Joining"
- [ ] Wait 30 seconds, refresh page
- [ ] Status should change to "Recording"
- [ ] Wait 1 minute, refresh page
- [ ] Status should change to "Completed"
- [ ] Click on meeting card
- [ ] Should see AI summary and transcript

### Admin Dashboard Test (First User Only)
- [ ] Click "Admin" in navbar
- [ ] Should see admin dashboard
- [ ] Verify stats show:
  - Total Users: 1
  - Total Meetings: 1
  - Active Meetings: 0
  - Completed Meetings: 1
- [ ] Verify user table shows your account
- [ ] Verify recent meetings shows your test meeting

---

## Post-Deployment

### 1. Fill in Deployment Links
- [ ] Open `DEPLOYMENT-LINKS.txt`
- [ ] Fill in your Vercel URL
- [ ] Fill in your Render URL
- [ ] Fill in your GitHub repo URL
- [ ] Save the file

### 2. Take Screenshots
- [ ] Landing page
- [ ] Signup page
- [ ] Dashboard with meeting creation
- [ ] Meetings list with status
- [ ] Meeting detail modal
- [ ] Admin dashboard (if first user)
- [ ] Save screenshots for submission

### 3. Prepare Submission
- [ ] Copy live URL from Vercel
- [ ] Copy API URL from Render
- [ ] Read `GENAI-USAGE.md` for submission text
- [ ] Prepare tech stack description
- [ ] List all features implemented

---

## Troubleshooting

### Backend Issues

#### API not responding
- [ ] Check Render dashboard → Logs
- [ ] Verify service is running (not sleeping)
- [ ] Check environment variables are set
- [ ] Try manual deploy from Render dashboard

#### Gemini API errors
- [ ] Verify API key is correct
- [ ] Check API key has no extra spaces
- [ ] Test API key at https://makersuite.google.com
- [ ] Check API quota limits

#### S3 upload errors
- [ ] Verify AWS credentials are correct
- [ ] Check bucket name matches
- [ ] Verify IAM user has S3 permissions
- [ ] Check bucket exists in correct region

### Frontend Issues

#### Can't connect to backend
- [ ] Verify API_URL in index.html is correct
- [ ] Check for typos in URL
- [ ] Verify backend is running
- [ ] Check browser console for CORS errors
- [ ] Try accessing API URL directly in browser

#### Login not working
- [ ] Clear browser localStorage: `localStorage.clear()`
- [ ] Check network tab in browser (F12)
- [ ] Verify API is returning JWT token
- [ ] Try creating new account
- [ ] Check backend logs for errors

#### Page not loading
- [ ] Clear browser cache
- [ ] Try incognito/private mode
- [ ] Check Vercel deployment logs
- [ ] Verify index.html was deployed
- [ ] Check for JavaScript errors in console

---

## Final Verification

### Before Submission
- [ ] Backend API is live and responding
- [ ] Frontend loads without errors
- [ ] Can create account
- [ ] Can login
- [ ] Can create meeting
- [ ] Meeting appears in list
- [ ] Status updates work
- [ ] AI summary generates
- [ ] Admin dashboard works (first user)
- [ ] All screenshots taken
- [ ] All links filled in DEPLOYMENT-LINKS.txt
- [ ] Tested on mobile device
- [ ] Tested on different browser

### Submission Checklist
- [ ] Live URL ready
- [ ] GitHub repo link ready
- [ ] GenAI usage explanation ready
- [ ] Tech stack description ready
- [ ] Features list ready
- [ ] Screenshots ready
- [ ] Tested complete user flow
- [ ] Verified all features work

---

## Success Criteria

Your deployment is successful when:

✅ Backend API responds at `/`
✅ API docs accessible at `/docs`
✅ Frontend loads without errors
✅ Can create account (first user = admin)
✅ Can login successfully
✅ Can create meeting
✅ Meeting appears in "My Meetings"
✅ Status updates from pending → recording → completed
✅ AI summary generates
✅ Admin dashboard shows stats
✅ Can delete meetings
✅ Real-time updates work (refresh to see changes)

---

## Emergency Contacts

### If Deployment Fails

**Render Issues:**
- Check: https://status.render.com
- Docs: https://render.com/docs
- Support: https://render.com/support

**Vercel Issues:**
- Check: https://www.vercel-status.com
- Docs: https://vercel.com/docs
- Support: https://vercel.com/support

**AWS Issues:**
- Check: https://status.aws.amazon.com
- Docs: https://docs.aws.amazon.com
- Support: https://console.aws.amazon.com/support

---

## Time Estimates

- Backend deployment: 10 minutes
- Frontend deployment: 5 minutes
- Testing: 10 minutes
- Screenshots: 5 minutes
- **Total: ~30 minutes**

---

## Next Steps After Deployment

1. ✅ Test all features thoroughly
2. ✅ Take screenshots for submission
3. ✅ Fill in DEPLOYMENT-LINKS.txt
4. ✅ Prepare submission form answers
5. ✅ Submit to internship program
6. ✅ Celebrate! 🎉

---

**Good luck with your deployment and internship submission!** 🚀
