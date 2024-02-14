```
// Get Event Required on Windows Platform
#event_simpleName=AgentOnline event_platform=Win
// Convert BastTime in epoch Time Stamp

| realBootTime := (((BaseTime/1000)*1024)+978307200)*1000

// Determine Uptime in Days

| uptimeDays := (now()-(realBootTime))/1000/60/60/24

// Round Uptime to Remove Decimal Place

| round("uptimeDays")

// Crate groupBy to organize output

| groupBy(aid, function=([selectLast([realBootTime,uptimeDays])]))

// Convert realBootTime to Human Readable Format and rename output

| realBootTimeHuman := formatTime("%Y-%m-%d %H:%M:%S", field=realBootTime, locale=en_US, timezone=Z)

// Make sure the field realBootTimeHuman has been calculated

| realBootTimeHuman = *

// Drop unnecessary field in epoch time

| drop(["realBootTime"])

```