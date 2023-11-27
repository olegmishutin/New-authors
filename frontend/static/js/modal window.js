const modalWindowBox = document.getElementById('modal-window-box')
const openModalwindowButtons = document.getElementsByClassName('call-modal-window')

for (let i = 0; i < openModalwindowButtons.length; i++) {
    openModalwindowButtons[i].onclick = function () {
        modalWindowBox.className = 'modal-window-box content-padding open-modal-window-box-animation show-modal-window-box'
    }
}

document.getElementById('close-model-window').onclick = function () {
    modalWindowBox.className = 'modal-window-box content-padding close-modal-window-box-animation show-modal-window-box'

    modalWindowBox.addEventListener('animationend', function listener(e) {
        modalWindowBox.className = 'modal-window-box content-padding'
        modalWindowBox.removeEventListener(e.type, listener)
    })
}