# Azure AD / Entra ID Package

### Log Ingestion

Deploying our tool named SeGateway - https://github.com/segateway/hosting-azure-aks/ which deploys an AKS cluster running syslog-ng that can pull events from an eventhub and forward onto LogScale

You then need to point the Azure AD Activity logs to the event hub following this documentation - https://learn.microsoft.com/en-us/entra/identity/monitoring-health/howto-stream-logs-to-event-hub?tabs=splunk

### Package Contents

Contains several dashboards to visualise Azure AD data in LogScale