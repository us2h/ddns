
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/us2h/ddns/docker-build-and-publish-release.yml)
![Latest Tag Version](https://img.shields.io/github/v/tag/us2h/ddns)
![Docker Image Size](https://img.shields.io/docker/image-size/us2h/ddns?sort=date)
![Docker Image Pulls](https://img.shields.io/docker/pulls/us2h/ddns)

# Dynamic DNS Monitor

If you have a dynamic IP address and want to host a websites or other services on your home network, you need a way to update your DNS records when your IP address changes.
This project provides a service that monitors your dynamic IP address and updates DNS records if a change in IP address is detected. It periodically checks your current IP address and updates DNS records by interacting with your DNS provider's API.

## Features

- Support for multiple DNS providers (currently supported: Route53)
- Support for multiple subdomains or whildcard of a domain
- Customizable check interval (default: 60 seconds)
- Docker support

## Requirements

- Python 3 or Docker
- API access to your DNS provider

## Running with Docker

Docker images are available on [Docker Hub](https://hub.docker.com/r/us2h/ddns)

Available architectures: `amd64`, `arm64`, `armv7`

Tag `latest` is latest stable release.

Tag `dev` is build from master branch.

Tags `vX.Y.Z` are stable releases.

Environment variables:

- `PROVIDER`: DNS provider (currently supported: `route53`)

- `PERIOD`: Check interval in seconds (default: `60`)

- `IPIFY_URL`: IPIFY URL (default: `https://api.ipify.org`) (in case you want to use your own instance of IPIFY)

- `DOMAINS`: Comma separated list of domains (e.g. `test1.example.com, test2.example.com`) or wildcard domains (e.g. `*.example.com`)

- `DOMAINS_FILE`: Filename of a file containing a list of domains (e.g. `domains.txt`) line by line

You could use both `DOMAINS` and `DOMAINS_FILE` at the same time. In case of `DOMAINS_FILE` is specified mount specified file to `/app/` in container. (e.g. `/app/domains.txt`)


### Providers

#### Route53

| Provider | Environment variable | Description          |
| --- | --- |----------------------|
| Route53 | `AWS_ACCESS_KEY_ID` | AWS access key ID    |
| Route53 | `AWS_SECRET_ACCESS_KEY` | AWS secret access key |
| Route53 | `AWS_HOSTED_ZONE_ID` | AWS hosted zone ID   |

Minimum required permissions for AWS IAM user:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "VisualEditor0",
      "Effect": "Allow",
      "Action": "route53:ChangeResourceRecordSets",
      "Resource": "arn:aws:route53:::hostedzone/<HOSTED_ZONE_ID>"
    },
    {
      "Sid": "VisualEditor1",
      "Effect": "Allow",
      "Action": "route53:ListHostedZonesByName",
      "Resource": "*"
    },
    {
      "Sid": "VisualEditor2",
      "Effect": "Allow",
      "Action": "route53:ListResourceRecordSets",
      "Resource": "arn:aws:route53:::hostedzone/<HOSTED_ZONE_ID>"
    }
  ]
}
```

Replace `<HOSTED_ZONE_ID>` with your hosted zone ID.

### Examples

#### Docker

```bash
docker run -d \
  --name ddns \
  -e PROVIDER=route53 \
  -e PERIOD=60 \
  -e AWS_ACCESS_KEY_ID=... \
  -e AWS_SECRET_ACCESS_KEY=... \
  -e AWS_HOSTED_ZONE_ID=... \
  -e DOMAINS=test1.example.com,test2.example.com \
  us2h/ddns
```

#### Docker Compose

```yaml
version: "3.8"

services:
  ddns:
    image: us2h/ddns:latest
    container_name: ddns
    environment:
      - PROVIDER=route53
      - PERIOD=60
      - AWS_ACCESS_KEY_ID=...
      - AWS_SECRET_ACCESS_KEY=...
      - AWS_HOSTED_ZONE_ID=...
      - DOMAINS=test1.example.com,test2.example.com
```

#### Docker Compose with domains file

```yaml
version: "3.8"

services:
  ddns:
    image: us2h/ddns:latest
    container_name: ddns
    environment:
      - PROVIDER=route53
      - PERIOD=60
      - AWS_ACCESS_KEY_ID=...
      - AWS_SECRET_ACCESS_KEY=...
      - AWS_HOSTED_ZONE_ID=...
      - DOMAINS_FILE=domains.txt
    volumes:
      - ./domains.txt:/app/domains.txt
```


## Running with Python

### Requirements

- Python 3
- pip

### Installation of dependencies

```bash
pip install -r requirements.txt
```

### Configuration

Set environment variables mentioned above or edit `config/common.py` file.

### Usage

```bash
python app.py
```
