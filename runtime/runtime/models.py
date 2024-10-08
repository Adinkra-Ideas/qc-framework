import os
import enum

from typing import List
from pydantic import BaseModel, field_validator


class ExecType(str, enum.Enum):
    EXECUTABLE = "executable"


class ModuleType(str, enum.Enum):
    CHECKER_BUNDLE = "checker_bundle"
    REPORT_MODULE = "report_module"
    RESULT_POOLING = "result_pooling"


class FrameworkManifest(BaseModel):
    manifest_file_path: List[str]

    @field_validator("manifest_file_path")
    @classmethod
    def file_path_must_exist(cls, v: List[str]) -> str:
        for raw_file_path in v:
            resolved_file_path = os.path.expandvars(raw_file_path)
            if not os.path.isfile(resolved_file_path):
                raise ValueError(f"File path '{resolved_file_path}' must exist.")
        return v


class Module(BaseModel):
    name: str
    exec_type: ExecType
    module_type: ModuleType
    exec_command: str


class ModuleManifest(BaseModel):
    module: List[Module]
