const form = document.getElementById('quote');
async function refresh() {
  for (const name of ['plans', 'subscriptions']) {
    const response = await fetch(`/api/${name}`);
    document.getElementById(name).textContent = JSON.stringify(await response.json(), null, 2);
  }
}
form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const data = new FormData(form);
  const body = {target_plan: data.get('target_plan'), effective_on: data.get('effective_on')};
  if (data.get('cap_cents') !== '') body.cap_cents = Number(data.get('cap_cents'));
  try {
    const response = await fetch(`/api/subscriptions/${encodeURIComponent(data.get('subscription_id'))}/quote`, {
      method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(body),
    });
    document.getElementById('result').textContent = `${response.status}\n${JSON.stringify(await response.json(), null, 2)}`;
  } catch (error) { document.getElementById('result').textContent = error.message; }
});
refresh().catch((error) => { document.getElementById('result').textContent = error.message; });
