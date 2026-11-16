from dataclasses import dataclass
from typing import List

@dataclass
class Project:
    name: str

@dataclass
class Tool:
    poetry: Project

@dataclass
class ProjectData:
    tool: Tool

@dataclass
class ProjectPath:
    project_data: ProjectData

def get_pep8_compliant_name(project_name: str) -> str:
    return project_name.replace('-', '_')

def get_project_path():
    with open('pyproject.toml', encoding='utf-8') as file:
        data = toml.load(file)
        return ProjectPath(ProjectData(Tool(get_pep8_compliant_name(data['tool']['poetry']['name']))))

def executar():
    return get_project_path().project_data.tool.name
