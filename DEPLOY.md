# Deploying to Streamlit Community Cloud

The app is **cloud-ready**: the prebuilt `data/scpd.duckdb` and `data/rutas.kml`
are committed, so it runs with **no 6 GB source ZIP and no pipeline step**. The
ZIP-only actions (re-run pipeline, build catalog, load source tables) hide
themselves when the ZIP isn't present.

## One-time setup

> **Where this app actually runs: Streamlit Community Cloud.**
> The repo's only deploy webhook is `share.streamlit.io`. `railway.json` and the
> `Dockerfile` are present and work, but **nothing is connected to Railway** — a
> push does not deploy there. Wire Railway up before relying on it.
>
> The repo must stay **public** for Streamlit Community Cloud to pull it on a
> free account. Making it private silently stops updates: the webhook still
> returns 200, but the app keeps serving the last build it could read.

1. Go to **https://share.streamlit.io** and sign in with the GitHub account
   that has access to the `Equal-Green` org (**grant-flaming-owl**).
2. **Authorize Streamlit for the private repo:** during sign-in, grant the
   Streamlit GitHub app access to the **Equal-Green** organization (GitHub →
   Settings → Applications → Streamlit → grant `Equal-Green`). Required because
   the repo is private.
3. Click **Create app → Deploy a public app from GitHub → Deploy now**
   (it works for private repos too once access is granted).

## App settings

| Field | Value |
|---|---|
| Repository | `Equal-Green/scpd-analytics` |
| Branch | `main` |
| Main file path | `dashboard/app.py` |
| Python version (Advanced) | `3.12` |

No secrets are required. `requirements.txt` is auto-detected.

Click **Deploy**. First build installs dependencies and starts the app on the
committed DuckDB — it opens directly on the Cover page (no pipeline run).

## Notes & limits

- **Resources:** the 97 MB DuckDB is memory-mapped, not loaded into RAM, so it
  fits Community Cloud comfortably.
- **Map tiles** need internet (they load from OpenStreetMap); the polygons and
  routes render regardless.
- **Refreshing the data:** re-run the pipeline locally with the source ZIP, then
  commit the updated `data/scpd.duckdb` and push — the cloud app redeploys.
- **Updating:** every push to `main` auto-redeploys.

## Alternative hosts

The same app runs on any container host (Google Cloud Run, Render, Railway,
Azure Container Apps). Use `streamlit run dashboard/app.py --server.port $PORT`
as the start command; bake `data/scpd.duckdb` into the image.
