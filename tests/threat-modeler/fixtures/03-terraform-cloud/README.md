# Invoice service infrastructure (SYNTHETIC TEST SYSTEM)

Stores customer invoice PDFs (customer name, billing address, amounts) in object storage. Two services (invoice-api, report-batch) run as cloud functions. A CI pipeline deploys the Terraform.
