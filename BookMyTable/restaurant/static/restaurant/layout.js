const layoutId = document.getElementById('layout-container').dataset.layoutId;
document.getElementById('add-table').addEventListener('click', function () {
    addTable();
});
document.querySelectorAll('.component').forEach(component => {
    component.addEventListener('mousedown', function (e) {
        let dragged = this;
        const offsetX = e.clientX - dragged.offsetLeft;
        const offsetY = e.clientY - dragged.offsetTop;

        function onMouseMove(e) {
            dragged.style.left = `${e.clientX - offsetX}px`;
            dragged.style.top = `${e.clientY - offsetY}px`;
        }

        function onMouseUp() {
            document.removeEventListener('mousemove', onMouseMove);
            document.removeEventListener('mouseup', onMouseUp);
        }

        document.addEventListener('mousemove', onMouseMove);
        document.addEventListener('mouseup', onMouseUp);
    });
});

document.getElementById('save-layout').addEventListener('click', function () {
    const components = [];
    document.querySelectorAll('.component').forEach(component => {
        components.push({
            id: component.dataset.id, // Use data-id attribute for existing components
            type: component.dataset.type, // e.g., "table", "door", "window"
            x: parseInt(component.style.left || 0, 10), // Default to 0 if not set
            y: parseInt(component.style.top || 0, 10),  // Default to 0 if not set
            seating_capacity: component.dataset.seatingCapacity || null,
            color: component.dataset.color || null,
            length: component.dataset.length || null
        });
    });

    fetch(`/save-layout/${layoutId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({ components: components })
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            alert(data.message);
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while saving the layout.');
        });
});

function getCSRFToken() {
    const token = document.querySelector('#csrf-container input[name="csrfmiddlewaretoken"]');
    if (!token) {
        console.error('CSRF token not found!');
        return null;
    }
    return token.value;
}
