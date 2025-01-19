resource "aws_subnet" "subnet-uno" {
  cidr_block        = cidrsubnet(aws_vpc.core-env.cidr_block, 3, 1)
  vpc_id            = aws_vpc.core-env.id
  availability_zone = "${var.region}a"
}

resource "aws_route_table" "route-table-core-env" {
  vpc_id = aws_vpc.core-env.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.core-env-gw.id
  }
  tags = {
    Name = "core-env-route-table"
  }
}
resource "aws_route_table_association" "subnet-association" {
  subnet_id      = aws_subnet.subnet-uno.id
  route_table_id = aws_route_table.route-table-core-env.id
}