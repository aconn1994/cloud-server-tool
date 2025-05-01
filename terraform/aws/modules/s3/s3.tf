resource "aws_s3_bucket" "cst-resources" {
  bucket = "cst-resources"

  tags = merge(var.required_common_tags, { BucketName = "cst-resources", Purpose = "Store CST Resources" })
}