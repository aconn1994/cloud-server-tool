variable "region" {
  description = "Value for AWS region to deploy resources"
  type        = string
  default     = "us-east-1"
}

variable "required_tags" {
  description = "ECR specific tags"
  type = object({
    RepoType   = string # Development | Game
    AccessType = string # Public | Private

  })
}

variable "required_common_tags" {
  description = "Required common resource tags defined by ME!!!!! Found in common vars in root directory"
  type        = map(string)
}

variable "PYTHON_IMAGE" {
  description = "ECR Repo name from container"
  type        = string
}