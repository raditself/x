
import docker
import uuid
import os

class DockerSandbox:
    def __init__(self):
        self.client = docker.from_env()
        self.container = None

    def execute_code(self, code, timeout=10):
        container_name = f"code_sandbox_{uuid.uuid4().hex}"
        volume_name = f"code_volume_{uuid.uuid4().hex}"

        try:
            # Create a volume
            volume = self.client.volumes.create(volume_name)

            # Write code to a file in the volume
            with open(f"/var/lib/docker/volumes/{volume_name}/_data/code.py", "w") as f:
                f.write(code)

            # Run the code in a container
            self.container = self.client.containers.run(
                "python:3.9-slim",
                f"python /code/code.py",
                name=container_name,
                volumes={volume_name: {'bind': '/code', 'mode': 'ro'}},
                detach=True,
                mem_limit="50m",
                nano_cpus=1000000000,  # 1 CPU
                network_disabled=True
            )

            # Wait for the container to finish or timeout
            result = self.container.wait(timeout=timeout)

            if result['StatusCode'] == 0:
                output = self.container.logs().decode('utf-8')
            else:
                output = f"Error: {self.container.logs().decode('utf-8')}"

        except docker.errors.ContainerError as e:
            output = f"Error: {str(e)}"
        except Exception as e:
            output = f"Unexpected error: {str(e)}"
        finally:
            # Clean up
            if self.container:
                self.container.remove(force=True)
            self.client.volumes.get(volume_name).remove(force=True)

        return output

# Usage example:
# sandbox = DockerSandbox()
# result = sandbox.execute_code("print('Hello from Docker sandbox!')")
# print(result)
