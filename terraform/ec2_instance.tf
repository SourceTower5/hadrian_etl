

# Create an EC2 instance
resource "aws_instance" "example" {
  ami           = "ami-0d53d72369335a9d6" # region ca-west-1
  instance_type = "t2.micro"

  # Configure security groups
  vpc_security_group_ids = [
    aws_security_group.ec2_aws_security_group.id,
  ]

  # Use user data to install Docker and Docker Compose
  user_data = <<-EOF
    #!/bin/bash
    sudo apt update
    sudo apt install -y docker.io
    sudo systemctl start docker
    sudo usermod -a -G docker ubuntu
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    EOF

  # Configure tags
  tags = {
    Name = var.aws_instance_tags
  }
}

# Create a security group to allow SSH and HTTP access
resource "aws_security_group" "ec2_aws_security_group" {
  name        = "ec2_aws_security_group"
  description = "Security group for ec2 instance"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = var.aws_instance_tags
  }
}