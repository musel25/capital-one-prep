const form = document.getElementById('report');
async function refresh() {
  for (const name of ['members', 'sessions']) {
    const response = await fetch(`/api/${name}`);
    document.getElementById(name).textContent = JSON.stringify(await response.json(), null, 2);
  }
}
form.addEventListener('submit', async (event) => {
  event.preventDefault();
  try {
    const query = new URLSearchParams(new FormData(form));
    const response = await fetch(`/api/attendance?${query}`);
    document.getElementById('result').textContent = `${response.status}\n${JSON.stringify(await response.json(), null, 2)}`;
  } catch (error) { document.getElementById('result').textContent = error.message; }
});
refresh().catch((error) => { document.getElementById('result').textContent = error.message; });
