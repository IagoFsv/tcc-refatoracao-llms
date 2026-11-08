from dataclasses import dataclass
from typing import Any, Callable

@dataclass
class ProjectRenameConfig:
    project_name: str

@dataclass
class PyprojectConfig:
    tool: dict[str, Any]
    tool_poetry: dict[str, str]

def get_pep8_compliant_name(project_name: str) -> str:
    return project_name.replace('-', '_')

def get_project_path() -> str:
    with open('pyproject.toml', encoding='utf-8') as file:
        poetry = PyprojectConfig(**tomb.load(file))
        return get_pep8_compliant_name(poetry.tool.poetry.name)

def rename_project(context: Context, config: ProjectRenameConfig) -> None:
    current_project_path = get_project_path()
    shutil.move(get_pep8_compliant_name(current_project_path), get_pep8_compliant_name(config.project_name))
    with open('pyproject.toml', 'r', encoding='utf-8') as file:
        data = tomb.load(file)
    data['tool']['poetry']['name'] = config.project_name
    with open('pyproject.toml', 'w', encoding='utf-8') as file:
        tomb.dump(data, file)

def executar(project_name: str) -> None:
    rename_project(Context(), ProjectRenameConfig(project_name))
