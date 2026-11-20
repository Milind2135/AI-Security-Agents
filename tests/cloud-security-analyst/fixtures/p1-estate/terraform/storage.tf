resource "aws_s3_bucket" "customer_exports" {
  bucket = "example-customer-exports"
  tags   = { "data-class" = "confidential-pii" }
}

resource "aws_s3_bucket" "reports_archive" {
  bucket = "example-reports-archive"
}

resource "aws_s3_bucket" "marketing_assets" {
  bucket = "example-marketing-assets"
  tags   = { "data-class" = "public" }
}

resource "aws_s3_bucket_acl" "marketing_assets" {
  bucket = aws_s3_bucket.marketing_assets.id
  acl    = "public-read"
}
