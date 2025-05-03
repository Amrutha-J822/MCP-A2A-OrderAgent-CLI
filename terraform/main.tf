provider "aws" {
  region = "us-west-1"
}

# VPC with DNS enabled
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true         # ✅ required for RDS
  enable_dns_hostnames = true         # ✅ required for RDS
  tags = {
    Name = "main-vpc"
  }
}

# Subnets (in allowed AZs)
resource "aws_subnet" "subnet1" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "us-west-1b"
  map_public_ip_on_launch = true
  tags = {
    Name = "subnet-1"
  }
}

resource "aws_subnet" "subnet2" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.2.0/24"
  availability_zone       = "us-west-1c"
  map_public_ip_on_launch = true
  tags = {
    Name = "subnet-2"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id
  tags = {
    Name = "main-igw"
  }
}

# Public Route Table
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }
  tags = {
    Name = "public-rt"
  }
}

# Route Table Associations
resource "aws_route_table_association" "a" {
  subnet_id      = aws_subnet.subnet1.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "b" {
  subnet_id      = aws_subnet.subnet2.id
  route_table_id = aws_route_table.public.id
}

# DB Subnet Group
resource "aws_db_subnet_group" "rds_subnet" {
  name       = "rds-subnet-group"
  subnet_ids = [aws_subnet.subnet1.id, aws_subnet.subnet2.id]
  tags = {
    Name = "RDS Subnet Group"
  }
}

# RDS PostgreSQL Instance
resource "aws_db_instance" "customer_db" {
  identifier             = "customer-db"
  engine                 = "postgres"
  engine_version         = "13.18"
  instance_class         = "db.t3.micro"
  allocated_storage      = 20
  db_name                = "customerdb"
  username               = "pgmaster"                      # ✅ FIXED
  password               = "YourSecurePassword123"
  db_subnet_group_name   = aws_db_subnet_group.rds_subnet.name
  vpc_security_group_ids = [aws_security_group.rds_sg.id]

  publicly_accessible    = true
  skip_final_snapshot    = true
  port                   = 5432

  tags = {
    Name = "Customer RDS"
  }
}


# Security Group for RDS access
resource "aws_security_group" "rds_sg" {
  name        = "rds-security-group"
  description = "Allow PostgreSQL access"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # ⚠️ open to all for hackathon ease
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "rds-sg"
  }
}