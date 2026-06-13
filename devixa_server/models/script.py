from contextlib import redirect_stderr, redirect_stdout
import io
import time
from sqlalchemy import Column, Integer, String, Text
from typing import Dict, Any, Optional
from ._db import db
from ._base import BaseModel, APIMethod


class Script(BaseModel):
    """
    Model for storing Python automation scripts.
    Each script must follow the AutomationScript class pattern.
    """
    __tablename__ = 'scripts'
    __table_args__ = {'extend_existing': True}

    # Core fields
    name = Column(String(255), nullable=False, index=True)
    code = Column(Text(), nullable=False)
    description = Column(Text(), nullable=True)
    
    # Metadata
    version = Column(Integer(), default=1)
    execution_count = Column(Integer(), default=0)


    @APIMethod(request_methods=['POST'])
    def execute(self, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute the script and record execution metadata.
        This is a placeholder - actual execution would happen in a worker/backend.
        Returns execution result metadata.
        """
        context = context or {}
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()

        try:
            namespace = {}
            with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                exec(str(self.code), namespace)

            if 'instance' not in namespace:
                raise RuntimeError("Script must define 'instance' variable")

            instance = namespace['instance']

            if not hasattr(instance, 'run') or not callable(instance.run):
                raise RuntimeError("Instance must have callable 'run' method")

            # Execute run method
            result = instance.run(**context)

            return {
                'success': True,
                'script_id': self.id,
                'script_name': self.name,
                'stdout': stdout_capture.getvalue(),
                'stderr': stderr_capture.getvalue(),
                'result': result,
            }

        except Exception as e:
            self.last_run_status = 'failed'
            return {
                'success': False,
                'script_id': self.id,
                'script_name': self.name,
                'error': str(e),
                'execution_count': self.execution_count
            }


    @APIMethod(request_methods=['POST'])
    def validate_script_code(self):
        return {'valid': True}