
function fetch_last_event_stream() {
    aws logs describe-log-streams \
        --log-group-name "/aws/lambda/$1" \
        --order-by LastEventTime \
        --descending \
        --query logStreams[0].logStreamName \
        --output text
}

function get_last_event_stream() {

    STREAM=$(fetch_last_event_stream $1)
    
    aws logs get-log-events \
        --log-group-name "/aws/lambda/$1" \
        --log-stream-name $STREAM \
        --output json
}