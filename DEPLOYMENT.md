# MPAgent Deployment Guide

This guide explains how to deploy the MPAgent application to Streamlit Cloud.

## Prerequisites

- A GitHub account
- A Streamlit Cloud account (free tier available)
- Your code pushed to a GitHub repository

## Deployment Steps

### 1. Prepare Your Repository

Make sure your repository has the following structure:

```
MPAgent/
├── mockup_app.py     # Main application file
├── requirements.txt  # Python dependencies
├── streamlit_config.py  # Streamlit configuration
└── static/           # Static files (images, etc.)
```

### 2. Deploy to Streamlit Cloud

1. Go to [Streamlit Cloud](https://share.streamlit.io/)
2. Click "New app"
3. Select your repository and branch
4. Set the following configuration:
   - Main file path: `mockup_app.py`
   - Python version: 3.9 (recommended)
5. Click "Deploy!"

### 3. Environment Variables (Optional)

If your app requires API keys or other secrets:

1. In your Streamlit Cloud app settings
2. Go to "Advanced settings"
3. Add your environment variables under "Secrets"

### 4. Updating Your App

To update your deployed app:

1. Push your changes to the connected GitHub repository
2. The app will automatically redeploy
3. Or, manually trigger a redeploy from the Streamlit Cloud dashboard

## Local Development

To run the app locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run mockup_app.py
```

## Troubleshooting

- **App not updating**: Clear your browser cache or try a hard refresh (Ctrl+F5)
- **Dependency issues**: Make sure all dependencies are listed in requirements.txt
- **Memory issues**: If your app uses a lot of memory, consider upgrading your Streamlit Cloud plan

## Support

For issues, please open an issue in the [GitHub repository](https://github.com/Fabbiologia/MPAgent/issues).
