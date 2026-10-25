const form = document.getElementById('submission');
async function refresh() {
  for (const name of ['datasets', 'jobs']) {
    const response = await fetch(`/api/${name}`);
    document.getElementById(name).textContent = JSON.stringify(await response.json(), null, 2);
  }
}
form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const data = new FormData(form);
  const headers = {'Content-Type': 'application/json'};
  if (data.get('key') !== '') headers['Idempotency-Key'] = data.get('key');
  try {
    const response = await fetch('/api/jobs', {
      method: 'POST', headers,
      body: JSON.stringify({dataset_id: data.get('dataset_id'), format: data.get('format')}),
    });
    document.getElementById('result').textContent = `${response.status}\n${JSON.stringify(await response.json(), null, 2)}`;
    await refresh();
  } catch (error) { document.getElementById('result').textContent = error.message; }
});
refresh().catch((error) => { document.getElementById('result').textContent = error.message; });
