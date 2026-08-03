# Deploying the Inception runtime (deploy-READY, not deployed)

This packages the running Inception service (`src/inception/`) for the cluster using the estate's
wave-deploy discipline. **Nothing here is applied to a cluster** — the live-traffic cutover is a
held, irreversible decision.

## What's here
- `Dockerfile` — non-root (uid 10001), read-only rootfs, durable event log on the mounted `/data`
  PVC. Entrypoint: `uvicorn inception.service:app` (the exact command validated against a live
  server locally).
- `deploy/` — a **self-contained** kustomize overlay (INV-DEP-10): `base-support/` renders the
  ServiceAccount+RBAC, ConfigMap, PVC (durable log), and NetworkPolicy; `base/` renders the
  Deployment + Service. `kubectl kustomize deploy/base` renders all 8 objects with no dangling
  reference. `tools/verify_deploy_self_contained.py` proves this in CI (kubectl-free, fail-closed).

## To actually deploy (the held steps — require your go)
1. Build + push the image and **pin its digest** (INV-DEP-1/6) — the release train's job, not done
   here. The manifest image ref is `...:RELEASE_TRAIN_PINS_DIGEST` on purpose (NOT a fake sha256,
   to avoid the ImagePullBackOff trap).
2. `kubectl apply -k deploy/base` into the `inception` namespace (blue-green/rollout optional).
3. **Live-traffic cutover** — explicit, irreversible; needs a real target namespace and your go.

Read-only only: the runtime exposes no world-changing adapter (Phases 4-6).
