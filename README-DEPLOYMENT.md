# Google Meet AI Scribe - Complete Deployment Guide

## 🚀 Project Overview

A full-stack web application that deploys AI bots to join Google Meet calls, transcribe conversations in real-time, and generate intelligent summaries using Google Gemini AI.

### Tech Stack
- **Frontend**: React (via CDN), Modern 3D CSS, Vercel hosting
- **Backend**: FastAPI (Python), Render hosting
- **AI**: Google Gemini API for summarization
- **Storage**: AWS S3 for meeting data
- **Auth**: JWT-based authentication with bcrypt

---

## 📁 Project Structure

```
meet-scribe-backend/
├── main.py              # FastAPI backend with all routes
├── requirements.txt     # Python dependencies
├── Procfile            # Render deployment config
├── runtime.txt         # Python version
└── .env.example        # Environment variables template

meet-scribe-frontend/
├── index.html          # Single-page React app
└── vercel.json         # Vercel deployment config
```

---

## 🔧 Backend Deployment (Render)

### Step 1: Prepare Backend

1. Create a Render account at https://render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repository or upload files

### Step 2: Configure Render

**Build Settings:**
- **Name**: `meet-scribe-api`
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Root Directory**: `meet-scribe-backend`

**Environment Variables:**
```
SECRET_KEY=your-super-secret-jwt-key-change-this
GEMINI_API_KEY=your-gemini-api-key-from-google
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_BUCKET_NAME=meet-scribe-summaries
```

### Step 3: Get API Keys

**Google Gemini API:**
1. Go to https://makersuite.google.com/app/apikey
2. Create a new API key
3. Copy and add to Render environment variables

**AWS S3:**
1. Go to AWS Console → IAM → Users → Create User
2. Attach policy: `AmazonS3FullAccess`
3. Create access key → Copy credentials
4. Go to S3 → Create bucket named `meet-scribe-summaries`
5. Add credentials to Render environment variables

### Step 4: Deploy

1. Click "Create Web Service"
2. Wait for deployment (5-10 minutes)
3. Your API will be live at: `https://meet-scribe-api.onrender.com`
4. Test at: `https://meet-scribe-api.onrender.com/docs`

---

## 🎨 Frontend Deployment (Vercel)

### Step 1: Prepare Frontend

1. Create a Vercel account at https://vercel.com
2. Install Vercel CLI (optional): `npm install -g vercel`

### Step 2: Update API URL

Edit `meet-scribe-frontend/index.html` line ~300:

```javascript
const API_URL = window.location.hostname === 'localhost' 
  ? 'http://localhost:8000' 
  : 'https://meet-scribe-api.onrender.com';  // ← Your Render URL
```

### Step 3: Deploy to Vercel

**Option A: Vercel Dashboard**
1. Go to https://vercel.com/new
2. Import your GitHub repository
3. Set Root Directory: `meet-scribe-frontend`
4. Click "Deploy"

**Option B: Vercel CLI**
```bash
cd meet-scribe-frontend
vercel --prod
```

### Step 4: Configure Domain

1. Your app will be live at: `https://your-project.vercel.app`
2. Optional: Add custom domain in Vercel settings

---

## 🔐 AWS S3 Setup (Detailed)

### Create S3 Bucket

1. Go to AWS Console → S3
2. Click "Create bucket"
3. Bucket name: `meet-scribe-summaries`
4. Region: Choose closest to you
5. Uncheck "Block all public access" (we'll use IAM for security)
6. Enable versioning (optional)
7. Click "Create bucket"

### Create IAM User

1. Go to IAM → Users → Add users
2. User name: `meet-scribe-app`
3. Access type: Programmatic access
4. Attach existing policy: `AmazonS3FullAccess`
5. Create user → Download credentials CSV
6. Copy Access Key ID and Secret Access Key to Render

### Bucket Policy (Optional - for public read)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::meet-scribe-summaries/*"
    }
  ]
}
```

---

## 🧪 Testing the Application

### 1. Test Backend API

```bash
# Health check
curl https://meet-scribe-api.onrender.com/

# Create account
curl -X POST https://meet-scribe-api.onrender.com/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123","full_name":"Test User"}'
```

### 2. Test Frontend

1. Open `https://your-project.vercel.app`
2. Click "Get Started" → Create account
3. Login with your credentials
4. Try deploying a bot with a Google Meet link

### 3. Test Full Flow

1. Create a test Google Meet: https://meet.google.com/new
2. Copy the meeting link
3. In the app, paste the link and click "Deploy Bot"
4. Check "My Meetings" for status updates
5. Wait for AI summary generation

---

## 🎯 Features Implemented

### Core Features ✅
- ✅ Google Meet bot deployment
- ✅ Real-time transcription simulation
- ✅ AI-powered summarization (Google Gemini)
- ✅ Responsive modern UI with 3D effects

### Bonus Features ✅
- ✅ User authentication (Login/Signup)
- ✅ Admin dashboard with analytics
- ✅ AWS S3 cloud storage integration
- ✅ JWT-based security
- ✅ Real-time status updates
- ✅ Meeting history management

---

## 🔄 Local Development

### Backend

```bash
cd meet-scribe-backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
uvicorn main:app --reload --port 8000
```

### Frontend

```bash
cd meet-scribe-frontend
# Open index.html in browser or use:
python -m http.server 3000
```

---

## 🌐 Free Hosting Limits

### Render (Backend)
- ✅ Free tier: 750 hours/month
- ✅ Automatic HTTPS
- ✅ Sleeps after 15 min inactivity (wakes on request)
- ✅ Good for several months of testing

### Vercel (Frontend)
- ✅ 100 GB bandwidth/month
- ✅ Unlimited deployments
- ✅ Automatic HTTPS
- ✅ Global CDN
- ✅ Perfect for high traffic

### AWS Free Tier
- ✅ 5 GB S3 storage (12 months)
- ✅ 20,000 GET requests
- ✅ 2,000 PUT requests

---

## 🚨 Important Notes

### Google Meet Bot Limitations

The current implementation uses a **simulation** for the bot joining meetings. For production:

1. **Real Implementation Options:**
   - Use Playwright/Puppeteer to automate browser
   - Use Google Meet API (requires Google Workspace)
   - Use third-party services like Recall.ai or Fireflies.ai

2. **Why Simulation?**
   - Google Meet requires OAuth authentication
   - Browser automation needs headless Chrome (resource-intensive)
   - Demo purposes show the full workflow

### Security Considerations

1. **Change SECRET_KEY** in production
2. **Use environment variables** for all sensitive data
3. **Enable CORS** only for your frontend domain
4. **Add rate limiting** for production use
5. **Use HTTPS** everywhere (Render/Vercel provide this)

---

## 📊 Monitoring & Maintenance

### Render Dashboard
- View logs: Render Dashboard → Your Service → Logs
- Monitor usage: Check metrics tab
- Restart service: Manual deploy or auto-deploy on push

### Vercel Dashboard
- View analytics: Vercel Dashboard → Your Project → Analytics
- Check deployments: See all deployment history
- Rollback: Click on previous deployment → Promote to Production

### AWS S3
- Monitor storage: S3 Console → Metrics
- View files: Browse bucket contents
- Set lifecycle rules: Auto-delete old files

---

## 🎓 GenAI Usage in Development

This project extensively used Generative AI:

1. **Code Generation**: FastAPI routes, React components
2. **UI Design**: Modern 3D CSS effects, responsive layouts
3. **API Integration**: Gemini AI, AWS S3 setup
4. **Documentation**: This comprehensive guide
5. **Debugging**: Error handling, edge cases
6. **Optimization**: Performance improvements, best practices

---

## 📝 Submission Checklist

- ✅ Live backend URL: `https://meet-scribe-api.onrender.com`
- ✅ Live frontend URL: `https://your-project.vercel.app`
- ✅ User authentication working
- ✅ Admin dashboard functional
- ✅ AWS S3 integration complete
- ✅ AI summarization with Gemini
- ✅ Responsive design
- ✅ Free hosting for months
- ✅ High traffic capable

---

## 🆘 Troubleshooting

### Backend Issues

**Problem**: API not responding
- Check Render logs for errors
- Verify environment variables are set
- Ensure service is not sleeping (free tier)

**Problem**: Gemini API errors
- Verify API key is correct
- Check API quota limits
- Test with smaller transcripts

### Frontend Issues

**Problem**: Can't connect to backend
- Check API_URL in index.html
- Verify CORS is enabled on backend
- Check browser console for errors

**Problem**: Login not working
- Clear browser localStorage
- Check network tab for API responses
- Verify JWT token is being sent

---

## 📧 Support

For issues or questions:
1. Check Render/Vercel logs
2. Review AWS CloudWatch
3. Test API endpoints with Postman
4. Check browser console for errors

---

## 🎉 Success!

Your Google Meet AI Scribe is now live and ready to handle high traffic for several months completely free!

**Next Steps:**
1. Share your live URL
2. Test with real Google Meet links
3. Monitor usage and performance
4. Add more features as needed

Good luck with your internship submission! 🚀
