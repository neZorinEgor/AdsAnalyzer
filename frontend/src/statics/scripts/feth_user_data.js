async function fetchUserData() {
    try {
        const response = await fetch('http://127.0.0.1:8000/user/me', {
            method: 'GET',
            headers: {
                'accept': 'application/json'
            },
            credentials: 'include' // Отправляем куки
        });

        if (response.ok) {
            const userData = await response.json();
            document.getElementById('username').textContent = userData.email;
        } else {
            const errorData = await response.json();
            console.error('Ошибка:', errorData);
        }
    } catch (error) {
        console.error('Ошибка при выполнении запроса', error);
    }
}

window.onload = fetchUserData;

async function logoutUser() {
    try {
        const response = await fetch('http://127.0.0.1:8000/auth/logout', {
            method: 'POST',
            headers: {
                'accept': 'application/json',
                'Content-Type': 'application/json' 
            },
            credentials: 'include', 
            body: JSON.stringify({}) 
        });

        if (response.ok) {
            window.location.href = 'unauthorize.html'; 
        } else {
            const errorData = await response.json();
            console.error('Ошибка при выходе:', errorData);
        }
    } catch (error) {
        console.error('Ошибка при выполнении запроса:', error);
    }
}

const logoutButton = document.getElementById('logout-button');
if (logoutButton) {
    logoutButton.addEventListener('click', logoutUser);
} else {
    console.warn('Кнопка выхода не найдена');
}
