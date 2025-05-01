locals {
  region = "us-east-1"

  required_common_tags = {
    Owner          = "Acorn"
    Project        = "Cloud Server Tool"
    ProjectPurpose = "Spin up game servers"
  }

}