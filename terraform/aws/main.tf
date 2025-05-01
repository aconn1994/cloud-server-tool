terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

module "ec2" {
  source = "./modules/ec2"
}

module "ecr" {
  source = "./modules/ecr"

  PYTHON_IMAGE = "dummy_image_tag"
  required_tags = {
    RepoType   = "Development"
    AccessType = "Private"
  }
  required_common_tags = local.required_common_tags
}