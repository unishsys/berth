# Berth

> September 2026 upgrade: [read the operations guide](docs/production-readiness.md). Authentication, ticket-based logs and single-writer storage require coordinated backend/chart upgrades.


**Berth is a self-hosted Kubernetes dashboard** for observing and managing
clusters from a single web UI. Observe nodes, pods, deployments, and services;
stream pod logs live; create and edit resources with cluster-aware visual
builders; expose an app end-to-end (Deployment → Service → Certificate → Gateway
→ Route) in one guided flow; and get an at-a-glance overview of endpoint health
and capacity. The whole app ships as **one container**, a Vue SPA embedded in a
small Go binary that runs inside your cluster.

> Berth is proprietary, commercial software. See the [EULA](LICENSE). It is
> **freemium**: free for small clusters, with paid tiers for larger ones, and
> it always verifies its license **offline** (no phone-home).

This repository is the **public distribution** for Berth, the Helm chart,
release binaries, and container image live here. The source is not public.

- Website & sign-up: **https://berth.agrohi.com**
- Container image: `ghcr.io/unishsys/berth`
- Helm chart (OCI): `oci://ghcr.io/unishsys/charts/berth`

---

## Editions

Berth is gated by **cluster size (node count)**. **Viewing is always free,
with no key.** *Making changes* (create/edit/delete) requires a license, a free
Community key, or a trial/paid key. Beyond your node cap, changes pause until you
upgrade; the dashboard always stays fully readable.

| Edition | Limits | How to get it |
| --- | --- | --- |
| **Community** | up to 10 nodes, single cluster | free, [create an account](https://berth.agrohi.com) for a key |
| **Enterprise** | unlimited nodes, per cluster | subscription with a 14-day trial, [see pricing](https://berth.agrohi.com/pricing/) |

> SSO/OIDC, RBAC, audit log, multi-cluster, and private agentic AI are the
> Enterprise roadmap, [design partners welcome](https://berth.agrohi.com/pricing/).

## 1. Register & get a license key

1. Create a free account at **https://berth.agrohi.com**. A **Community** key is
   issued to you automatically.
2. For unlimited evaluation, [start a 14-day trial](https://berth.agrohi.com/pricing/);
   to subscribe, pick a plan at checkout.
3. Your current key (and a personalized install guide) is always available on
   your **dashboard** at https://berth.agrohi.com. Keys are renewed/extended
   automatically while your subscription is active.

You can install and **view** your cluster without any key, you only need one to
make changes.

## 2. Install

### Helm (recommended)

The chart is published as an **OCI artifact** on GHCR. Helm 3.8+ is required.

```sh
# Installs the latest stable release. Defaults to secure token auth and
# generates an auth token for you.
helm upgrade --install berth oci://ghcr.io/unishsys/charts/berth \
  --namespace berth --create-namespace
```

Pin a specific version (recommended for production), or install a pre-release:

```sh
helm upgrade --install berth oci://ghcr.io/unishsys/charts/berth \
  --version 1.0.1 --namespace berth --create-namespace

# pre-releases (e.g. betas) must be requested by exact version:
helm upgrade --install berth oci://ghcr.io/unishsys/charts/berth \
  --version 1.0.0-beta --namespace berth --create-namespace
```

Read your auth token and reach the UI:

```sh
kubectl -n berth get secret berth-secrets -o jsonpath='{.data.AUTH_TOKEN}' | base64 -d ; echo
kubectl -n berth port-forward svc/berth 8081:8081   # then open http://localhost:8081/
```

To expose it publicly, enable the Ingress and TLS:

```sh
helm upgrade --install berth oci://ghcr.io/unishsys/charts/berth --reuse-values \
  --set ingress.enabled=true --set ingress.className=nginx \
  --set ingress.host=berth.example.com \
  --set ingress.tls.enabled=true --set ingress.tls.secretName=berth-tls
```

**Apply your license:**

```sh
helm upgrade --install berth oci://ghcr.io/unishsys/charts/berth --reuse-values \
  --set license.key='<YOUR_KEY>'
# or reference a Secret that holds a LICENSE_KEY key:
helm upgrade --install berth oci://ghcr.io/unishsys/charts/berth --reuse-values \
  --set license.existingSecret=my-license
```

The current tier, trial countdown, and node usage are shown in the dashboard's
license banner.

> **Security:** Berth has cluster-wide access, treat dashboard access as
> cluster access. Don't run `auth.mode=none` on shared/exposed clusters, and
> serve it over HTTPS.

### Container image

The image runs inside Kubernetes via the Helm chart above (`incluster` mode). To
point it at a cluster from your workstation, run it in `remotecluster` mode with
your kubeconfig mounted:

```sh
export AUTH_TOKEN="$(openssl rand -hex 32)"
docker run --rm -p 127.0.0.1:8081:8081 \
  -e AUTH_MODE=token -e AUTH_TOKEN -e BIND_ADDRESS=0.0.0.0 \
  -v "$HOME/.kube/config:/home/nonroot/.kube/config:ro" \
  ghcr.io/unishsys/berth:1.0.1 remotecluster
# then open http://localhost:8081/  (AUTH_MODE defaults to token; configure AUTH_TOKEN with at least 32 random characters)
```

Images are multi-arch (`linux/amd64`, `linux/arm64`), ship an SBOM + provenance,
and are **cosign-signed** (keyless). Verify:

```sh
cosign verify ghcr.io/unishsys/berth:1.0.1 \
  --certificate-identity-regexp 'https://github.com/unishsys/.*' \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com
```

### Standalone binary

Download the binary for your OS/arch from the
[latest release](https://github.com/unishsys/berth/releases/latest), verify it
against `SHA256SUMS`, then run it against your kubeconfig:

```sh
# macOS (Apple Silicon) example
curl -sSLO https://github.com/unishsys/berth/releases/download/v1.0.1/berth-darwin-arm64
curl -sSLO https://github.com/unishsys/berth/releases/download/v1.0.1/SHA256SUMS
shasum -a 256 -c SHA256SUMS --ignore-missing   # verify
chmod +x berth-darwin-arm64
./berth-darwin-arm64 remotecluster           # serves the UI on :8081
```

Binaries are published for:

| OS | Architectures |
| --- | --- |
| macOS | `amd64` (Intel), `arm64` (Apple Silicon) |
| Linux | `amd64`, `arm64` |
| Windows | `amd64` (`.exe`) |

## 3. Usage

- **Run modes:** `incluster` (inside a pod, uses the ServiceAccount, what the
  Helm chart runs) or `remotecluster` (uses your local `~/.kube/config`).
- **Authentication:** the Helm chart defaults to `token` mode and generates a
  stable token. Read it from the `berth-secrets` Secret (above). For a local
  binary, auth defaults to `token`; explicit loopback-only development may use `none`.
- **License:** paste your key (Helm `license.key`, or `LICENSE_KEY` env). Empty =
  Community tier. Verified offline; works in air-gapped clusters.
- **Optional integrations** degrade gracefully when absent: metrics-server
  (CPU/memory), Gateway API, cert-manager / external-dns (the domain → DNS → TLS
  → gateway chain), and the in-app AI SRE assistant (local Ollama, or Claude on
  your own key).

### Common configuration

Set these via Helm (`--set`) or as environment variables on the container:

| Variable / Helm value | Default | Purpose |
| --- | --- | --- |
| `auth.mode` / `AUTH_MODE` | `token` (chart) | `none`, `token`, or `proxy-header`. |
| `auth.token` / `AUTH_TOKEN` | _(generated)_ | Static bearer token for `token` mode. |
| `license.key` / `LICENSE_KEY` | _(unset)_ | Signed license token. Empty = Community. |
| `ingress.*` | disabled | Expose the UI via an Ingress + TLS. |
| `telemetryDisabled` / `TELEMETRY_DISABLED` | `false` | Disable the optional anonymous usage ping. |
| `ai.providers` / `AI_PROVIDERS` | `ollama` | Providers to offer: `ollama`, `anthropic`, `claude` (Bedrock). |
| `ai.ollama.host` / `OLLAMA_HOST` | `http://ollama.ollama.svc:11434` | Local Ollama endpoint. |
| `ai.anthropic.apiKey` / `ANTHROPIC_API_KEY` | _(unset)_ | Claude via the Anthropic API (Enterprise). |
| `ai.persistence.enabled` | `false` | Persist the AI usage ledger + incident memory (SQLite). |

See `helm show values oci://ghcr.io/unishsys/charts/berth` for the full list.

## Helm configuration

The chart is built for real clusters, scheduling onto tainted pools, policy
engines, private registries, HA, and locked-down security all have first-class
flags. Pass them with `--set`/`--set-json`, or (recommended) a values file:
`helm upgrade --install berth oci://ghcr.io/unishsys/charts/berth -n berth -f my-values.yaml`.

### Scheduling & availability

| Value | Default | Purpose |
| --- | --- | --- |
| `replicaCount` | `1` | Required single-writer deployment; higher values rejected. |
| `nodeSelector` | `{}` | Pin pods to a node pool. |
| `tolerations` | `[]` | Schedule onto tainted nodes (spot pools, GPU, control-plane). |
| `affinity` | `{}` | Node/pod (anti-)affinity. |
| `topologySpreadConstraints` | `[]` | Spread replicas across zones/nodes. |
| `priorityClassName` | `""` | Protect from eviction/preemption (e.g. on spot). |
| `podDisruptionBudget.enabled` | `false` | Keep the UI up during node drains. `minAvailable`/`maxUnavailable` configurable. |
| `terminationGracePeriodSeconds` | `30` | Graceful-shutdown window (the app drains in-flight requests). |
| `revisionHistoryLimit` | `3` | ReplicaSets kept for rollback. |
| `strategy` | `{}` | Deployment update strategy (e.g. `maxUnavailable: 0`). |
| `startupProbe` / `livenessProbe` / `readinessProbe` | tuned | Probe timing (path/port fixed to `/ping`). |

### Security & policy

| Value | Default | Purpose |
| --- | --- | --- |
| `podSecurityContext` | restricted, uid `65532` | Pod-level context. On OpenShift, drop the fixed UIDs so the SCC assigns them. |
| `securityContext` | restricted | Container-level (no-priv-escalation, read-only rootfs, drop ALL caps). |
| `rbac.create` | `true` | Set `false` to manage the cluster-scoped ClusterRole/Binding yourself. |
| `serviceAccount.annotations` | `{}` | Cloud workload identity (AKS/EKS/GKE). |
| `commonLabels` / `commonAnnotations` | `{}` | Applied to **every** object, for OPA Gatekeeper / Kyverno requirements or cost tags. |
| `podLabels` / `podAnnotations` | `{}` | Service-mesh injection, Prometheus scrape hints. |
| `networkPolicy.enabled` | `false` | Restrict inbound to the UI port; `allowedNamespaces` whitelists callers. |

### Image, networking & storage

| Value | Default | Purpose |
| --- | --- | --- |
| `image.repository` / `image.tag` | `ghcr.io/unishsys/berth` / appVersion | Use a mirrored image / pin a version. |
| `imagePullSecrets` | `[]` | Pull from a private/mirrored registry (air-gapped). |
| `service.type` / `service.annotations` | `ClusterIP` / `{}` | e.g. an internal cloud load balancer. |
| `ingress.*` | disabled | Expose the UI via Ingress + TLS. |
| `extraVolumes` / `extraVolumeMounts` | `[]` | Mount e.g. a corporate CA bundle (rootfs is read-only). |
| `extraEnv` | `[]` | Additional environment variables. |

### AI SRE assistant

The dashboard has a built-in, **read-only** AI SRE that reasons over your live
cluster. You bring the model and the key, Berth calls the provider directly
from inside the cluster and never proxies, meters, or bills tokens. Local Ollama
is available on every tier; Claude (Anthropic API or Amazon Bedrock, on your own
key) needs an Enterprise license **and** dashboard auth (`auth.mode != none`), so
an anonymous caller can never spend your key.

| Value | Default | Purpose |
| --- | --- | --- |
| `ai.providers` | `ollama` | Comma-separated: `ollama`, `anthropic`, `claude` (alias `bedrock`). |
| `ai.defaultProvider` | _(first listed)_ | Provider used when a chat names none. |
| `ai.ollama.host` / `ai.ollama.model` | in-cluster svc / `sabbir/berth-sre` | Local model endpoint and tag. |
| `ai.ollama.numCtx` | `16384` | Ollama context window, do not lower (smaller loops the model). |
| `ai.anthropic.apiKey` / `.existingSecret` | _(unset)_ | Anthropic API key inline or from a Secret (`ANTHROPIC_API_KEY`). |
| `ai.anthropic.model` | `claude-opus-5` | e.g. `claude-sonnet-5` for lower cost. |
| `ai.bedrock.token` / `.existingSecret` | _(unset)_ | Bedrock bearer token; empty uses the pod's AWS credential chain. |
| `ai.bedrock.region` / `.model` | `us-east-1` / _(backend default)_ | Bedrock region and model id. |
| `ai.effort` / `ai.thinking` / `ai.maxTokens` | `high` / `adaptive` / `8192` | Shared Claude behaviour. |
| `ai.guardrails.dailyTokenBudget` / `.monthlyTokenBudget` | `0` / `0` | Cloud token caps (0 = unlimited), enforced with an in-flight reservation. |
| `ai.guardrails.rateLimitPerMinute` / `.maxConcurrentRuns` | `20` / `4` | Per-principal rate limit and concurrency cap. |
| `ai.allowRawDiagnostics` | `false` | Explicitly allow raw logs/descriptions to reach your model. |
| `ai.persistence.enabled` / `.dataDir` / `.size` | `false` / `/data/ai` / `1Gi` | Persist the usage ledger, incident memory, and Settings overrides (SQLite PVC). |

The rootfs is read-only, so the ledger needs a writable volume: enable
`ai.persistence` (or leave it off to keep usage/memory in-memory). The store is a
single-process SQLite file. Use one replica with Recreate and a local RWO block volume. NFS/RWX and overlapping replicas are unsupported. Cloud providers require persistent storage. Most of this is also editable at runtime in **Settings → AI**
(requires auth). Full reference: `https://berth.agrohi.com/how-ai-works/`.

### Recipes

**Schedule onto a tainted spot pool (AKS) and survive reclamation:**
```yaml
tolerations:
  - key: kubernetes.azure.com/scalesetpriority
    operator: Equal
    value: spot
    effect: NoSchedule
priorityClassName: system-cluster-critical
podDisruptionBudget:
  enabled: true
  minAvailable: 1
```
(GKE spot uses `cloud.google.com/gke-spot=true:NoSchedule`; control-plane nodes use `node-role.kubernetes.io/control-plane:NoSchedule`.)

**Single-writer storage:**
```yaml
replicaCount: 1
strategy: { type: Recreate }
ai:
  persistence:
    enabled: true
    accessMode: ReadWriteOnce
```

**Private / air-gapped registry:**
```yaml
image:
  repository: registry.internal/berth
imagePullSecrets:
  - name: internal-registry
```

**AI SRE with Claude on your own Anthropic key (Enterprise), budgeted & persisted:**
```yaml
license:
  key: <ENTERPRISE_KEY>            # or license.existingSecret
ai:
  providers: "anthropic,ollama"    # cloud + local fallback
  defaultProvider: anthropic
  anthropic:
    existingSecret: berth-anthropic   # Secret with key ANTHROPIC_API_KEY
    model: claude-opus-5
  guardrails:
    dailyTokenBudget: 2000000
    monthlyTokenBudget: 20000000
  persistence:
    enabled: true                  # durable usage ledger + incident memory
    size: 1Gi
```
(auth.mode must not be `none` for cloud providers to be offered.)

**Fully local / air-gapped AI (Community-friendly, nothing leaves the cluster):**
```yaml
ai:
  providers: "ollama"
  ollama:
    host: http://ollama.ollama.svc:11434
    model: sabbir/berth-sre
```

**OpenShift (let the SCC assign UIDs):** Helm *merges* maps, so you must
null out the default UIDs (not just omit them):
```yaml
podSecurityContext:
  runAsNonRoot: true
  runAsUser: null
  runAsGroup: null
  fsGroup: null
  seccompProfile:
    type: RuntimeDefault
```

**Cloud workload identity (AKS shown):**
```yaml
serviceAccount:
  annotations:
    azure.workload.identity/client-id: <client-id>
podLabels:
  azure.workload.identity/use: "true"
```

**Internal load balancer instead of an Ingress (AKS shown):**
```yaml
service:
  type: LoadBalancer
  annotations:
    service.beta.kubernetes.io/azure-load-balancer-internal: "true"
```

**Lock down inbound traffic to the ingress controller only:**
```yaml
networkPolicy:
  enabled: true
  allowedNamespaces: [ingress-nginx]
```
> Heads-up: with `allowedNamespaces` set, some CNIs (e.g. Calico) also block the
> kubelet's health probes (they come from the node, not a namespace), causing a
> restart loop. Confirm your CNI permits node→pod probes, or allow the node CIDR.

**Let your security team own RBAC** (chart creates only the ServiceAccount):
```yaml
rbac:
  create: false
```

**Trust a corporate/self-signed CA:**
```yaml
extraVolumes:
  - name: ca-bundle
    configMap: { name: corp-ca }
extraVolumeMounts:
  - name: ca-bundle
    mountPath: /etc/ssl/certs/corp-ca.crt
    subPath: ca.crt
    readOnly: true
```

## Support & legal

- Docs & guides: https://berth.agrohi.com
- Support: support@agrohi.com
- License: [EULA](LICENSE) · Privacy & Terms: https://berth.agrohi.com
