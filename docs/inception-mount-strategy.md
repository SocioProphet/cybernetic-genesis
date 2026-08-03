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

## Follow-up

Live wiring — the actual Inception container manifests (`deploy/`, `Dockerfile` `/data`)
declaring their mounts through this strategy so the running service's `/data` PVC and any
task scratch are provably the right type — is tracked separately (@mdheller).
