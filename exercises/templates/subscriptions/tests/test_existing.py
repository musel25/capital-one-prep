from fastapi.testclient import TestClient

from app.main import create_app


def test_plan_prices_are_integer_cents():
    client = TestClient(create_app())
    plans = client.get('/api/plans').json()['items']
    assert {plan['id']: plan['monthly_cents'] for plan in plans} == {'basic': 1200, 'plus': 3100, 'team': 5000}
    assert all(type(plan['monthly_cents']) is int for plan in plans)


def test_subscription_detail_preserves_billing_period():
    client = TestClient(create_app())
    subscription = client.get('/api/subscriptions/sub-200').json()
    assert subscription['period_start'] == '2026-10-15'
    assert subscription['period_end'] == '2026-11-15'
    assert subscription['plan_id'] == 'plus'
    assert subscription in client.get('/api/subscriptions').json()['items']


def test_cancelled_accounts_are_visible_and_unknown_accounts_are_rejected():
    client = TestClient(create_app())
    assert client.get('/api/subscriptions/sub-300').json()['status'] == 'cancelled'
    assert client.get('/api/subscriptions/missing').status_code == 404
