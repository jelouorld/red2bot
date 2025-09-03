alias e=echo


# terraform aliases
alias taa="terraform apply -auto-approve"
alias tda="terraform destroy -auto-approve"
alias tp="terraform plan"
alias tom="terraform output -raw medar_fetcher_lambda_url"
alias tob="terraform output -raw red2bot_url"

# git aliases 
alias gs="git status"
alias gp="git push"
alias gr="git restore ."
alias gl="git pull"
alias gam="git add . && git commit -m "
alias gd="git diff"

# aws aliases
alias ali="aws lambda invoke --function-name "
alias all="aws lambda list-functions"

# aws shell functions 

function ads() {
    aws dynamodb scan --table-name $1 | jq 
}

function aws_lambda_invoke_and_log(){
    function_name=$1
    tempfile="__temp__$1"
    touch $tempfile
    aws lambda invoke --function-name $function_name $tempfile
    e -----------------------------
    cat $tempfile | jq # pretty format the response 
    rm $tempfile # remove the temp file
}



# some env vars:
export PYTHONDONTWRITEBYTECODE=1


