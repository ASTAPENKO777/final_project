"""Shared pytest fixtures.

Every test runs against a fresh in-memory SQLite database so tests are
isolated from each other and never touch the real project.db.
"""
import os
import sys
from pathlib import Path

# Make the project root importable (tests/ lives one level below it).
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# create_db reads DATABASE_URL at import time, so it must be set beforehand.
os.environ.setdefault("DATABASE_URL", "sqlite://")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import models  # noqa: F401  registers every mapper before create_all
from models.base import Base
from create_db import get_db
from app import app


@pytest.fixture()
def db_session():
    """A transactional session bound to a throwaway in-memory database."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,  # keep one connection so :memory: survives
    )
    Base.metadata.create_all(bind=engine)
    TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSession()
    try:
        yield session
    finally:
        session.close()
        engine.dispose()


@pytest.fixture()
def client(db_session):
    """TestClient with the get_db dependency pointed at the test database."""

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture()
def team(client):
    """A persisted team, returned as the API represents it."""
    response = client.post("/team/", json={"name": "Dream Team"})
    assert response.status_code == 200
    return response.json()


@pytest.fixture()
def tournament(client):
    """A persisted tournament, returned as the API represents it."""
    response = client.post(
        "/tournaments/",
        json={
            "title": "Summer Cup",
            "description": "Annual summer tournament",
            "start_date": "2026-06-01T10:00:00",
            "end_date": "2026-06-30T18:00:00",
        },
    )
    assert response.status_code == 200
    return response.json()
