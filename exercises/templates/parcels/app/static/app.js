const message = document.querySelector('#message');
const money = cents => `$${(cents / 100).toFixed(2)}`;
async function api(path, body) {
  const response = await fetch(path, body ? {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(body)} : {});
  const data = await response.json();
  if (!response.ok) throw new Error(typeof data.detail === 'string' ? data.detail : 'Please check the package details.');
  return data;
}
document.querySelector('#quote-form').addEventListener('submit', async event => {
  event.preventDefault();
  const fields = event.target.elements;
  try {
    const result = await api('/api/quotes', {zone: fields.zone.value, service: fields.service.value, weight_grams: Number(fields.weight.value), signature: fields.signature.checked});
    const output = document.querySelector('#quote'); output.replaceChildren();
    for (const [label, value] of [['Billable units', result.billable_units], ['Transport', money(result.transport_cents)], ['Signature', money(result.signature_cents)], ['Total', money(result.total_cents)], ['Estimated days', result.estimated_days]]) {
      const term = document.createElement('dt'); term.textContent = label;
      const definition = document.createElement('dd'); definition.textContent = value;
      output.append(term, definition);
    }
    message.textContent = 'Quote ready.';
  } catch (error) { message.textContent = error.message; }
});
async function start() {
  try {
    for (const rate of (await api('/api/rates')).items) {
      document.querySelector('#zone').add(new Option(rate.zone, rate.zone));
      const row = document.createElement('tr');
      for (const value of [rate.zone, money(rate.base_cents), money(rate.per_unit_cents), rate.standard_days]) {
        const cell = document.createElement('td'); cell.textContent = value; row.append(cell);
      }
      document.querySelector('#rates').append(row);
    }
  } catch (error) { message.textContent = error.message; }
}
start();
