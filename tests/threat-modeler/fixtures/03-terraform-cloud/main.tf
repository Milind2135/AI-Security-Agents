provider "aws" {
  region = "eu-west-1"
}

resource "aws_s3_bucket" "invoices" {
  bucket = "example-invoices-prod"
}

resource "aws_s3_bucket_acl" "invoices" {
  bucket = aws_s3_bucket.invoices.id
  acl    = "public-read"
}

resource "aws_iam_role" "shared_app_role" {
  name               = "shared-app-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume.json
}

resource "aws_iam_role_policy" "shared_app_policy" {
  role = aws_iam_role.shared_app_role.id
  policy = jsonencode({
    Version   = "2012-10-17"
    Statement = [{ Effect = "Allow", Action = "*", Resource = "*" }]
  })
}

resource "aws_lambda_function" "invoice_api" {
  function_name = "invoice-api"
  role          = aws_iam_role.shared_app_role.arn
  handler       = "index.handler"
  runtime       = "nodejs20.x"
  filename      = "invoice-api.zip"
}

resource "aws_lambda_function" "report_batch" {
  function_name = "report-batch"
  role          = aws_iam_role.shared_app_role.arn
  handler       = "index.handler"
  runtime       = "nodejs20.x"
  filename      = "report-batch.zip"
}
