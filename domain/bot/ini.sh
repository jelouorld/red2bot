
#!/bin/bash
function fetch_last_stream() {
    aws logs describe-log-streams \
        --log-group-name "/aws/lambda/$1" \
        --order-by LastEventTime \
        --descending \
        --query logStreams[0].logStreamName 
}

function fetch_last_event() {
    set -x
    LAST_STREAM=$(fetch_last_stream $1 | tr -d '"')

    # echo "DEBUG: LAST_STREAM: $LAST_STREAM"

    aws logs get-log-events \
        --log-group-name "/aws/lambda/$1" \
        --log-stream-name $LAST_STREAM \
        --output json

    set +x

}


# run infra ini: 

cd infra 
source ini.sh
cd - 

