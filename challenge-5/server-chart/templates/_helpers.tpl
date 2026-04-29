{{- define "server-chart.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "server-chart.fullname" -}}
{{- if .Values.fullnameOverride -}}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- $name := default .Chart.Name .Values.nameOverride -}}
{{- if contains $name .Release.Name -}}
{{- .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}
{{- end -}}

{{- define "server-chart.labels" -}}
helm.sh/chart: {{ include "server-chart.name" . }}
{{ include "server-chart.selectorLabels" . }}
server-chart/version: "{{ .Chart.Version }}"
{{- end -}}

{{- define "server-chart.selectorLabels" -}}
app.kubernetes.io/name: {{ include "server-chart.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}