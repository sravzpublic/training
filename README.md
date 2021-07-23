Share Research And ViZualize [Sravz](https://sravz.com) is an analytics platform for smart investments.

### [Sravz Training YouTube Playlist](https://youtu.be/vFtlOtXPo5s)

### Start srarvz training docker container
```bash
# Run make to see the list of available commands
$ make
help                           This help.
print-env                      Print Env
docker-build                   Builds docker image
docker-push                    Docker: push docker images
docker-compose-rebuild-service Rebuild docker compose service: make docker-compose-rebuild-service service=backend-go
docker-compose                 Run docker compose action: make docker-compose up/down
docker-compose-tail-logs       Tails docker logs: make docker-compose-tail-logs service=training
docker-exec                    Exec into a docker container: make docker-exec service=training

# Start the docker service
$ make docker-compose action=up
docker network create training | true
echo "Running docker command up"; \
        if [ "up" == "up" ]; then \
        docker compose up -d; \
        else \
        docker compose up; \
        fi
Running docker command up
[+] Running 2/2
 ⠿ Network training_training      Created                                                                                                                                           0.1s
 ⠿ Container training_training_1  Started

 # Tail the docker service logs
$ make docker-compose-tail-logs service=training
docker context use default
default
docker-compose logs -f --tail=10 training
training_1  | tail: cannot open 'anything' for reading: No such file or directory
^Ccanceled

# Login do docker service container to check the workspace directory
$ make docker-exec service=training
docker exec -it `docker ps -aqf "name=training_training_1"` sh
$ cd workspace
$ ls
docker-compose.yaml  Dockerfile  favicon.ico  Makefile  README.md  training-ansible  training-hugo  training-py
```


[Sravz Documentation](https://docs.sravz.com/)
[Sravz Website](https://sravz.com)
