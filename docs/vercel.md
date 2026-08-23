# Deploying the Frontend to Vercel

This project has a static frontend in the `frontend/` folder and a Python FastAPI backend that runs separately. Vercel is best for hosting the static frontend. Use the steps below to deploy the frontend and route API calls to your backend.

1. Prepare a publicly reachable backend

- Host your backend somewhere reachable from the internet (Render, Railway, Fly.io, a VPS, or a Docker host). The backend must expose the API at `https://your-backend.example.com`.
- Ensure the backend uses HTTPS and that CORS allows requests from your frontend domain.

2. Configure `vercel.json`

- Open `vercel.json` at the repository root and replace `REPLACE_WITH_BACKEND_URL` with your backend URL (no trailing slash), e.g. `https://api.example.com`.

3. Deploy the frontend

- Install the Vercel CLI and login:

```bash
npm i -g vercel
vercel login
```

- From the repository root, deploy the `frontend` folder as a new project:

```bash
cd frontend
vercel --prod
```

During the interactive deploy, set the project root to the current directory. Alternatively, in the Vercel dashboard import the repo and set the build root to `frontend`.

4. Environment / API base URL

- If your frontend's JavaScript needs an API base URL, either hardcode the deployed backend URL into your JS config or set a Vercel environment variable and reference it in your build. The static app will call `/api/...` which the `vercel.json` rewrite maps to the backend URL.

5. Backend hosting recommendations

- If you want me to deploy the backend too, pick a target: `Render`, `Railway`, `Fly.io`, or `Docker host` and I will prepare the config and deployment steps.

6. Verify

- After deployment, open your Vercel frontend URL and perform a few API actions (login, fetch practice) to confirm the rewrite works and CORS is configured.
