from servicefoundry import Build, Service, PythonBuild, Resources


service = Service(
    name="term-deposit-svc",
    image=Build(
        build_spec=PythonBuild(
            command="uvicorn main:app --port 8000 --host 0.0.0.0",
            requirements_path="requirements.txt",
        )
    ),
    ports=[{"port": 8000}],
    env={
        "TFY_HOST": "https://app.develop.truefoundry.tech",
        "TFY_API_KEY": '<your-api-key>',
        "MODEL_VERSION_FQN": "<your-model-fqn>"
    },
    resources=Resources(cpu_request=1, cpu_limit=1.5,
                        memory_limit=2000, memory_request=1500)
)

deployment = service.deploy(workspace_fqn='v1:tfy-dev-cluster:sri-demo')
