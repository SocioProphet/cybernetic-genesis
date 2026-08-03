# Deploy decisions — Inception GAR/WIF wiring (ADR)

Records the reasoning behind the build+push retarget (`.github/workflows/image.yml`) and the prod
overlay (`deploy/overlays/prod/`). The companion ArgoCD Application lives in **prophet-platform**
(`deploy/argocd/inception-services.yaml`) with its own note.

Status: **deploy-READY, not deployed.** No cluster is touched by merging this. No prod namespace is
created, no traffic is cut.

## 1. GAR *and* ghcr, not ghcr alone

The estate DEPLOYMENT registry is Google Artifact Registry —
`us-central1-docker.pkg.dev/socioprophet-platform/socioprophet/<service>`. The live GKE nodes have
Workload Identity auth to GAR and **none to ghcr**, so a ghcr-only digest 401s on a real
`kubectl apply` (the apply-caught registry mismatch the estate already paid for; see
`prophet-platform/.github/workflows/search-orchestrator-image.yml`). The deployable digest therefore
**must** land in GAR.

We kept the ghcr push as the public build/validation mirror rather than dropping it. That is the one
place we diverge from search-orchestrator (which is GAR-only). Rationale: this repo is public MIT and
ghcr is its existing, world-readable artifact home; the deploy path never reads ghcr (it pins the GAR
digest), so the extra push costs nothing operationally and keeps a public mirror.

> **Open question for the reviewer:** keep the dual-push, or drop ghcr to match the estate's GAR-only
> convention exactly? Either is a one-line change to the `tags:` list.

## 2. Digest pin, never a moving tag

`deploy/overlays/prod/kustomization.yaml` pins the image by `@sha256:` digest via kustomize `images:`.
`:latest` + `imagePullPolicy: IfNotPresent` means the kubelet reuses the node cache forever — a fixed
image never rolls, and even `rollout restart` does not re-pull. The pinned digest
(`sha256:423b4ae6…`, tag `81fd3cc-amd64`) is the one **actually validated** Ready+serving on the live
GKE cluster in `inception-validation`, then torn down. We pin the validated digest, not "whatever the
next build makes"; a future release train rebuilds and re-pins here.

## 3. linux/amd64 only

GKE nodes are amd64; an arm64 image (this repo's dev machines are Apple silicon) crash-loops with
`exec format error`. The build platform is pinned to `linux/amd64`.

## 4. WIF, no PATs; org-allowlisted actions only

GAR auth is minted in-CI from the OIDC token via `google-github-actions/auth@v2` (no long-lived key,
no committed credential). The workflow uses only actions already in heavy use across prophet-platform
workflows — `actions/checkout@v4`, `docker/setup-buildx-action@v3`, `google-github-actions/auth@v2`,
`docker/login-action@v3`, `docker/build-push-action@v6` — so it clears any org action allowlist by
construction. Provider + service account are read from the same secret **names** the estate uses:
`GCP_WORKLOAD_IDENTITY_PROVIDER`, `GCP_SERVICE_ACCOUNT`.

## 5. Deliberately held (needs owner action, NOT in this PR)

- **IAM / WIF binding (BLOCKER).** Those two secrets are today **repo-level on prophet-platform** and
  there are **no org-level Actions secrets**, so `cybernetic-genesis` cannot yet authenticate. Before
  this workflow's GAR push can succeed the owner must, out of band:
  1. add `GCP_WORKLOAD_IDENTITY_PROVIDER` + `GCP_SERVICE_ACCOUNT` to this repo (or promote them to
     org-level with `cybernetic-genesis` in scope), and
  2. add a Workload Identity attribute binding letting the `SocioProphet/cybernetic-genesis` OIDC
     subject impersonate that service account, with `roles/artifactregistry.writer` on the
     `socioprophet` GAR repo.
  This PR references the secret names so it works with **zero code change** once the binding exists.
- **Prod namespace / first sync / traffic.** No namespace is created, no ingress is added, no traffic
  is cut. Those are held, owner-only, and (for cutover) irreversible.
