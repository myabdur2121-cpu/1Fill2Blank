# AGENTS.md — 1Fill2Blank projects

This repo contains video projects. The reusable workflow ("skill") and tools live in
the separate **1Fill2Blank-Tools** repo — read its `AGENTS.md` first, then the
relevant `skills/*/SKILL.md`, then this project's `README.md` + `project_config.json`.

Project rules:
- Reply to the owner in Bangla by default; short update at every major step.
- Each video variant (e.g. generated voice vs `my_voice`) keeps its own subfolder
  with its own `project_config.json`, manifests and notes. Do not mix variants.
- Never commit generated media (WAV stems, renders, Manim `media/`), venvs or caches.
  Final MP4s go to GitHub Releases.
- Do not overwrite a base scene with a production variant; derive/generate the
  production scene and keep the builder/adapter with the variant.
- Corrections from the owner come as timestamps; change the manifest/config,
  recompute pads and re-render. Never hand-edit a final MP4.
- No push and no delete/move without the owner's explicit approval. No tokens in files, ever.
