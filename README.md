# iCare EIDON vs Optos Sales Gallery

Static, password-gated webpage for field reps and tradeshows.

## Included
- Extracted images from provided `.docx` files
- Case-by-case gallery page
- Simple password gate (client-side)

## Current password
`Optossux`

> Note: This is lightweight client-side protection (good for casual gating, not high-security PHI use).

## Update password
1. Generate SHA-256 hash of new password
2. Replace `PASSWORD_HASH` in `public/index.html`

Example:
```bash
python3 - <<'PY'
import hashlib
print(hashlib.sha256('NEW_PASSWORD'.encode()).hexdigest())
PY
```

## Rebuild content from source docs
Put `.docx` files in `source_docs/` then run:
```bash
python3 scripts/build_site.py
```

## Deploy (GitHub Pages)
This repo includes a Pages workflow that publishes from `public/`.

## Deploy (Netlify, preferred neutral URL)
This repo includes `netlify.toml` so Netlify can deploy directly from GitHub.
- Publish dir: `public`
- Build command: `python3 scripts/build_site.py`

Suggested Netlify site name: `eidonimages` (URL: `https://eidonimages.netlify.app` if available)
