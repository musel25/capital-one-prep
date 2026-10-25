const form = document.getElementById('delivery');
async function refresh() {
  for (const name of ['parcels', 'notifications']) {
    const response = await fetch(`/api/${name}`);
    document.getElementById(name).textContent = JSON.stringify(await response.json(), null, 2);
  }
}
form.addEventListener('submit', async (event) => {
  event.preventDefault();
  try {
    const response = await fetch('/api/deliveries', {
      method: 'POST', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(Object.fromEntries(new FormData(form))),
    });
    document.getElementById('result').textContent = `${response.status}\n${JSON.stringify(await response.json(), null, 2)}`;
    await refresh();
  } catch (error) { document.getElementById('result').textContent = error.message; }
});
refresh().catch((error) => { document.getElementById('result').textContent = error.message; });
