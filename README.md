# container-cleaner
Deletes automatically the containers (including the volumes) that are not
running and don't have restart policy.

This is particularly useful to clean completed tasks/jobs on Amazon Web
Services ec2 instances.

## Example

```
docker run -it --rm \
    -v /run/docker.sock:/tmp/docker.sock \
    cecton/container-cleaner --loop-delay=5 --dry-run
```

## Program Arguments
 *  --dry-run -n

    perform a trial run with no changes made

 *  --loop-delay

    sleep a certain delay in seconds (0 to disable, this is the default)
