resource "google_cloudfunctions2_function" "pricing_api" {
  name     = "pricing-api"
  location = "europe-west1"

  build_config {
    runtime     = "python312"
    entry_point = "handler"
  }

  service_config {
    ingress_settings = "ALLOW_ALL"
  }
}

resource "google_cloud_run_service_iam_member" "public_invoker" {
  location = google_cloudfunctions2_function.pricing_api.location
  service  = google_cloudfunctions2_function.pricing_api.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}
