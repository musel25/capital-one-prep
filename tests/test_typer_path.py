"""Check offline CLI execution and reject incomplete solutions."""
import pytest


def test_all_seven_references_pass_and_real_faults_fail():
    from cojudge.typer_path.support import load_specs, verify
    specs = load_specs()
    assert len(specs) == 7
    for spec in specs:
        result = verify(spec)
        assert result['cases'] >= 5
        assert result['template_failures'] > 0
        assert result['mutations']


def test_verification_rejects_an_undetected_fault():
    from cojudge.typer_path.support import load_specs, verify
    spec = load_specs()[0]
    spec['mutations'] = [{'name': 'equivalent', 'old': 'a + b', 'new': 'b + a'}]
    with pytest.raises(AssertionError, match='survived'):
        verify(spec)
