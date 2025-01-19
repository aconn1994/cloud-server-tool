resource "aws_internet_gateway" "core-env-gw" {
  vpc_id = aws_vpc.core-env.id
  tags = {
    Name = "core-env-gw"
  }
}