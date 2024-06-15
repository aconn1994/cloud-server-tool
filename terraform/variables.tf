variable "region" {
  description = "Value for AWS region to deploy resources"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Value for deployment environment"
  type = string
  default = "dev"
}

variable "ami" {
  description = "Image Hash for EC2 instance"
  type        = string
  default     = "ami-07d9b9ddc6cd8dd30"
}

variable "instance_type" {
  description = "Value for EC2 instance type"
  type        = string
  default     = "t2.micro"
}

variable "build_type" {
  description = "Value tag for build type"
  type        = string
  default     = "terraform"
}