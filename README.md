<h1 align="center"><img src="./docs/images/banner_cli.png" alt="Testing as a service"></h1>  

# Discovery CLI
Discovery CLI will list estuary stack stats in your shell. Alternative to [Estuary Viewer](https://github.com/estuaryoss/estuary-viewer).

# About config.yaml
There are 2 ways to configure this CLI:
- inside eureka domain, define the eureka server address and this cli will look over all discovery(ies) to get the stack stats
```yaml
eureka: "http://localhost:8080/eureka/v2"
```
- define your discovery(ies) one by one. Make sure it is compatible as ```homePageUrl``` field in eureka server. Example:
```yaml
discovery:
  - http://localhost:8081/
  - http://localhost:8082/
```

In case both sections are present ```discovery``` section takes precedence.

## Code quality
[![Maintainability](https://api.codeclimate.com/v1/badges/0bfd475fa5174ea20ae7/maintainability)](https://codeclimate.com/github/estuaryoss/discovery-cli/maintainability)

## Linux status
[![Build Status](https://travis-ci.com/estuaryoss/discovery-cli.svg?branch=main)](https://travis-ci.com/estuaryoss/discovery-cli)

## Win status
[![CircleCI](https://circleci.com/gh/estuaryoss/discovery-cli.svg?style=svg&circle-token=cd4dd66d5683d534ca44f5a64a644720149d8578)](https://circleci.com/gh/estuaryoss/discovery-cli)

## Steps
-  deploy an eureka server
-  deploy [estuary-discovery](https://github.com/estuaryoss/estuary-discovery)) on the target machine (metal/VM/Docker/IoT device)
-  define the yaml configuration 
-  get stats

## Usage
```bash
python .\main.py --ip=192.168.0.10 --port=8080 --token=None --file="config.yaml"
```

## Params
```bash
>python main.py --help
Usage: main.py [OPTIONS]

Options:
  --token TEXT     The authentication token that will be sent via 'Token'
                   header. Use 'None' if estuary-discovery is deployed unsecured

  --protocol TEXT  The protocol with which the estuary-discovery was deployed.
                   Default is http. E.g. https

  --cert TEXT      The certificate with which the estuary-discovery was
                   deployed. E.g. https/cert.pem

  --file TEXT      The yaml file path on disk. Default is "./config.yaml"
  --help           Show this message and exit.

```


Support project: <a href="https://paypal.me/catalindinuta?locale.x=en_US"><img src="https://lh3.googleusercontent.com/Y2_nyEd0zJftXnlhQrWoweEvAy4RzbpDah_65JGQDKo9zCcBxHVpajYgXWFZcXdKS_o=s180-rw" height="40" width="40" align="center"></a>    
