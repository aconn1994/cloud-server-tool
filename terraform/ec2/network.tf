resource "aws_vpc" "core-env" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
  tags = {
    Name = "core-env"
  }
}

resource "aws_eip" "ip-core-env" {
  instance = aws_instance.game_server_tf.id
  vpc      = true
}