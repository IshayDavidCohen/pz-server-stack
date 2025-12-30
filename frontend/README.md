# Project Zomboid Server Stack - Frontend

A React + Vite + TypeScript frontend for the Project Zomboid Server Stack whitelist system.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Add your safehouse video:
   - Place your Project Zomboid safehouse video file at `public/safehouse-video.mp4`
   - The video should be in MP4 format
   - It will play as a background with VHS grain overlay effect

3. Start the development server:
```bash
npm run dev
```

4. Build for production:
```bash
npm run build
```

## Features

- **Safehouse Page**: Landing page with "Join Safehouse" and "Grant Access" buttons
- **Whitelister Page**: Form to request whitelist access with username and optional note
- **Project Zomboid Aesthetic**: Dark, gritty theme with VHS grain effects
- **API Integration**: Connects to FastAPI backend at `http://localhost:8000/whitelist/request`

## API Endpoint

The frontend expects a FastAPI backend running at `http://localhost:8000` with the following endpoint:

- `POST /whitelist/request`
  - Body: `{ "username": string, "note": string }`
  - Response: `{ "ok": boolean, "message": string, "request_id": string }`

## Components

- `Button`: Reusable button with primary/secondary variants
- `Input`: Accessible input component with validation
- `Card`: Container component with distressed styling
- `VideoBackground`: Video background with VHS overlay effect

