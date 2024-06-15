terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region = var.region
}

resource "aws_instance" "arma_server_tf" {
  ami           = var.ami
  instance_type = var.instance_type

  tags = {
    Name       = "Acorn's Arma Server DEV"
    Build_Type = var.build_type
  }
}