# resource "aws_instance" "game_server_tf" {
#   ami                         = var.ami
#   instance_type               = var.instance_type
#   key_name                    = var.ami_key_pair_name
#   security_groups             = [aws_security_group.ingress-all-core.id]
#   associate_public_ip_address = true
#
#   subnet_id = aws_subnet.subnet-uno.id
#   user_data = file("startup.sh")
#
#   tags = {
#     Name       = "Acorn's Game Server ${var.environment} ${var.build_type}"
#     Build_Type = var.build_type
#   }
#
# }