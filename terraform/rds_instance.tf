

# Create an RDS instance
resource "aws_db_instance" "rds_resource" {
  identifier        = "rds-resource"
  instance_class    = "db.t3.micro"
  engine            = "postgres"
  engine_version    = "16.4"
  allocated_storage = 20
  storage_type      = "gp2"
  username          = var.db_username
  password          = var.db_password
  publicly_accessible = false
  skip_final_snapshot = true

  # Configure security groups
  vpc_security_group_ids = [
    aws_security_group.rds_security_group.id
  ]

  # Configure tags
  tags = {
    Name = var.aws_instance_tags
  }
}

# Create a security group to allow access from the EC2 instance
resource "aws_security_group" "rds_security_group" {
  name        = "rds_security_group"
  description = "Security group for example RDS instance"

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    security_groups = [aws_security_group.ec2_aws_security_group.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}