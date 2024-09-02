# WIP docker compose setup for janus

## Setup
0. Ensure you have docker installed on your machine. If your instalation is relatively old, you might be running compose v1 which reached EOL and is no longer supported. [More info](https://docs.docker.com/compose/migrate/)
 
1. Build the Database Image (Postgres + SQLx binary)


```bash
cd ..
docker build -t postgress-sqlx . -f Dockerfile.postgress
```

2. Spin up the containers

```bash
# Assuming this is the current working directory (cwd)
docker compose up -d
```

> Note: Docker Compose has been integrated directly into Docker, accessible with the `docker compose` command. Previously, it was a separate component, docker-compose. Using the old version can lead to unexplained issues.

## Janus configs

Each janus component has a `config.yaml` and optionaly a `tasks.yaml`, defined in [configs](./configs/). These are documented in the root folder:
- [basic config](../docs/samples/basic_config)
- [advanced config](../docs/samples/advanced_config)
- [tasks.yaml](../blob/main/docs/samples/tasks.yaml)

## Useful Docker Compose Commands

Just a quick cheatsheet

- **Start services**: `docker compose up` - Starts the containers in detached mode (`-d` for detached). Use without `-d` to see the logs in the console.
- **Stop services**: `docker compose down` - Stops and removes all the containers defined by the `docker-compose.yml` file. Add the `-v` flag to remove the volumes as well.
- **Rebuild services**: `docker compose up --build` - Use this to rebuild the containers before starting them. This is useful after making changes to the Dockerfiles.
- **View running containers**: `docker compose ps` - Lists all running containers associated with the `docker-compose.yml` in the current directory.
- **View logs**: `docker compose logs` - Displays log output from all containers. Add a service name to view logs for a specific service, e.g., `docker compose logs web`.
- **Execute commands in container**: `docker compose exec [service] [command]` - Allows you to execute a command inside a service's container. For example, `docker compose exec web bash`.
- **Stop services**: `docker compose stop` - Stops running containers without removing them. Use `docker compose start` to restart the services.
- **Remove stopped containers**: `docker compose rm` - Use this command to remove stopped containers manually.
- **View service logs in real-time**: `docker compose logs -f [service]` - Follows the log output of a specific service. Remove the service name to follow logs for all services.
