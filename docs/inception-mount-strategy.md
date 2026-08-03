# InceptionMountStrategy — the Podman mount-type contract

Docker's *Manage data* model gives three mount types. Applied to the **sovereign Podman
runtime** (Podman, not Docker), each maps to a specific durability posture:

| Mount type | Meaning | Durability | Host-coupled? |
| --- | --- | --- | --- |
| **named volume** | sovereign-managed store; Podman owns the name and location | durable | **no** |
| **bind** | a scoped host path mounted into the container | caller's choice | yes (a real path) |
| **tmpfs** | memory-only filesystem | ephemeral (dies with the container) | no |

The contract binds each **agent-execution context** to the *one* admissible mount type, so a
wrong pairing is unrepresentable, not merely discouraged.

## The mapping (the teeth)

| Context | Mount type | Rule |
| --- | --- | --- |
| `task_execution` | **tmpfs** | Ephemeral. MUST NOT persist. A task on a durable volume/bind is **REJECTED** *unless* `declared_durable: true` is set explicitly. |
| `userspace` | **volume** | Durable user state. tmpfs ⇒ data loss ⇒ REJECTED; bind ⇒ host-coupled durable state ⇒ REJECTED. |
| `chat` | **volume** | as above |
| `workspace` | **volume** | as above |
| `project` | **volume** | Durable project state. (Project *source code* is mounted read-only via a `directory` context scoped to the project — see below.) |
| `directory` | **bind** | A scoped host directory / project source. Read-only or scoped-write, and **NEVER through a symlink**. |

Two more invariants every mount carries:

1. **Scope.** `scope_ref` is required and non-empty, and its namespace MUST match the context
   (`chat:…` for `chat`, `workspace:…` for `workspace`, `dir:…` for `directory`, `task:…`,
   `user:…`, `project:…`). A mount cannot bind one scope's data under another context —
   **cross-scope leakage is unrepresentable**.
2. **Symlink safety.** For a `bind`, `symlink_safe` must be declared `true`, and the verifier
   **proves it against the real filesystem**: if the `source` resolves through a symlink the
   mount is REJECTED regardless of the claim (`feedback_never_write_through_symlink` —
   the claim is never trusted, the artifact is verified).

## Where the teeth live

- **Structural** — `schemas/inception_mount_strategy.schema.json` (JSON Schema draft 2020-12):
  enum coherence (`tmpfs⇒ephemeral`, `volume⇒durable`), required `scope_ref`, `bind` requires
  `source`, the context→mount-type mapping, and the task-persistence lock.
- **Semantic** — `tools/verify_mount_strategy.py`: the symlink real-resolution and the
  scope-namespace coherence, i.e. the checks JSON Schema cannot see. It validates against the
  schema first, then applies these. `project_to_podman()` is **fail-closed**: it refuses to
  render a mount that does not pass `evaluate()`.

## The Podman projection

`tools/verify_mount_strategy.py project <instance.json>` renders an admissible mount to a
single `podman --mount` argument:

| Context / type | Projection |
| --- | --- |
| task_execution / tmpfs | `--mount=type=tmpfs,destination=/scratch,tmpfs-size=64m` |
| userspace / volume | `--mount=type=volume,source=incept-user-<slug>-<sha256[:12]>,destination=/home/app,ro=false` |
| directory / bind | `--mount=type=bind,source=<realpath of source>,destination=/src,ro=true` |

The named-volume `source` is a **deterministic sovereign name**, never a host path: it is
`incept-<scope-slug>-<digest>` where the digest is a **SHA-256 (FIPS 180-4)** of the
`scope_ref`, so distinct scopes never collide onto one volume. The bind projection emits the
**resolved realpath** (never a symlink).

## Run it

```bash
make mount-strategy                                   # selftest + pytest, fail-closed
python tools/verify_mount_strategy.py check   examples/mount_strategy.task_tmpfs.valid.json
python tools/verify_mount_strategy.py project examples/mount_strategy.userspace_volume.valid.json
```

## Live wiring — the running Inception service

The abstract contract is not enough: the *actual* container manifests declare their mounts
**through** it. The running service persists a durable, append-only, hash-chained event log at
`/data/events.jsonl` (source of truth, replayable) and uses `/tmp` for ephemeral scratch under a
read-only rootfs. Each real mount has a strategy instance, and a verifier proves the manifest
matches it:

| Mount | Strategy instance | Context → type | K8s backing (`deploy/base/deployment.yaml`) | Podman |
| --- | --- | --- | --- | --- |
| `/data` | `examples/mount_strategy.inception_data.valid.json` | `project` → **volume** (durable) | `persistentVolumeClaim: inception-data` | named volume |
| `/tmp` | `examples/mount_strategy.inception_tmp.valid.json` | `task_execution` → **tmpfs** (ephemeral) | `emptyDir { medium: Memory, sizeLimit: 64Mi }` | tmpfs |

`tools/verify_deploy_mount_strategy.py` (CI: *deploy mounts declared THROUGH the mount-strategy*)
is **fail-closed** and proves, kubectl-free, that:

1. every container `volumeMount` is governed by exactly one strategy instance (undeclared mount ⇒ REJECTED);
2. each instance passes the contract teeth (`verify_mount_strategy.evaluate`);
3. the K8s backing matches the `mount_type` — **durable → PVC**, **tmpfs → `emptyDir{medium: Memory}`**
   (a plain node-disk `emptyDir` is *not* tmpfs and is rejected), **bind → hostPath**;
4. the durable log (`INCEPTION_LOG` from the ConfigMap the Deployment consumes) resolves onto a
   **durable** mount, never tmpfs — so the event log provably survives the container.

Point (3), applied to `task_execution → tmpfs`, is exactly why **task-scratch can never land on the
`/data` volume**: a task mount cannot be a PVC. The engine (`src/inception/engine.py`) reinforces
this in code — its only disk write is the append-only log at `log_path` (`/data`); all other state
is in memory, so there is no separate task-scratch to persist.

### Same declared type under Podman (local runs)

The K8s PVC and the local Podman named volume are the **same declared type** (durable `volume`), and
`/tmp` is tmpfs in both. Project the two instances straight to `podman run --mount` flags — the
projection is fail-closed, so a mount that would not pass the contract never renders:

```bash
# The exact flags (deterministic; the volume NAME is derived from scope_ref via SHA-256 / FIPS 180-4):
python tools/verify_mount_strategy.py project examples/mount_strategy.inception_data.valid.json
#   --mount=type=volume,source=incept-project-inception-5130ee1ba6d4,destination=/data,ro=false
python tools/verify_mount_strategy.py project examples/mount_strategy.inception_tmp.valid.json
#   --mount=type=tmpfs,destination=/tmp,tmpfs-size=64m

# Run the sovereign Podman runtime with the SAME declared mount types as the cluster:
podman volume create incept-project-inception-5130ee1ba6d4   # durable named volume (Podman-managed)
podman run --rm -p 8731:8731 \
  -e INCEPTION_LOG=/data/events.jsonl \
  "$(python tools/verify_mount_strategy.py project examples/mount_strategy.inception_data.valid.json)" \
  "$(python tools/verify_mount_strategy.py project examples/mount_strategy.inception_tmp.valid.json)" \
  cybernetic-genesis/inception:<digest>
```

`/data` is a durable Podman-managed named volume (the event log outlives the container, same as the
PVC); `/tmp` is a memory-only tmpfs (scratch dies with the container, same as the `medium: Memory`
`emptyDir`). Run `make deploy-check` to prove the whole chain locally, fail-closed.

> Nothing here is applied to a cluster — the deploy overlays are held (see `deploy/README.md`).
