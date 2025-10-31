
# To-do later: https://developer.hashicorp.com/terraform/language/backend
# terraform {
#   backend "s3" {
#     bucket         = "my-terraform-state-bucket-name"
#     key            = "my-project/terraform.tfstate"
#     region         = "us-east-1"
#     encrypt        = true
#     dynamodb_table = "terraform-lock-table"
#   }
# }


terraform {
    required_providers {
      digitalocean = {
        source = "digitalocean/digitalocean"
        version = "~> 2.68.0"
      }
    }
}

variable "do_token" {
  description = "DigitalOcean API Token."
  type = string
  sensitive = true
}

provider "digitalocean" {
  token = var.do_token # exists in "terraform.tfvars"
}

data "digitalocean_ssh_key" "laptop_key" { # first is resource type, second is local name
  name = "laptop_linux"
}

# Add it later
# data "digitalocean_ssh_key" "pc_key" {
#   name = "pc_linux"
# }

resource "digitalocean_droplet" "web_server" {
  image = "ubuntu-22-04-x64"
  name = "devops-app-server"
  region = "fra1"
  size = "s-1vcpu-1gb"

  ssh_keys = [data.digitalocean_ssh_key.laptop_key.id]
}

# After terraform apply show ip address of the server
output "droplet_ip_address" {
  description = "Server public IP adress."
  value = digitalocean_droplet.web_server.ipv4_address
}

output "ssh_keys_on_server" {
  description = "Names of the SSH keys installed on the server"
  value = [data.digitalocean_ssh_key.laptop_key.name]
}