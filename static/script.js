const currentIP = "http://192.168.1.138:5000" //localni adresa pro debug, az se pujde na production bude to url te stranky
const form = document.getElementById("uploadForm")

const darkBtn = document.getElementById('toggleDark');

        // Tohle je kód, který checkne v LocalStorage, jestli je tam uložený darkMode (Kdyby si nevěděl Lukáši)
        if (localStorage.getItem('darkMode') === 'enabled') {
            document.body.classList.add('dark');
            darkBtn.innerHTML = '<i class="fas fa-sun"></i> Light Mode';
        }

        darkBtn.addEventListener('click', () => {
            document.body.classList.toggle('dark');

            if (document.body.classList.contains('dark')) {
                localStorage.setItem('darkMode', 'enabled');
                darkBtn.innerHTML = '<i class="fas fa-sun"></i> Light Mode';
            } else {
                localStorage.setItem('darkMode', 'disabled');
                darkBtn.innerHTML = '<i class="fas fa-moon"></i> Dark Mode';
            }
        });

form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const input = document.getElementById('file');
    const file = input.files[0];

    if (!file) {
        console.error('Please select an image to upload.');
        return;
    }

    const extension = (file.name).split(".").pop().toLowerCase();
    const valid_extensions = ["jpg","jpeg","png","gif","bmp","webp","svg","tif","tiff","heic","avif"];

    if (!valid_extensions.includes(extension)) {
        alert("Wrong file extension used");
        return;
    }

    const formData = new FormData();
    formData.append('image', file);

    try {
        const response = await fetch(currentIP+'/upload_image', {
            method: 'POST',
            body: formData 
        });

        // Check if the response is OK (status 200-299)
        if (response.ok) {
            const data = await response.json();
            if (data.image_url) {
                console.log("laces");
            }
        } else {
            const errorData = await response.json();
            alert(`Error: ${errorData.error || "Something went wrong!"}`);
        }
    } catch (error) {
        console.error('Error during request:', error);
        alert('Something went wrong with the request!');
    }
});