from abc import ABC, abstractmethod
from sqlalchemy import create_engine
from pathlib import Path

class AbstractPythonClass(ABC):
    def __init__(self,case_config):
        self.case_config = case_config
        self.engine = create_engine(
            f"postgresql://{case_config.user}:{case_config.password}@{case_config.localhost}:{case_config.port}/{case_config.database}"
        )
        self.results_path = Path(case_config.project_path + '/Results/' + self.case_config.function_name)
        self.results_path.mkdir(parents=True, exist_ok=True)
    @abstractmethod
    def query(self):
        pass
    @abstractmethod
    def export_data(self):
        pass