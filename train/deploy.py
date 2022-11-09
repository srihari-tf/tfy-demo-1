from servicefoundry import Build, Job, PythonBuild, Resources

job = Job(
    name="term-deposit-rfc-train",
    image=Build(
        build_spec=PythonBuild(
            command="python train.py",
            requirements_path="requirements.txt",
        )
    ),
    env={
        "TFY_HOST": 'https://app.truefoundry.com/',
        "TFY_API_KEY": '<your-api-key>'
    },
    resources=Resources(cpu_request=1, cpu_limit=1.5,
                        memory_limit=2000, memory_request=1500)
)

deployment = job.deploy(workspace_fqn='tfy-cluster-euwe1:test-ws')