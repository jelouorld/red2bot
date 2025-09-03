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

# aws aliases
alias ali="aws lambda invoke --function-name "
alias all="aws lambda list-functions"

# aws shell functions 

function ads() {
    aws dynamodb scan --table-name $1 | jq 
}


# some env vars:
export PYTHONDONTWRITEBYTECODE=1


