
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

      local = { # provider for interacting with local files
        source = "hashicorp/local"
        version = "~> 2.1"
      }
    }
}

locals {
  app_tag = "devops-app"
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


resource "digitalocean_firewall" "web_firewall" {
  name = "devops-app-firewall"

  tags = [local.app_tag] # One firewall for all droplets with this tag

  depends_on = [ digitalocean_droplet.web_server ]


    # Rules for INCOMING traffic
  inbound_rule {
    protocol         = "tcp"
    port_range       = "22" # Allow SSH from anywhere
    source_addresses = ["0.0.0.0/0", "::/0"]
  }
  inbound_rule {
    protocol         = "tcp"
    port_range       = "5000" # Allow our Flask App from anywhere
    source_addresses = ["0.0.0.0/0", "::/0"]
  }
  inbound_rule {
    protocol         = "tcp"
    port_range       = "9100" # Allow requests to Node exporter
    source_addresses = ["0.0.0.0/0", "::/0"] # temporarly open for all traffic
  }

  # Rules for OUTGOING traffic
  outbound_rule {
    protocol         = "tcp"
    port_range       = "all" # Allow all outbound TCP
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }
  outbound_rule {
    protocol         = "udp"
    port_range       = "all" # Allow all outbound UDP
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }
  outbound_rule {
    protocol         = "icmp" # Allow ping
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }

}

resource "digitalocean_droplet" "web_server" {
  count = 2 # create n droplets
  image = "ubuntu-22-04-x64"
  name = "devops-app-server-${count.index + 1}"
  region = "fra1"
  size = "s-1vcpu-1gb"

  ssh_keys = [data.digitalocean_ssh_key.laptop_key.id]

  tags = [local.app_tag] # assign the same tag as firewall to auto apply it
}


resource "local_file" "ansible_inventory" {
  content = templatefile("${path.module}/inventory.tftpl", {
    droplets = digitalocean_droplet.web_server
  })

  
  filename = "${path.module}/../ansible_project/inventory.ini"

  depends_on = [
    digitalocean_droplet.web_server
  ] # wait till the server has been created and valid ip can be found
}



# After terraform apply show ip address of the server
output "droplet_ip_address" {
  description = "Servers public IP adresses."
  value = digitalocean_droplet.web_server.*.ipv4_address
}

output "ssh_keys_on_server" {
  description = "Names of the SSH keys installed on the server"
  value = [data.digitalocean_ssh_key.laptop_key.name]
}