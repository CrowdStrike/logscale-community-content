# LogScale Internal Monitoring Package

This package has been created to give insights into all the humio-* views/repos that are created in your Cloud organization with ease. The package comes with dashboards across all the sources, a parsers for the log collector debug logs and some alerts you can setup to monitor your log ingestion


### How to use this package

- Create a view that connects all the LogScale internal repos/views.
- Name this view "LogScale-Internal-Monitoring"
- Connect all the humio-* repos/views
- Once created install the package as a zip under its Settings page

You should then see all the dashboards.

Some dashboards may require a CSV file on initial load and will fail, this is because there are scheduled searches waiting to run to create these CSV files.