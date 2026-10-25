let page = 1;
const message = document.querySelector('#message');
async function api(path, body) {
  const response = await fetch(path, body ? {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(body)} : {});
  const data = await response.json();
  if (!response.ok) throw new Error(typeof data.detail === 'string' ? data.detail : 'Please check the reader and filter values.');
  return data;
}
async function load() {
  const fields = document.querySelector('#filters').elements;
  const query = new URLSearchParams({page, page_size: fields.size.value, available_only: fields.available.checked});
  if (fields.genre.value) query.set('genre', fields.genre.value);
  try {
    const data = await api('/api/books?' + query);
    document.querySelector('#page-info').textContent = `Page ${data.page} · ${data.total} matching books`;
    document.querySelector('#previous').disabled = page === 1;
    document.querySelector('#next').disabled = !data.has_next;
    const table = document.querySelector('#books'); table.replaceChildren();
    for (const book of data.items) {
      const row = document.createElement('tr');
      for (const value of [book.title, book.author, book.genre]) {
        const cell = document.createElement('td'); cell.textContent = value; row.append(cell);
      }
      const action = document.createElement('td');
      if (book.available) {
        const button = document.createElement('button'); button.textContent = 'Check out';
        button.addEventListener('click', async () => {
          try {
            await api('/api/loans', {book_id: book.id, reader: document.querySelector('#reader').value});
            message.textContent = `Checked out ${book.title}.`; await load();
          } catch (error) { message.textContent = error.message; }
        });
        action.append(button);
      } else action.textContent = 'Checked out';
      row.append(action); table.append(row);
    }
    const loans = document.querySelector('#loans'); loans.replaceChildren();
    for (const loan of (await api('/api/loans')).items) {
      const item = document.createElement('li'); item.textContent = `${loan.reader} · ${loan.book_id}`; loans.append(item);
    }
  } catch (error) { message.textContent = error.message; }
}
document.querySelector('#filters').addEventListener('submit', event => { event.preventDefault(); page = 1; load(); });
document.querySelector('#previous').addEventListener('click', () => { page -= 1; load(); });
document.querySelector('#next').addEventListener('click', () => { page += 1; load(); });
load();
