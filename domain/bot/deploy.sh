

function apply() {
    terraform -chdir=infra init
}

function destroy() { 
    terraform -chdir=infra destroy --auto-approve 
}


function test() {
    aws 
}


if [ "$1" == "apply" ]; then
    apply
elif [ "$1" == "destroy" ]; then
    destroy
fi




