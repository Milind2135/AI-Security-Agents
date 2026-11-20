resource "aws_security_group" "web" {
  name   = "web-sg"
  vpc_id = "vpc-0a1b2c3d"
  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "web_01" {
  ami                         = "ami-00000000000000001"
  instance_type               = "t3.medium"
  subnet_id                   = "subnet-public-a"
  associate_public_ip_address = true
  vpc_security_group_ids      = [aws_security_group.web.id]
  iam_instance_profile        = aws_iam_instance_profile.app.name
  tags = { Name = "web-01", env = "prod" }
}
