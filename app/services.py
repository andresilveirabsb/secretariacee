from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import pandas as pd

from . import db
from .models import Student


@dataclass
class ImportResult:
    inserted: int
    updated: int


def import_students_from_excel(file_stream) -> ImportResult:
    dataframe = pd.read_excel(file_stream)
    dataframe = dataframe.rename(
        columns={
            "matricula": "registration",
            "nome": "name",
            "turma": "class_name",
            "data_nascimento": "birth_date",
            "responsavel": "guardian_name",
        }
    )

    required_columns = {"registration", "name", "class_name"}
    missing_columns = [col for col in required_columns if col not in dataframe.columns]
    if missing_columns:
        raise ValueError(
            f"Colunas obrigatórias ausentes na planilha: {', '.join(missing_columns)}"
        )

    inserted, updated = 0, 0

    for item in _iter_rows(dataframe):
        student = Student.query.filter_by(registration=item["registration"]).first()
        if student is None:
            student = Student(registration=item["registration"])
            db.session.add(student)
            inserted += 1
        else:
            updated += 1

        student.name = item["name"]
        student.class_name = item["class_name"]
        student.birth_date = item.get("birth_date")
        student.guardian_name = item.get("guardian_name")

    db.session.commit()
    return ImportResult(inserted=inserted, updated=updated)


def _iter_rows(dataframe: pd.DataFrame) -> Iterable[dict]:
    dataframe = dataframe.fillna("")
    for row in dataframe.to_dict(orient="records"):
        registration = str(row.get("registration", "")).strip()
        name = str(row.get("name", "")).strip()
        class_name = str(row.get("class_name", "")).strip()
        if not registration or not name or not class_name:
            continue

        yield {
            "registration": registration,
            "name": name,
            "class_name": class_name,
            "birth_date": str(row.get("birth_date", "")).strip() or None,
            "guardian_name": str(row.get("guardian_name", "")).strip() or None,
        }
