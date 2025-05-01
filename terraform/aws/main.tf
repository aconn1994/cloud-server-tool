terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"

  backend "s3" {
    bucket = "cst-resources"
    key    = "terraform/terraform.tfstate"
    region = "us-east-1"
  }
}

module "s3" {
  source               = "./modules/s3"
  required_common_tags = local.required_common_tags
}

module "ec2" {
  source               = "./modules/ec2"
  required_common_tags = local.required_common_tags
}

module "ecr" {
  source                 = "./modules/ecr"
  DEVELOPMENT_IMAGE_NAME = "cst_base"
  required_tags = {
    RepoType    = "Development"
    AccessType  = "Private"
    RepoPurpose = "DevOps image repository for local and cicd"
  }
  required_common_tags = local.required_common_tags
}