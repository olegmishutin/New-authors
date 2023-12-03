const coverInput = document.getElementById('cover-image-input')
const coverStatus = document.getElementById('cover-status')

coverInput.addEventListener('change', function (e) {
    if (e.target.files[0]) {
        coverStatus.textContent = e.target.files[0].name
    }
})