locals {
  environment = "dev"
  app_prefix = "cst"

  required_common_tags = {
    Owner = "Adam Connolly (Acorn)"
    Project = "Cloud Server Tool"
    Purpose = "Spin up game servers"
  }

  serviced_games = {
    arma_three = "Arma 3",
    minecraft = "Minecraft"
  }

  terraform_commands = [
    "apply",
    "plan",
    "import",
    "push",
    "refresh",
    "output",
    "destroy"
  ]
}