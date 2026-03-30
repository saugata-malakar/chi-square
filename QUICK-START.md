# 🚀 Quick Start Guide - Google Meet AI Scribe

## ⚡ 5-Minute Deployment

### Prerequisites
- GitHub account
- Render account (free): https://render.com
- Vercel account (free): https://vercel.com
- Google Gemini API key: https://makersuite.google.com/app/apikey
- AWS account (optional, for S3): https://aws.amazon.com

---

## Step 1: Deploy Backend (3 minutes)

1. **Go to Render**: https://dashboard.render.com/
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repo or upload files
4. **Configure:**
   - Name: `meet-scribe-api`
   - Root Directory: `meet-scribe-backend`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

5. **Add Environment Variables:**
   ```
   SECRET_KEY=your-random-secret-key-here-change-this
   GEMINI_API_KEY=your-gemini-api-key
   AWS_ACCESS_KEY_ID=your-aws-key (optional)
   AWS_SECRET_ACCESS_KEY=your-aws-secret (optional)
   AWS_BUCKET_NAME=meet-scribe-summaries (optional)
   ```

6. Click **"Create Web Service"**
7. Wait 5-10 minutes for deployment
8. Copy your API URL: `https://meet-scribe-api.onrender.com`

---

## Step 2: Deploy Frontend (2 minutes)

1. **Update API URL** in `meet-scribe-frontend/index.html`:
   ```javascript
   const API_URL = 'https://meet-scribe-api.onrender.com'; // Your Render URL
   ```

2. **Go to Vercel**: https://vercel.com/new
3. Import your GitHub repository
4. **Configure:**
   - Root Directory: `meet-scribe-frontend`
   - Framework Preset: Other
5. Click **"Deploy"**
6. Your app is live at: `https://your-project.vercel.app`

---

## Step 3: Test Your App (1 minute)

1. Open your Vercel URL
2. Click **"Get Started"** → Create account
3. Login with your credentials
4. Create a test meeting:
   - Title: "Test Meeting"
   - Link: `https://meet.google.com/test-link`
5. Click **"Deploy Bot"**
6. Check **"My Meetings"** for status

---

## 🎉 Done!

Your Google Meet AI Scribe is now live and ready to use!

### What You Have:
✅ Live backend API with authentication
✅ Beautiful 3D frontend interface
✅ AI-powered meeting summaries
✅ Admin dashboard
✅ Free hosting for months
✅ High traffic capability

### Next Steps:
1. Get a real Gemini API key for AI summaries
2. Set up AWS S3 for cloud storage (optional)
3. Share your live URL
4. Test with real Google Meet links

---

## 🆘 Quick Troubleshooting

### Backend not responding?
- Check Render logs: Dashboard → Your Service → Logs
- Verify environment variables are set
- Wait for service to wake up (free tier sleeps after 15 min)

### Frontend can't connect?
- Check API_URL in index.html matches your Render URL
- Open browser console (F12) for errors
- Try clearing browser cache

### Login not working?
- Clear localStorage: Console → `localStorage.clear()`
- Check network tab for API responses
- Verify backend is running

---

## 📝 Important URLs

- **Backend API**: https://meet-scribe-api.onrender.com
- **API Docs**: https://meet-scribe-api.onrender.com/docs
- **Frontend**: https://your-project.vercel.app
- **Render Dashboard**: https://dashboard.render.com
- **Vercel Dashboard**: https://vercel.com/dashboard

---

## 🔑 Get API Keys

### Google Gemini (Required for AI):
1. Go to: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy and add to Render environment variables
4. Restart your Render service

### AWS S3 (Optional for storage):
1. Go to: https://console.aws.amazon.com/iam/
2. Create user with S3 access
3. Generate access key
4. Create S3 bucket: `meet-scribe-summaries`
5. Add credentials to Render

---

## 💰 Cost Breakdown

### Render (Backend)
- **Free Tier**: 750 hours/month
- **Cost**: $0/month for testing
- **Limits**: Sleeps after 15 min inactivity

### Vercel (Frontend)
- **Free Tier**: 100 GB bandwidth
- **Cost**: $0/month
- **Limits**: None for personal projects

### AWS S3 (Optional)
- **Free Tier**: 5 GB storage (12 months)
- **Cost**: $0/month for first year
- **After**: ~$0.10/month for 5 GB

### Google Gemini
- **Free Tier**: 60 requests/minute
- **Cost**: $0/month for testing
- **Limits**: Rate limited

**Total Monthly Cost: $0** ✨

---

## 📊 Features Checklist

### Core Features
- ✅ Google Meet bot deployment
- ✅ Real-time transcription
- ✅ AI summarization (Gemini)
- ✅ Responsive UI

### Bonus Features
- ✅ User authentication
- ✅ Admin dashboard
- ✅ Cloud storage (S3)
- ✅ Meeting history
- ✅ Real-time updates
- ✅ 3D modern design

---

## 🎓 For Internship Submission

### What to Submit:
1. **Live URL**: Your Vercel frontend URL
2. **GenAI Usage**: See `GENAI-USAGE.md`
3. **Screenshots**: Take screenshots of:
   - Landing page
   - Dashboard
   - Meeting creation
   - Meeting summary
   - Admin panel

### Submission Form Fields:
- **Live URL**: `https://your-project.vercel.app`
- **GitHub Repo**: Your repository link
- **GenAI Usage**: "Used AI for full-stack development, see GENAI-USAGE.md"
- **Tech Stack**: "React, FastAPI, Google Gemini, AWS S3, Render, Vercel"

---

## 🚀 Advanced: Local Development

### Run Backend Locally:
```bash
cd meet-scribe-backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your keys
uvicorn main:app --reload --port 8000
```

### Run Frontend Locally:
```bash
cd meet-scribe-frontend
# Open index.html in browser or:
python -m http.server 3000
```

---

## 📞 Support

If you encounter issues:
1. Check the logs (Render/Vercel dashboards)
2. Review `README-DEPLOYMENT.md` for detailed steps
3. Test API endpoints at `/docs`
4. Check browser console for errors

---

## 🎉 Success Indicators

Your deployment is successful when:
- ✅ Backend API responds at `/`
- ✅ Frontend loads without errors
- ✅ You can create an account
- ✅ You can login
- ✅ You can create a meeting
- ✅ Meeting appears in "My Meetings"
- ✅ Admin dashboard shows stats (if admin)

---

**Congratulations! Your Google Meet AI Scribe is live!** 🎊

Now go submit your internship application with confidence! 💪
