from dataclasses import dataclass

@dataclass
class CaseConfig:
    project_path : str
    function_name : str
    user : str
    password : str
    localhost : str
    port : int
    database : str