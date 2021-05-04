# Reminder Bot

## Init

```bash
./scripts/init.sh
```

## Deploy

1. create bot

https://www.freecodecamp.org/news/create-a-discord-bot-with-python/

2. create image registry

```sh
./scripts/create_registry.sh $project
```

3. create serviceaccount

```sh
./scripts/create_account.sh $project
```

4. build image

```sh
./scripts/build.sh $project
```

5. deploy your project

```bash
./scripts/deploy.sh $project $token
```

## Option

[Scheduling compute instances with Cloud Scheduler](https://cloud.google.com/scheduler/docs/start-and-stop-compute-engine-instances-on-a-schedule)

