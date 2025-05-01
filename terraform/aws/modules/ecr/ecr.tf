resource "aws_ecr_repository" "cst_ecr_dev_repo" {
  name                 = var.PYTHON_IMAGE
  image_tag_mutability = "MUTABLE"
  image_scanning_configuration {
    scan_on_push = true
  }
  tags = merge(var.required_common_tags, var.required_tags, { Name = var.PYTHON_IMAGE })
}