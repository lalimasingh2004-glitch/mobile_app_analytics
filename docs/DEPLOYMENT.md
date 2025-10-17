# Deployment Guide

## Live Dashboard
**URL:** https://mobile-app-analytics.onrender.com

## Deployment Platform
- **Platform:** Render.com
- **Plan:** Free Tier
- **Region:** US West (Oregon)
- **Runtime:** Python 3.10.14

## Deployment Process
1. Connected GitHub repository
2. Configured build settings
3. Added environment variables
4. Auto-deploys on push to `main` branch

## Performance
- **Cold Start:** few minutes (first load)
- **Warm Load:** <10 seconds
- **Uptime:** 99.9% (Render.com SLA)

## Monitoring
View logs: https://dashboard.render.com

## Re-deployment
Push to GitHub main branch triggers auto-deploy.