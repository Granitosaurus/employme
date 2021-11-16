from employme.interpreter import KnowledgeInterpreter


def test_KnowledgeInterpreter_skills_from_text():
    ki = KnowledgeInterpreter()
    assert ki.skills_from_text("one Python three and fast-api") == ["python", "fastapi"]
