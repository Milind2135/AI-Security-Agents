resource "aws_cloudtrail" "main" {
  name                          = "main-trail"
  s3_bucket_name                = "example-trail-logs"
  is_multi_region_trail         = false
  include_global_service_events = true
  # data events not configured
}
