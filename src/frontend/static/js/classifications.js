document.getElementById('create-handler-form').addEventListener('submit', async (event) => {
    event.preventDefault();

    const formData = new FormData(event.target);
    const responseDiv = document.getElementById('response');

    const baseUrl = window.location.origin;

    try {
        const response = await fetch(`http://0.0.0.0:5000/ml_endpoint/classification/create?endpoint_path=${encodeURIComponent(event.target.endpoint_path.value)}&algorithm=${encodeURIComponent(event.target.algorithm.value)}&label_name=${encodeURIComponent(event.target.label_name.value)}`, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
            },
            body: formData
        });


        const statusCode = response.status;
        const statusText = response.statusText;
        let responseBody;

        if (response.ok) {
            responseBody = await response.json();
            showNotification();  // Показ уведомления
        } else {
            responseBody = await response.text();
        }

        responseDiv.innerHTML = `
            <div class="px-4 py-2 border border-gray-300 rounded bg-white shadow">
                <h2 class="font-bold">Ответ сервера:</h2>
                <p><strong>Сообщение:</strong> ${responseBody.message}</p>
                <p><strong>Путь конечной точки:</strong> <a href="${baseUrl}${responseBody.endpoint_path}" class="text-blue-600 hover:underline">${baseUrl}${responseBody.endpoint_path}</a></p>
            </div>
        `;
    } catch (error) {
        responseDiv.innerHTML = `<p class="text-red-600">Ошибка: ${error.message}</p>`;
    }
});

function showNotification() {
    const notification = document.getElementById('notification');
    notification.classList.remove('hidden');
    setTimeout(() => {
        notification.classList.add('hidden');
    }, 5000);
}

document.getElementById('dataset').addEventListener('change', (event) => {
    const fileName = event.target.files[0] ? event.target.files[0].name : 'Не выбран файл';
    document.getElementById('file-name').textContent = fileName;
});