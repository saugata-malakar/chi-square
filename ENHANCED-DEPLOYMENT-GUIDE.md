# 🚀 Enhanced Deployment Guide - Complete Setup

## 📋 Overview

This guide covers deploying the ENHANCED version with:
- ✅ Google OAuth Authentication
- ✅ Stripe Payment Integration
- ✅ Advanced Admin Dashboard
- ✅ User Management System
- ✅ Subscription Plans
- ✅ Analytics & Statistics

---

## 🔧 Prerequisites

### Required Accounts
1. **Render** - Backend hosting (https://render.com)
2. **Vercel** - Frontend hosting (https://vercel.com)
3. **Google Cloud** - OAuth credentials (https://console.cloud.google.com)
4. **Stripe** - Payment processing (https://stripe.com)
5. **AWS** - S3 storage (https://aws.amazon.com)
6. **Google AI Studio** - Gemini API (https://makersuite.google.com)

---

## 📝 Step 1: Google OAuth Setup

### 1.1 Create Google Cloud Project
1. Go to https://console.cloud.google.com
2. Create new project: "Meet Scribe AI"
3. Enable Google+ API

### 1.2 Create OAuth Credentials
1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth 2.0 Client ID"
3. Application type: "Web application"
4. Name: "Meet Scribe Web Client"
5. Authorized JavaScript origins:
   ```
   http://localhost:3000
   https://your-project.vercel.app
   ```
6. Authorized redirect URIs:
   ```
   http://localhost:3000/auth/callback
   https://your-project.vercel.app/auth/callback
   ```
7. Click "Create"
8. **Save Client ID and Client Secret**

---

## 💳 Step 2: Stripe Setup

### 2.1 Create Stripe Account
1. Go to https://dashboard.stripe.com/register
2. Complete account setup
3. Switch to "Test mode" (toggle in top right)

### 2.2 Create Products & Prices
1. Go to "Products" → "Add product"

**Pro Plan:**
- Name: "Pro Plan"
- Description: "Unlimited meetings, 3-hour limit"
- Price: $29/month
- Copy the Price ID (starts with `price_`)

**Enterprise Plan:**
- Name: "Enterprise Plan"
- Description: "Unlimited everything + priority support"
- Price: $99/month
- Copy the Price ID

### 2.3 Get API Keys
1. Go to "Developers" → "API keys"
2. Copy "Publishable key" (starts with `pk_test_`)
3. Copy "Secret key" (starts with `sk_test_`)

### 2.4 Setup Webhook
1. Go to "Developers" → "Webhooks"
2. Click "Add endpoint"
3. Endpoint URL: `https://your-api.onrender.com/api/payments/webhook`
4. Events to send: Select "checkout.session.completed"
5. Copy "Signing secret" (starts with `whsec_`)

---

## ☁️ Step 3: AWS S3 Setup

### 3.1 Create S3 Bucket
1. Go to AWS Console → S3
2. Click "Create bucket"
3. Bucket name: `meet-scribe-summaries-prod`
4. Region: Choose closest to you
5. Uncheck "Block all public access"
6. Enable versioning
7. Click "Create bucket"

### 3.2 Create IAM User
1. Go to IAM → Users → "Add users"
2. User name: `meet-scribe-app`
3. Access type: "Programmatic access"
4. Attach policy: "AmazonS3FullAccess"
5. Create user
6. **Download credentials CSV**
7. Save Access Key ID and Secret Access Key

---

## 🤖 Step 4: Google Gemini API

1. Go to https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Select your Google Cloud project
4. Copy the API key

---

## 🖥️ Step 5: Deploy Backend (Render)

### 5.1 Prepare Files
1. Use `meet-scribe-backend/main_enhanced.py`
2. Rename it to `main.py` or update Procfile

### 5.2 Deploy to Render
1. Go to https://dashboard.render.com
2. Click "New +" → "Web Service"
3. Connect GitHub or upload files
4. Configuration:
   - Name: `meet-scribe-api-enhanced`
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main_enhanced:app --host 0.0.0.0 --port $PORT`

### 5.3 Environment Variables
Add these in Render dashboard:

```env
SECRET_KEY=generate-random-32-char-string
GEMINI_API_KEY=your-gemini-api-key
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_BUCKET_NAME=meet-scribe-summaries-prod
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret
STRIPE_SECRET_KEY=sk_test_your-stripe-secret-key
STRIPE_PUBLISHABLE_KEY=pk_test_your-stripe-publishable-key
STRIPE_WEBHOOK_SECRET=whsec_your-webhook-secret
FRONTEND_URL=https://your-project.vercel.app
```

### 5.4 Deploy
1. Click "Create Web Service"
2. Wait 5-10 minutes
3. Copy your API URL: `https://meet-scribe-api-enhanced.onrender.com`

---

## 🎨 Step 6: Deploy Frontend (Vercel)

### 6.1 Update Configuration
Edit `meet-scribe-frontend/index_enhanced.html`:

```javascript
// Update these constants (around line 100)
const API_URL = 'https://meet-scribe-api-enhanced.onrender.com';
const GOOGLE_CLIENT_ID = 'your-google-client-id.apps.googleusercontent.com';
const STRIPE_PUBLISHABLE_KEY = 'pk_test_your-stripe-publishable-key';
```

### 6.2 Deploy to Vercel
1. Go to https://vercel.com/new
2. Import your repository
3. Configuration:
   - Framework: Other
   - Root Directory: `meet-scribe-frontend`
   - Build Command: (leave empty)
   - Output Directory: (leave empty)

4. Environment Variables (optional):
   ```
   NEXT_PUBLIC_API_URL=https://meet-scribe-api-enhanced.onrender.com
   NEXT_PUBLIC_GOOGLE_CLIENT_ID=your-client-id
   ```

5. Click "Deploy"
6. Copy your URL: `https://your-project.vercel.app`

---

## ✅ Step 7: Testing

### 7.1 Test Backend
```bash
# Health check
curl https://meet-scribe-api-enhanced.onrender.com/health

# Should return service status
```

### 7.2 Test Google OAuth
1. Open your Vercel URL
2. Click "Sign in with Google"
3. Complete OAuth flow
4. Should redirect to dashboard

### 7.3 Test Stripe Payment
1. Login to your account
2. Go to "Upgrade" or "Pricing"
3. Click "Upgrade to Pro"
4. Use test card: `4242 4242 4242 4242`
5. Expiry: Any future date
6. CVC: Any 3 digits
7. Should redirect to success page

### 7.4 Test Meeting Creation
1. On dashboard, enter:
   - Title: "Test Meeting"
   - Link: https://meet.google.com/test-link
2. Click "Deploy Bot"
3. Check "My Meetings"
4. Wait for AI summary

### 7.5 Test Admin Dashboard
1. First user is automatically admin
2. Click "Admin" in navbar
3. Verify statistics display
4. Check user management table

---

## 🔐 Security Checklist

- [ ] Changed SECRET_KEY to random string
- [ ] Using HTTPS for all URLs
- [ ] Stripe in test mode initially
- [ ] Google OAuth redirect URIs match exactly
- [ ] AWS S3 bucket has proper permissions
- [ ] Environment variables not in code
- [ ] CORS configured for your domain only

---

## 📊 Features Verification

### Core Features
- [ ] Google OAuth login works
- [ ] Email/password login works
- [ ] Meeting creation works
- [ ] AI summary generates
- [ ] Real-time status updates

### Payment Features
- [ ] Stripe checkout opens
- [ ] Test payment processes
- [ ] Subscription updates in database
- [ ] Free plan limits enforced
- [ ] Upgrade flow works

### Admin Features
- [ ] Admin dashboard accessible
- [ ] User list displays
- [ ] Statistics accurate
- [ ] Can update user roles
- [ ] Can delete users
- [ ] Analytics charts work

---

## 🚨 Troubleshooting

### Google OAuth Issues
**Error: "redirect_uri_mismatch"**
- Verify redirect URI in Google Console matches exactly
- Include protocol (https://)
- No trailing slash

**Error: "invalid_client"**
- Check GOOGLE_CLIENT_ID is correct
- Verify client secret in backend

### Stripe Issues
**Error: "No such price"**
- Update price IDs in `main_enhanced.py`
- Use actual Stripe price IDs from dashboard

**Webhook not receiving events**
- Verify webhook URL is correct
- Check webhook signing secret
- Test with Stripe CLI: `stripe listen --forward-to localhost:8000/api/payments/webhook`

### Backend Issues
**Error: "Service Unavailable"**
- Check Render logs
- Verify all environment variables set
- Ensure service is not sleeping

---

## 📈 Monitoring

### Render Dashboard
- View logs: Dashboard → Service → Logs
- Monitor metrics: CPU, Memory usage
- Check deployment history

### Stripe Dashboard
- Monitor payments: Dashboard → Payments
- View customers: Dashboard → Customers
- Check webhooks: Developers → Webhooks → Events

### Google Cloud Console
- Monitor OAuth usage: APIs & Services → Dashboard
- Check quotas: IAM & Admin → Quotas

---

## 🎯 Production Checklist

Before going live:

- [ ] Switch Stripe to live mode
- [ ] Update Stripe keys in environment
- [ ] Update webhook URL to production
- [ ] Set up custom domain (optional)
- [ ] Enable Render auto-deploy
- [ ] Set up monitoring/alerts
- [ ] Test all features in production
- [ ] Prepare support documentation

---

## 💰 Cost Breakdown

### Free Tier Limits
- **Render**: 750 hours/month
- **Vercel**: 100GB bandwidth
- **AWS S3**: 5GB storage (12 months)
- **Google OAuth**: Free
- **Stripe**: 2.9% + $0.30 per transaction
- **Gemini API**: 60 requests/minute free

### Estimated Monthly Cost
- **Development**: $0
- **Production (low traffic)**: $0-10
- **Production (high traffic)**: $20-50

---

## 🎉 Success!

Your enhanced Google Meet AI Scribe is now live with:
✅ Google OAuth authentication
✅ Stripe payment processing
✅ Advanced admin dashboard
✅ User management system
✅ Subscription plans
✅ Analytics and statistics

**Next Steps:**
1. Test all features thoroughly
2. Take screenshots for submission
3. Prepare demo video (optional)
4. Submit to internship program

---

## 📞 Support Resources

- **Render Docs**: https://render.com/docs
- **Vercel Docs**: https://vercel.com/docs
- **Google OAuth**: https://developers.google.com/identity/protocols/oauth2
- **Stripe Docs**: https://stripe.com/docs
- **AWS S3 Docs**: https://docs.aws.amazon.com/s3/

---

**Congratulations on deploying a production-ready application!** 🚀
