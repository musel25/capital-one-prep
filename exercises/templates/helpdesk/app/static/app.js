const ticket = document.querySelector('#ticket');
const message = document.querySelector('#message');
async function api(path, body) {
  const response = await fetch(path, body ? {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(body)} : {});
  const data = await response.json();
  if (!response.ok) throw new Error(typeof data.detail === 'string' ? data.detail : 'Please check the form values.');
  return data;
}
async function showTicket() {
  try {
    const data = await api(`/api/tickets/${ticket.value}`);
    document.querySelector('#detail').textContent = `${data.subject} · ${data.status}`;
    document.querySelector('#status-form select').value = data.status;
    const list = document.querySelector('#timeline');
    list.replaceChildren();
    try {
      const activity = await api(`/api/tickets/${ticket.value}/timeline`);
      document.querySelector('#timeline-message').textContent = activity.items.length ? '' : 'No activity yet.';
      for (const event of activity.items) {
        const item = document.createElement('li');
        item.textContent = `${event.actor} · ${event.kind}: ${event.text}`;
        list.append(item);
      }
    } catch (error) { document.querySelector('#timeline-message').textContent = error.message; }
  } catch (error) { message.textContent = error.message; }
}
ticket.addEventListener('change', showTicket);
for (const [formId, endpoint] of [['comment-form', 'comments'], ['status-form', 'status']]) {
  document.getElementById(formId).addEventListener('submit', async event => {
    event.preventDefault();
    try {
      await api(`/api/tickets/${ticket.value}/${endpoint}`, Object.fromEntries(new FormData(event.target)));
      message.textContent = endpoint === 'comments' ? 'Comment added.' : 'Status saved.';
      if (endpoint === 'comments') event.target.elements.body.value = '';
      await showTicket();
    } catch (error) { message.textContent = error.message; }
  });
}
async function start() {
  try {
    for (const item of (await api('/api/tickets')).items) ticket.add(new Option(`${item.id} · ${item.subject}`, item.id));
    await showTicket();
  } catch (error) { message.textContent = error.message; }
}
start();
