const modalWindowBox = document.getElementById('modal-window-box')
const modalWindow = document.getElementById('model-window')

const openModalwindowButtons = document.getElementsByClassName('call-modal-window')

for (let i = 0; i < openModalwindowButtons.length; i++) {
    openModalwindowButtons[i].onclick = function () {
        modalWindowBox.className = 'modal-window-box content-padding show-modal-window-box'
        modalWindow.className = 'modal-window open-window-animation'
    }
}

document.getElementById('close-model-window').onclick = function () {
    modalWindow.className = 'modal-window close-window-animation'

    modalWindow.addEventListener('animationend', function listener(e) {
        modalWindowBox.className = 'modal-window-box content-padding'
        modalWindow.removeEventListener(e.type, listener)
    })
}