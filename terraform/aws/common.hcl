locals {
  environment = "dev"
  app_prefix = "cst"

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