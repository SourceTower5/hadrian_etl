
variable "aws_access_key" {
  type        = string
  default     = "my_access_key"
}

variable "aws_secret_key" {
  type        = string
  default     = "my_secret_key"
}

variable "aws_instance_tags" {
    type        = string
    default     = "example-instance"
}

variable "db_username" {
    type        = string
    default     = "my_username"
} 

variable "db_password" {
    type        = string
    default     = "my_password"
} 
