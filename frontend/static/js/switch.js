const switcher1 = document.getElementById('switcher-1')
const switcher2 = document.getElementById('switcher-2')
switcher1.onclick = callSwitcher1
switcher2.onclick = callSwitcher2

const checkbox1 = document.getElementById('userTypeUser')
const checkbox2 = document.getElementById('userTypeAuthor')

function callSwitcher1() {
    checkbox2.removeAttribute('checked')
    switcher2.className = 'switcher'
    checkbox1.setAttribute('checked', 'checked')
    switcher1.className = 'switcher switcher-on'
}

function callSwitcher2() {
    checkbox1.removeAttribute('checked')
    switcher1.className = 'switcher'
    checkbox2.setAttribute('checked', 'checked')
    switcher2.className = 'switcher switcher-on'
}