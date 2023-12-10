const filteringPanel = document.getElementById('filtering-panel')
let filteringPanelIsOpen = false

const pcCheckboxes = document.getElementsByClassName('pc-checkbox')
const mobileCheckboxes = document.getElementsByClassName('mobile-checkbox')

for (let i = 0; i < pcCheckboxes.length; i++) {
    pcCheckboxes[i].addEventListener('change', function () {
        mobileCheckboxes[i].checked = pcCheckboxes[i].checked
    });

    mobileCheckboxes[i].addEventListener('change', function () {
        pcCheckboxes[i].checked = mobileCheckboxes[i].checked
    });
}

document.getElementById('close-filtering-panel').onclick = closeFilteringPanel
document.getElementById('open-filtering-panel').onclick = function () {
    if (window.innerWidth <= 550) {
        filteringPanel.className = 'panel show-panel left-panel left-panel-open-animation'
        filteringPanelIsOpen = true
    }
}

function closeFilteringPanel() {
    filteringPanel.className = 'panel show-panel left-panel left-panel-close-animation'

    filteringPanel.addEventListener('animationend', function listener(e) {
        filteringPanel.className = 'panel left-panel'
        filteringPanelIsOpen = false
        filteringPanel.removeEventListener(e.type, listener)
    })
}

$(window).on('resize', function () {
    if (filteringPanelIsOpen && window.innerWidth > 550) {
        closeFilteringPanel()
    }
})