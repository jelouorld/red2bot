
This package contains the defintion of the infrastructure for the bot

    - lambda core function
    - lambda layer to support the fixed and project-accidental dependencies 
    - dynamodb chat store:
        necesary to reconstruct conversation for every llm invocation
    - dybamo product store:
        necesary to create a pineconde vector database 