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

resource "aws_key_pair" "deployer" {
  key_name   = "ec2-ssh-keypair"
  public_key = file("./ec2-ssh-keypair.pub")
}

resource "aws_instance" "arma_server_tf" {
  ami                         = var.ami
  instance_type               = var.instance_type
  key_name                    = "ec2-ssh-keypair"
  associate_public_ip_address = true

  provisioner "file" {
    source      = "../dist/server_config.tar.gz"
    destination = "/home/arma3/server_config.tar.gz"

    connection {
      type        = "ssh"
      user        = "ubuntu"
      private_key = file("./ec2-ssh-keypair")
      host        = self.public_ip
    }
  }

  tags = {
    Name       = "Acorn's Arma Server DEV TERRAFORM"
    Build_Type = var.build_type
  }

  user_data = file("./scripts/launch.sh")
}