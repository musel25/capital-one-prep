const form = document.getElementById('query');
async function refresh() {
  const data = new FormData(form);
  const merchant = encodeURIComponent(data.get('merchant_id'));
  for (const [id, url] of [['settlements', `/api/settlements?merchant_id=${merchant}`], ['summary', `/api/merchants/${merchant}/summary?on=${data.get('on')}`]]) {
    const response = await fetch(url);
    document.getElementById(id).textContent = JSON.stringify(await response.json(), null, 2);
  }
}
form.addEventListener('submit', (event) => { event.preventDefault(); refresh(); });
refresh();
