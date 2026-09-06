{{/*
Common labels applied to every object.
*/}}
{{- define "berth.labels" -}}
app.kubernetes.io/name: berth
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
helm.sh/chart: {{ printf "%s-%s" .Chart.Name .Chart.Version }}
app: berth
{{- with .Values.commonLabels }}
{{ toYaml . }}
{{- end }}
{{- end -}}

{{/*
Pod selector labels (stable across upgrades — never include version here).
*/}}
{{- define "berth.selectorLabels" -}}
app: berth
{{- end -}}

{{/*
Fully-qualified image reference. image.tag defaults to the chart appVersion so
the deployed version is pinned (never floats to :latest).
*/}}
{{- define "berth.image" -}}
{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}
{{- end -}}

{{/*
Name of the chart-managed Secret that holds AUTH_TOKEN and/or LICENSE_KEY.
*/}}
{{- define "berth.secretName" -}}
berth-secrets
{{- end -}}

{{/*
Name of the PVC backing the AI data dir (ledger + memory + settings).
*/}}
{{- define "berth.aiPvcName" -}}
{{ ((.Values.ai | default dict).persistence | default dict).existingClaim | default "berth-ai-data" }}
{{- end -}}
