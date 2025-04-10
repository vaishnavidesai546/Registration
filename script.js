const apiUrl = 'http://localhost:5000/api/users'; 

async function fetchUsers() {
    const response = await fetch(apiUrl);
    const users = await response.json();
    const tableBody = document.querySelector('#userTable tbody');
    tableBody.innerHTML = '';
    users.forEach(user => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${user.name}</td>
            <td>${user.email}</td>
            <td>${user.date_of_birth}</td>
            <td>
                <button class="delete" onclick="deleteUser(${user.id})">Delete</button>
8            </td>
        `;
        tableBody.appendChild(row);
    });
}


document.querySelector('#registrationForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    const name = document.querySelector('#name').value;
    const email = document.querySelector('#email').value;
    const dob = document.querySelector('#dob').value;

    const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name, email, date_of_birth: dob })
    });

    if (response.ok) {
        fetchUsers(); 
        document.querySelector('#registrationForm').reset();
    }
});


async function deleteUser(id) {
    const response = await fetch(${apiUrl}/${id}, { method: 'DELETE' });
    if (response.ok) {
        fetchUsers(); 
    }
}

// Initial load
fetchUsers();