"""Added boundary tests, kept separate from the imported tests."""

EXTRA = {
6: '''
def test_added_date_defaults_at_each_creation(user, food):
    import time
    from datetime import datetime
    first = FoodEntry(id=10, user=user, food=food, number_servings=2)
    time.sleep(0.02)
    second = FoodEntry(id=11, user=user, food=food, number_servings=0.5)
    assert second.date_added > first.date_added
    explicit = datetime(2020, 1, 2, 3, 4, 5)
    item = FoodEntry(id=12, user=user, food=food, number_servings=0, date_added=explicit)
    assert item.date_added == explicit
    assert item.total_calories == 0
''',
7: '''
def test_added_unknown_user_has_empty_log(client):
    response = client.get('/users/999')
    assert response.status_code == 200
    assert response.json() == []
''',
8: '''
def test_added_calorie_boundary_and_user_isolation(client, food_entry1):
    from copy import deepcopy
    original = dict(food_log)
    payload = deepcopy(food_entry1)
    payload['id'] = 31
    payload['user']['id'] = 31
    payload['user']['username'] = 'other'
    payload['user']['max_daily_calories'] = 156
    payload['number_servings'] = 2
    assert client.post('/', json=payload).status_code == 201
    too_much = deepcopy(payload)
    too_much['id'] = 32
    too_much['number_servings'] = 0.5
    before = dict(food_log)
    response = client.post('/', json=too_much)
    assert response.status_code == 400
    assert response.json()['detail'].endswith('156 kcal / day')
    assert food_log == before
    assert all(food_log[key] == value for key, value in original.items())

def test_added_duplicate_does_not_overwrite(client, food_entry1):
    before = dict(food_log)
    changed = dict(food_entry1, number_servings=0)
    assert client.post('/', json=changed).status_code == 400
    assert food_log == before
''',
9: '''
def test_added_html_filters_and_escapes(client, food_entry1):
    from copy import deepcopy
    payload = deepcopy(food_entry1)
    payload['id'] = 10
    payload['user']['username'] = 'Other'
    payload['food']['name'] = 'private-food'
    assert client.post('/', json=payload).status_code == 201
    response = client.get('/Julian')
    assert response.headers['content-type'].startswith('text/html')
    assert 'private-food' not in response.text
    payload['id'] = 11
    payload['user']['username'] = 'Julian'
    payload['food']['name'] = '<script>alert(1)</script>'
    assert client.post('/', json=payload).status_code == 201
    text = client.get('/Julian').text
    assert '<script>' not in text
    assert '&lt;script&gt;' in text
    empty = BeautifulSoup(client.get('/nobody').text, 'html.parser')
    assert empty.find_all('td') == []
''',
10: '''
def test_added_reject_expired_tampered_and_unknown_tokens(client):
    from datetime import datetime, timedelta, timezone
    from jose import jwt
    from app import SECRET_KEY, ALGORITHM
    for claims in (
        {'sub': 'tim', 'exp': datetime.now(timezone.utc) - timedelta(seconds=20)},
        {'sub': 'nobody', 'exp': datetime.now(timezone.utc) + timedelta(minutes=1)},
        {'exp': datetime.now(timezone.utc) + timedelta(minutes=1)},
    ):
        encoded = jwt.encode(claims, SECRET_KEY, algorithm=ALGORITHM)
        response = client.get('/', headers={'Authorization': 'Bearer ' + encoded})
        assert response.status_code == 401
        assert response.json()['detail'] == 'Could not validate credentials'
    encoded = jwt.encode({'sub': 'tim', 'exp': datetime.now(timezone.utc) + timedelta(minutes=1)},
                         'wrong-signing-key', algorithm=ALGORITHM)
    assert client.get('/', headers={'Authorization': 'Bearer ' + encoded}).status_code == 401

def test_added_update_cannot_transfer_ownership(client, user1, user2, food1):
    from copy import deepcopy
    from app import food_log
    payload = dict(id=90, user=user1, food=food1, number_servings=1)
    headers = _create_food_as_user(client, payload, user1['username'])
    changed = deepcopy(payload)
    changed['user'] = user2
    before = dict(food_log)
    assert client.put('/90', json=changed, headers=headers).status_code == 400
    assert food_log == before
    changed['user'] = dict(user1, id=user2['id'])
    assert client.put('/90', json=changed, headers=headers).status_code == 400
    assert food_log == before

def test_added_create_cannot_overwrite_other_user_id(client, user1, user2, food1):
    from app import food_log
    payload = dict(id=91, user=user1, food=food1, number_servings=1)
    _create_food_as_user(client, payload, user1['username'])
    headers = {'Authorization': 'Bearer ' + _get_token(client, user2['username']).json()['access_token']}
    payload['user'] = user2
    before = dict(food_log)
    assert client.post('/', json=payload, headers=headers).status_code == 400
    assert food_log == before
''',
}
