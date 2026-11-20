resource "aws_security_group" "alb_public" {
  name = "alb-public-sg"
  ingress {
    description = "Public HTTPS for the shop load balancer (CHG-1042)"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
